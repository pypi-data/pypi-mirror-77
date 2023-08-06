# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import numpy as np
from chainladder.utils.sparse import sp
import pandas as pd
import copy
from chainladder.methods import Chainladder

class MackChainladder(Chainladder):
    """ Basic stochastic chainladder method popularized by Thomas Mack

    Parameters
    ----------
    None

    Attributes
    ----------
    triangle
        returns **X**
    ultimate_
        The ultimate losses per the method
    ibnr_
        The IBNR per the method
    full_expectation_
        The ultimates back-filled to each development period in **X** replacing
        the known data
    full_triangle_
        The ultimates back-filled to each development period in **X** retaining
        the known data
    summary_
        summary of the model
    full_std_err_
        The full standard error
    total_process_risk_
        The total process error
    total_parameter_risk_
        The total parameter error
    mack_std_err_
        The total prediction error by origin period
    total_mack_std_err_
        The total prediction error across all origin periods

    """

    def fit(self, X, y=None, sample_weight=None):
        """Fit the model with X.

        Parameters
        ----------
        X : Triangle-like
            Data to which the model will be applied.
        y : Ignored
        sample_weight : Ignored

        Returns
        -------
        self : object
            Returns the instance itself.
        """
        super().fit(X, y, sample_weight)
        # Caching full_triangle_ for fit as it is called a lot
        self._full_triangle_ = self.full_triangle_
        self.average_ = self.X_.average_
        self._mack_recursion('param_risk')
        self._mack_recursion('process_risk')
        self._mack_recursion('total_param_risk')
        del self._full_triangle_
        self.process_variance_ = self._include_process_variance()
        return self

    @property
    def full_std_err_(self):
        from chainladder.utils.utility_functions import num_to_nan
        obj = copy.copy(self.X_)
        xp = obj.get_array_module()
        lxp = self.X_.ldf_.get_array_module()
        full = self.full_triangle_
        tri_array = full.values
        weight_dict = {'regression': 0, 'volume': 1, 'simple': 2}
        avg = list(self.average_) if type(self.average_) is not list else self.average_
        val = xp.array([weight_dict.get(item.lower(), 2)
                        for item in avg + [avg[-1]]])
        val = xp.broadcast_to(val, self.X_.shape)
        weight = num_to_nan(xp.sqrt(tri_array[..., :len(self.X_.ddims)]**(2-val)))
        obj.values = self.X_.sigma_.values / weight
        w = lxp.concatenate(
            (self.X_.w_, lxp.ones((*val.shape[:3], 1))*xp.nan), axis=3)
        w[xp.isnan(w)] = 1
        obj.values = xp.nan_to_num(obj.values) * xp.array(w)
        obj.valuation_date = full.valuation_date
        obj._set_slicers()
        return obj

    @property
    def total_process_risk_(self):
        obj = copy.copy(self.process_risk_)
        xp = obj.get_array_module()
        obj.values = xp.sqrt(xp.nansum(self.process_risk_.values**2, 2))
        obj.values = obj.values[:, :, None,...]
        obj.odims = ['tot_proc_risk']
        obj._set_slicers()
        return obj

    def _mack_recursion(self, est):
        obj = copy.copy(self.X_)
        xp = obj.get_array_module()
        nans = self.X_.nan_triangle[None, None]
        nans = nans * xp.ones(self.X_.shape)
        nans = xp.concatenate(
            (nans, xp.ones((*self.X_.shape[:3], 1))*xp.nan), 3)
        nans = 1-xp.nan_to_num(nans)
        properties = self._full_triangle_
        obj.ddims = np.concatenate(
            (properties.ddims[:len(self.X_.ddims)],
            np.array([properties.ddims[-1]])))
        obj.valuation_date = self._full_triangle_.valuation_date
        risk_arr = xp.zeros((*self.X_.shape[:3], 1))
        if est == 'param_risk':
            obj.values = self._get_risk(nans, risk_arr,
                                        obj.std_err_.values)
            obj._set_slicers()
            self.parameter_risk_ = obj
        elif est == 'process_risk':
            obj.values = self._get_risk(nans, risk_arr,
                                        self.full_std_err_.values)
            obj._set_slicers()
            self.process_risk_ = obj
        else:
            risk_arr = risk_arr[..., 0:1, :]
            obj.values = self._get_tot_param_risk(risk_arr)
            obj.odims = ['Total param risk']
            obj._set_slicers()
            self.total_parameter_risk_ = obj

    def _get_risk(self, nans, risk_arr, std_err):
        xp = self._full_triangle_.get_array_module()
        lxp = self.X_.ldf_.get_array_module()
        full_tri = xp.nan_to_num(self._full_triangle_.values)[..., :len(self.X_.ddims)]
        t1_t = (full_tri * std_err)**2
        extend = self.X_.ldf_.shape[-1]-self.X_.shape[-1]+1
        ldf = self.X_.ldf_.values[..., :len(self.X_.ddims)-1]
        ldf = lxp.concatenate(
            (ldf, lxp.prod(self.X_.ldf_.values[..., -extend:], -1,
             keepdims=True)), -1)
        for i in range(len(self.X_.ddims)):
            t1 = t1_t[..., i:i+1]
            t2 = (ldf[..., i:i+1] * risk_arr[..., i:i+1])**2
            t_tot = xp.sqrt(t1+t2)*nans[..., i+1:i+2]
            risk_arr = xp.concatenate((risk_arr, xp.nan_to_num(t_tot)), 3)
        return risk_arr

    def _get_tot_param_risk(self, risk_arr):
        """ This assumes triangle symmertry """
        xp = self._full_triangle_.get_array_module()
        lxp = self.X_.ldf_.get_array_module()
        t1 = xp.nan_to_num(self._full_triangle_.values)[..., :len(self.X_.ddims)] - \
            xp.nan_to_num(self.X_.values) + \
            xp.nan_to_num((self.X_-self.X_[self.X_.valuation<self.X_.valuation_date]).values)
        t1 = xp.sum(t1*self.X_.std_err_.values, axis=2, keepdims=True)
        extend = self.X_.ldf_.shape[-1]-self.X_.shape[-1]+1
        ldf = self.X_.ldf_.values[..., :len(self.X_.ddims)-1]
        ldf = lxp.concatenate(
            (ldf, lxp.prod(self.X_.ldf_.values[..., -extend:], -1,
             keepdims=True)), -1)
        ldf = lxp.unique(ldf, axis=-2)
        for i in range(self._full_triangle_.shape[-1]-1):
            t_tot = xp.sqrt((t1[..., i:i+1])**2 + (ldf[..., i:i+1] *
                            risk_arr[..., -1:])**2)
            risk_arr = xp.concatenate((risk_arr, xp.nan_to_num(t_tot)), -1)
        return risk_arr

    @property
    def mack_std_err_(self):
        obj = copy.copy(self.parameter_risk_)
        xp = obj.get_array_module()
        obj.values = xp.sqrt(self.parameter_risk_.values**2 +
                             self.process_risk_.values**2)
        obj._set_slicers()
        if obj.array_backend=='sparse':
            obj.num_to_nan()
        return obj

    @property
    def total_mack_std_err_(self):
        obj = copy.copy(self.X_.latest_diagonal)
        xp = obj.get_array_module()
        obj.values = xp.sqrt(self.total_process_risk_.values**2 +
                             self.total_parameter_risk_.values**2)
        obj.values = obj.values[..., -1:]
        return pd.DataFrame(
            obj.values[..., 0, 0], index=obj.kdims,
            columns=[item for item in obj.vdims])

    @property
    def summary_(self):
        # This might be better as a dataframe
        obj = copy.copy(self.X_)
        xp = obj.get_array_module()
        obj.values = xp.concatenate(
            (self.X_.latest_diagonal.values,
             self.ibnr_.values,
             self.ultimate_.values,
             self.mack_std_err_.values[..., -1:]), 3)
        obj.ddims = ['Latest', 'IBNR', 'Ultimate', 'Mack Std Err']
        obj.valuation_date = self.ultimate_.valuation_date
        obj._set_slicers()
        return obj
