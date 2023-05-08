from . import *
import pandas as pd
import numpy as np
from core.fit import Fit
from core import config

df_fit = pd.read_excel("df_to_fit.xlsx", index_col=[0])
cfg = config().get("fit")

weights = [
    0.02943593, 0.05356905, 0.07547133, 0.09039583, 0.10303477,
    0.10160338, 0.09509044, 0.08739734, 0.07862605, 0.07569147,
    0.07319083, 0.06369493, 0.04305667, 0.02974198
]

df_new_fits = pd.read_excel("to_appr_13.6.xlsx")
# df_new_fits = pd.read_excel("to_appr_15.xlsx")
# df_new_fits = pd.read_excel("to_appr_22.xlsx")
# df_new_fits = pd.read_excel("to_appr_35.xlsx")
# df_new_fits = pd.read_excel("sum_angles.xlsx")

@pytest.fixture
def fit():
    return Fit(df_fit, cfg, "laplace")

@pytest.fixture
def new_fit():
    return Fit(df_new_fits, cfg, "laplace")

def test_df_fit(fit):
    coefs, fttd = fit.df_fit("aver", width=72, weights=weights)
    print(coefs)
    assert 0

def test_new_df_fit(new_fit):
    coefs, fttd = new_fit.df_fit("aver", width=1, weights=[1])
    print(coefs)
    print(fttd)
    assert 0

def test_watt_fit():
    f = Fit(df_new_fits, cfg, "watt")
    coefs, fitted = f.df_fit("E", 1, weights)
    print(coefs)
    for i in fitted[0]:
        print(i)
    print(fitted.sum())
    assert 0
    # assert 0.95 < fttd.sum() < 1.05

def test_maxwell_fit():
    f = Fit(df_new_fits, cfg, "maxwell")
    coefs, fitted = f.df_fit("E", 1, weights)
    print(coefs)
    for i in fitted[0]:
        print(i)
    print(fitted.sum())
    assert 0


def test_get_maxwell_spectra():
    f = Fit(df_new_fits, cfg, "maxwell")
    maxwell = f.maxwell(df_new_fits["E"], 2.33)
    print(maxwell.sum())
    assert 0

def test_gamma_fit():
    a = 4.415837807475444
    f = Fit(df_new_fits, cfg, "gamma")
    fitted = f.gamma(df_new_fits["E"], shape=3/2, scale = a)
    for i in fitted:
        print(i)
    print(fitted.sum())
    assert 0