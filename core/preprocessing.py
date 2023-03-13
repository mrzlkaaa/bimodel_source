from __future__ import annotations
from typing import List, Union
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Preprocessor:
    def __init__(self, df):
        self.df = df
        self._mms = MinMaxScaler(feature_range=(-1, 1))

    @property
    def mms(self) -> MinMaxScaler:
        return self._mms

    @mms.setter
    def mms(self, feature_range) -> None:
        self._mms = MinMaxScaler(feature_range=feature_range)

    def drop_secondary_data(
        self, key:str="_",
        ignore: Union[List[str], None] = None
    ) -> None:
        """
        * drop column which contains keyword - key
        * if ignore array is given exclude this cols from todrop array
        """
        #! drop column by regex
        cols = self.df.columns
        todrop = [i for i in cols if key in i]
        if ignore is not None:
            todrop = [i for i in todrop if not i in ignore]

        self.df = self.df.drop(labels=todrop, axis=1)

    def drop_unused_cols(self, cols: List[str]) -> None:
        self.df = self.df.drop(labels=cols, axis=1)

    def mirror_angular_data(
        self, X_col_name: str,
        range_:tuple=(),
        cos:bool=False,
        dsd: Union[tuple, None]=("_", None),
        dud: Union[List[str], None]=None,
        scale: bool=True,
        zero_centered: bool=True
    ) -> pd.core.DataFrame:
        """
        * mirror df to new df_new
        * joins df and df_new
        * so extends df to new one

        * Parameters
        * ---------
        * X_col_name : str, positional
        *   X axis of data    
        * range_: tuple, positional
        *   indicates the range of data (min, max values)
        * cos: bool, optional
        *   stands for is angular data is in units of cos
        * dsd: Union[tuple, None]=("_", None), optional
        *    drop_secondary_data where the tuple is (key, ignore) params
        * dud: Union[List[str], None]=None, optional
        *   drop_unused_data takes array of str as a columns name to drop
        * scale: bool, optional
        *   scale a given column by a max value
        * zero_centered: bool, optional, default: True
        *   helper to normalize and zero center X axis
        """

        min_, max_ = range_  # * move range_ to config file

        if dsd is not None:
            key, ignore = dsd
            self.drop_secondary_data(key, ignore)
        
        if dud is not None:
            self.drop_unused_cols(cols=dud)

        if scale:
            scale_cols = list(set(self.df.columns).difference(set([X_col_name])))
            self.df[scale_cols] = self.df.loc[:, scale_cols].apply(lambda x: x/x.max(), axis=0)

        df_c = self.df.copy()

        if not cos:
            mirror_X = [min_ - i for i in df_c[X_col_name]] #* builds new X from -90 to 90
        else:
            mirror_X = [abs(min_ - i) + 1 for i in df_c[X_col_name]][::-1] #* builds new X from 0 to 2 where 1 is 90 deg
        
        df_c = df_c.reset_index(drop=True)
        df_c[X_col_name] = mirror_X

        new_df = pd.concat([self.df, df_c]).reset_index(drop=True)

        if not cos and zero_centered:
            # pass
            new_df[X_col_name] = new_df[X_col_name]/new_df[X_col_name].max()

        elif cos and zero_centered:
            new_df[X_col_name] = self.zero_centered_normalize(new_df[X_col_name])

        return new_df
    
    def zero_centered_normalize(
        self, 
        data: Union[np.ndarray, pd.core.series.Series],
        to2D: bool=True
    ) -> np.ndarray:

        if type(data) != np.ndarray:
            data = data.to_numpy()

        #* aim 2d arr shape
        shape = (len(data), 1)
        if to2D:
            data = data.reshape(-1, 1)
        if not self._check_shape(data.shape, shape):
            raise ValueError("Expected 2D array")  

        return self.mms.fit_transform(data).reshape(len(data))

        
    def _check_shape(self, shape1, shape2):
        if shape1 == shape2:
            return True
        return False

    @classmethod
    def read_excel(
        cls, 
        path: str, 
        index_col: Union[int, str]=0
    ) -> object:
        return  cls(pd.read_excel(path, index_col=[index_col]))

