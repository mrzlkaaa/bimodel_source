import numpy as np
import pandas as pd
from typing import Union
from scipy.optimize import curve_fit

class Fit:

    """
    * Fits angular distributions to a existing math distributions
    * to get continious functions for latter use
    * by now only gauss fitting is implemented
    """
    def __init__(
        self,
        df: Union[pd.core.frame.DataFrame, None]
    ) -> None:
        # self.config = config #* injected
        self.df = df

    def gauss(self, x, x0, A, sigma):
        return A * np.exp(-(x - x0)**2/(2*(sigma)** 2))

    def gauss_fit_coefs(
        self,
        ff_name:str,
        X: np.ndarray, 
        y: np.ndarray
    ):
        #! call get method to config file to check if given ff_name correct
        # ! then to call gettattr only 
        ff = getattr(self, ff_name)
        popt, _ = curve_fit(ff, X, y)
        return popt

    def df_fit(
        self, X_col_name: str, ff_name: str = "gauss"):
        """
        * method serves to fit df data to one of the fitting functions
        * Parameters
        * ---------
        * df: pd.core.DataFrame, positional
        *   df to fit
        * X_col_name: str, positional
        *   variable indicates the X axis column
        * ff_name: str, optional, default - gauss
        *   stands for fitting function to use to fit df data
        """
        X = self.df[X_col_name]
        y = list(set(self.df.columns).difference(set([X_col_name])))
        print(y)

        coefs = []
        fitted = []

        for i in range(len(y)):
            coef = self.gauss_fit_coefs(ff_name, X, self.df.loc[:, y[i]])
            fitted.append(self.gauss(X, *coef))
            coefs.append(coef)

        return coefs, fitted

    def get_real_gauss_sigma(self):
        return

    @classmethod
    def read_excel(
        cls, 
        path: str, 
        index_col: Union[int, str]=0
    ) -> object:
        return  cls(pd.read_excel(path, index_col=[index_col]))
