from __future__ import annotations
from hashlib import new
from typing import List, Union, Any, TypeVar, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


lub = TypeVar("lub", str, float, int)

class Preprocessor:
    '''
    #* Class description
    #* Attributes
    #* ----------
    #* Methods
    #* ----------
    #* Add method after cleaning the code
    #*'''
    def __init__(self,
        df: pd.core.DataFrame,
        X_col_name: str | None = "aver",
        dsd: Union[str, None]="_",
        dud: Union[List[str], None]=None,
    ) -> None:
        """
        #* Parameters
        #* ----------
        #* df: pd.core.DataFrame
        #*  input DataFrame to apply preprocessing on
        #* X_col_name : str, optional
        #*  X axis of dataframe
        #* dsd: Union[tuple, None]=("_", None), optional
        #*   drop_secondary_data - data to drop by key in string
        #* dud: Union[List[str], None]=None, optional
        #*  drop_unused_data takes array of str as a columns name to drop
        """

        self.df = df
        self.X_col_name = X_col_name
        self.dsd = dsd
        self.dud = dud

        self._data_cleaning()

    #! In case of scaling of the tool
    #! some arguments better to move to __init__ section
    def angular_data(
        self, 
        # cos:bool=False, #! applied only for mirror section
        X_col_name: str | None = None,
        sr: bool=True,  #* set True by default
        norm: bool=True,
        egroups: bool=True,
        #! if "l" or "r" are required in df lb and ub can be removed
        lb: float = 0.5,
        ub: float = 14.5,
        lg: str | None = None,   #* works with egroups only
        rg: str | None = None,   #* works with egroups only
        lethargy: bool = True,   #* works with egroups only
        width: Union[str, float, int] | None = None,
        # mirror: bool = True
    ) -> Tuple[pd.core.DataFrame, float, list, list]:
        """
        * makes preproccesing of angular data
        * input data frame consists of 3 info columns:
        * "l", "r" and "aver" - this default names and 
        * stands for left and rigth boundaries of angle groups
        * "aver" is average angle in group
        * the rest columns are data to preprocess
        * the data is descrete type so 1 value belogns to 1 group
        * the units of data can be devided by lethargy and steradian so
        * function arguments shall be provided accordingly

        * Parameters
        * ---------
        * cos: bool, optional
        *   stands for is angular data is in units of cos
        
        * sr: bool, optional
        *   indicates whether a given data devided by steradian (solid angle)
        *   if set to True does back normalization (multiply by angle of steradian)
        * norm: bool, optional
        *   normilize all columns except X_col_name
        * egroups: bool, optional
        *   param to create new array filled with energies 
        *   that are stands for energy groups
        *   by default columns with names "l" and "r" are
        *   consider as a lower and upper energies.
        * lethargy: bool, optional
        *   if parameter is true values in column are normalized
        *   by lethargy so then back normalization required to get rigth weights
        *   False value does nothing
        * width: float | int
        *   constant to use as normalizer on X axis

        * Returns
        * ---------
        * new_df: pd.core.DataFrame
        *   df with 1 info column "aver" that can be normalized
        *   to be zero centred
        *   the number and size of data columns the same
        *   depends on optional arguments can be normalized
        * width: float
        *   width of gauss distibution to use on Fit stage
        * weigths: list
        *   relative weights of spectrum (portion of particles for a given energy)
        * groups: list
        *   array of floats describes energy groups
        """

        if not X_col_name:
            X_col_name: str = self.X_col_name
        data_cols: list[Any] = self._exclude_df_cols(X_col_name)

        agroups: list | None = None
        
        weights: np.ndarray = self._columns_weight(cols=data_cols)
    
        #* the aim is to to multiply all data_cols by sr
        #* it's required to get right weight of energy groups
        if sr:
            
            agroups = self.df.loc[:, X_col_name]  #* average angles
            if lg and rg:
                agroups = self._get_groups(lg, rg)
                data_cols: list[Any] = self._exclude_df_cols(X_col_name, lg, rg)
                #* lg and rg are dropped
                self.df = self.df.drop([lg, rg], axis=1)

            df_sr = self.df.loc[:, data_cols]\
                .apply(lambda x: x*agroups, axis=0)

            #* calls _columns_weight to update weights 
            weights = self._columns_weight(cols=data_cols, df=df_sr)

        egroups = [lb, *self._aver_to_group(data_cols), ub]

        #* multiply current weights by lethrgy to get weight * Ln(Ei+1/Ei)
        if lethargy:
            weights = np.array([
                weights[n]*np.log(egroups[n+1]/egroups[n])
                for n, _ in enumerate(egroups)
                if n != len(egroups) - 1
            ])
            #* normalize by sum to get right weight that 
            #* corresponds with initial data
            weights = weights/weights.sum()

        #* data_cols normalization by sum
        if norm:
            self._normalize_df(tpe="sum", cols=data_cols)


        #* get the width before X normalization
        # * do not required of X axis doesnt changes
        # if width is None:
        #     width = self._min_max_diff(X_col_name)

        new_df = self.df.copy()

        #* normalize of X axis to get values in range of 0 to 1
        new_df[X_col_name] = new_df[X_col_name]/new_df[X_col_name].max()
        
        #? returns new_df: df, width of distribution: float, source weights: arr
        #? add gruops as extra return of function
        return new_df, width, weights, egroups

    def _aver_to_group(self, Es: list):
        '''
        #* method does back to groups normalization
        #* so Es is array of average energies
        #* it does return new array with shape
        #* equal to shape of input array 
        #* Parameters
        #* ----------
        #* Es: list
        #*  input array of average energies
        #*  each Esi indicate value average
        #*  value in group of [ Esj, Esj+1 ]
        #* Returns
        #* ----------
        #* array where each pair is a group
        '''
        return [(float(Es[n+1])
                + float(Es[n]))/2
                for n, i in enumerate(Es)
                if not n == len(Es)-1
        ]

    def _zero_centered_normalize(
        self, 
        data: Union[np.ndarray, pd.core.series.Series],
        to2D: bool=True
    ) -> np.ndarray:
        '''
        #* Private method applies MinMaxNorm (-1, 1)
        #* to zero centered data
        #* Parameters
        #* ----------
        #* data: Union[np.ndarray, pd.core.series.Series]
        #*  X axis to which MinMaxNorm applies
        #* to2D: bool, optional
        #*  transfroms data to 2D array
        #*  if set to True 
        #* Raises
        #* ----------
        #* ValueError
        #*  if data is not 2D array or
        #*  2D transform has not been applied
        #*  so self._check_shape method failed
        #* Returns
        #* ----------
        #* 1D array on which MinMaxNorm was applied
        #* MinMaxNorm returns 2D array so reshape method used
        #* to get 1D array as an output
        '''

        if type(data) != np.ndarray:
            data = data.to_numpy()

        #* aim 2d arr shape
        shape = (len(data), 1)
        if to2D:
            data = data.reshape(-1, 1)
        if not self._check_shape(data.shape, shape):
            raise ValueError("Expected 2D array")  

        return self.mms.fit_transform(data).reshape(len(data))

    def _data_cleaning(self) -> None:
        '''
        #* modify inifial df
        #* drops column by columns name
        #* that are given in dud and dsd
        '''
        if self.dud is not None:
            self._drop_unused_data(self.dud)
        
        if self.dsd is not None:
            self._drop_secondary_data(self.dsd)


    def _drop_secondary_data(
        self, 
        key: str="_",
    ) -> None:
        """
        * drop column which contains keyword - key
        * if ignore array is given exclude this cols from todrop array
        """
        #! drop column by regex or by containing of key
        cols = self.df.columns
        todrop = [i for i in cols if key in i]
        self.df = self.df.drop(labels=todrop, axis=1)

    def _drop_unused_data(self, cols: List[str]) -> None:
        '''
        #* drops columns from dataframe
        #* Parameters
        #* ----------
        #* cols: List[str]
        #*  array of columns name
        '''
        self.df = self.df.drop(labels=cols, axis=1)

    def _get_groups(self, lg: str, rg: str):
        left = self.df.loc[1:, lg] - self.df.loc[0, lg]
        right = self.df.loc[:, rg] - self.df.loc[0, lg]
        return sorted(list(set(
            [
            *left.to_numpy(),
            *right.to_numpy()
            ]
        )))

    def _columns_weight(
        self,
        cols: List[Any],
        df: pd.Data.DataFrame | None = None,
    ) -> np.ndarray:
        '''
        #* computate weight of energy
        #* in a spectrum 
        #* Parameters
        #* ----------
        #* cols: List[Any]
        #*  column names to use to get a weights
        #* Returns
        #* ----------
        #* array of weights
        '''
        if df is None:
            df = self.df
        cols_sum = df.loc[:, cols].sum(axis=0)
        total = cols_sum.sum()
        return (cols_sum/total).to_numpy()

    def _exclude_df_cols(self, *to_exclude: Tuple[Any]):
        to_exclude = list(to_exclude)
        return self.df.drop(labels=to_exclude, axis=1).columns

    def _check_shape(
        self,
        shape1: tuple, 
        shape2: tuple
    ) -> bool:
        if shape1 == shape2:
            return True
        return False

    def _normalize_df(
        self, 
        tpe: str,
        cols: List[Any] | None=None
    ) -> None:

        norm_cols = self.df.columns
        if cols is not None:
            norm_cols = cols

        #* hardcoded by now
        if tpe == "sum":
            self.df[norm_cols] = self.df.loc[:, norm_cols].apply(lambda x: x/x.sum(), axis=0)

    def _min_max_diff(self, column):
        #? takes average data that is defferent from full width
        # return self.df[column].max() - self.df[column].min()
        return self.df[column].max()  #* full width of distribution

    @classmethod
    def read_excel(
        cls,
        path: str,
        index_col: Union[int, str]=0
    ) -> object:
        return  cls(pd.read_excel(path, index_col=[index_col]))


#* In case of scaling of preprocessing
#* Creates abstract class
#* way to avoid referecne - inherit troubles
# class Factory(ABC):
    # @abstractmerthod
    # def process

# class Angular(Factory):
#     # def process

# class Anyother(Factory):
#     # def process