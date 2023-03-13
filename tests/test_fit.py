from . import *
import pandas as pd
from core.fit import Fit

df_fit = pd.read_excel("df_to_fit.xlsx", index_col=[0])

@pytest.fixture
def fit():
    return Fit(df_fit)

def test_df_fit(fit):
    fit.df_fit("aver")
    assert 0