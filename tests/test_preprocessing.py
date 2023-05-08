
from . import *
import inspect
import pandas as pd
import os
from core.preprocessing import Preprocessor

# file_name = "excels/merged_for_angular_deg_sr_CDF.xlsx"
# file_name = "excels/merged_for_angular_deg_sr_CDF.xlsx"
file_name = "excels/merged_for_angular.xlsx" #* deg /sr/lethargy no lg and rg

df_path = os.path.join(
    os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],
    file_name
)


df = pd.read_excel(df_path, index_col=[0])

cols = ['1.000', '2.000', '3.000', '4.000', '5.000', '6.000', '7.000', '8.000',
    '9.000', '10.000', '11.000', '12.000', '13.000', '14.000']

@pytest.fixture
def pp():
    return Preprocessor(df, "aver")

def test_drop_secondary_data(pp):
    pp.drop_secondary_data(ignore=["cos_aver"])
    assert 0

def test_angular_data(pp):
    ad = pp.angular_data(
        sr=True,
        lethargy=True,
        # lg = "l",
        # rg = "r"
    )
    print(ad)
    assert 0

def test_list_vars(pp):
    print(inspect.signature(pp.mirror_angular_data))
    assert 0

def test_get_groups(pp):
    groups = pp._get_groups("l", "r")
    print(groups)
    assert 0