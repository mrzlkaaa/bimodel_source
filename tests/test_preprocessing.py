
from . import *
import inspect
import pandas as pd
import os
from core.preprocessing import Preprocessor

file_name = "merged_for_angular.xlsx"
# file_name = "merged_for_angular_cos.xlsx"
df_path = os.path.join(
    os.path.split(os.path.dirname(os.path.abspath(__file__)))[0],
    file_name
)


df = pd.read_excel(df_path, index_col=[0])

@pytest.fixture
def pp():
    return Preprocessor(df)

def test_drop_secondary_data(pp):
    pp.drop_secondary_data(ignore=["cos_aver"])
    assert 0

def test_mirror_angular_data(pp):
    # ad = pp.mirror_angular_data("aver",
    #         (0, 1),
    #         cos=True,
    #         dud=["l", "r"])
    ad = pp.mirror_angular_data("aver",
            (0, 180),
            cos=False,
            dud=["l", "r"])
    print(ad)
    assert 0

def test_list_vars(pp):
    print(inspect.signature(pp.mirror_angular_data))
    assert 0