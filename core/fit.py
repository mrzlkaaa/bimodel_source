import numpy as np
import pandas as pd
import scipy.special as sps
import math
from typing import Union, Tuple, Callable
from scipy.optimize import curve_fit

class Fit:
    """
    * Fits angular distributions to a existing math distributions
    * to get continious functions for latter use
    * by now only gauss fitting is implemented
    * Attributes
    * -----------
    * ff_name: str, optional, default - gauss
        *   stands for fitting function name to use to fit df data
    """
    def __init__(
        self,
        df: Union[pd.core.frame.DataFrame, None],
        config: dict,
        ff_name: str = "gauss"
    ) -> None:
        self.df = df
        print(config)
        self.config = config  #* injected
        self.ff = self.initialize_ff(ff_name)  #* method to call


    def initialize_ff(self, ff_name: str) -> Callable:
        '''
        #* Initialize the fitting function by a key
        #* if a key exists returns method that assotites with a key
        #* Parameters
        #* ----------
        #* ff_name: str
        #*  name of fitting function in a string format
        #* Raises
        #* ----------
        #* KeyError
        #*  if there are no mathces for a given ff_name
        #* Returns
        #* ----------
        #* method (callable) that assotiates with ff_name
        '''
        ff = self.config.get("ff").get(ff_name)
        if ff is None:
            raise KeyError("Given fitting function is not found")
        return getattr(self, ff)

    #! must be gausss_pdf
    #! and gauss_cdf ???
    def gauss(
        self, 
        x: float,
        A: float,
        sigma: float, 
        # x0:float | None=0, 
    ) -> float:
        # return A*np.exp(-1/2*(x - 0)**2/((sigma)** 2))
        return A*np.exp(-(x - 0)**2/(sigma)** 2)

    def laplace(self, x, A, sigma):
        return A*np.exp(- abs(x - 0)/sigma)

    def watt(
        self,
        x,
        a,
        b,
        c
    ) -> float:
        return c*1/((3.14*a*b)**1/2) * np.sinh((4*x*b/a**2)**1/2) * np.exp(-(b+x)/a) #* a,b,c where b is Ek of residiuals

    def maxwell(
        self,
        x,
        a,
        b
    ) -> float:
        return b*2*((x/3.14)**1/2)/(a**3/2)*np.exp(-x/a)
        # return b*(x**1/2)*np.exp(-x/a) #* Terrell's formula
    
    #! basic test
    def gamma(
        self,
        x,
        shape,
        scale
    ) -> float:
        return x**(shape-1)*(np.exp(-x/scale) /  
                     (sps.gamma(shape)*scale**shape))

    def fitting_coefs(
        self,
        X: np.ndarray, 
        y: np.ndarray
    ) -> np.ndarray:
        popt, _ = curve_fit(self.ff, X, y)
        return popt

    def df_fit(
        self,
        X_col_name: str,
        weights: np.ndarray,
        width: Union[int, float] = None,
        as_dict:bool = True #? under dev or will be removed
    ) -> Tuple[list, list]:
        """
        * method serves to fit df data to one of the fitting functions
        * Parameters
        * ---------
        * df: pd.core.DataFrame, positional
        *   df to fit
        * X_col_name: str, positional
        *   variable indicates the X axis column
        * width: Union[int, float, None], optional
        *   scaling factor that indicates real width of distribution
        """

        X = self.df[X_col_name].to_numpy()
        # y = np.sort(np.array(list(set(self.df.columns).difference(set([X_col_name])))))
        y = self.df.drop([X_col_name], axis=1).columns

        coefs = []
        fitted = []

        for i in range(len(y)):
            coef = self.fitting_coefs(X, self.df.loc[:, y[i]])
            #* drops x0 coef cuz it's nill (zero centered gauss)
            # coef = coef[:-1]
            fitted.append(self.ff(X, *coef))
            coefs.append(coef)

        coefs = np.array(coefs)
        fitted = np.array(fitted)
        #* normalization of sigma to real width to get real std.dev
        #? useless i think
        if width is not None:
            try:
                width = float(width)
            except TypeError as e:
                raise e
            coefs[:, -1] = coefs[:, -1]*width
        #* join y (columns name) and coefs to get all required coefs for a source
        #* coefs: A, sigma, weight, E
        coefs = [[*coefs[i], weights[i], y[i]] for i in range(len(coefs))]

        # if as_dict:


        return coefs, fitted

    @classmethod
    def read_excel(
        cls, 
        path: str, 
        index_col: Union[int, str]=0
    ) -> object:
        return  cls(pd.read_excel(path, index_col=[index_col]))
