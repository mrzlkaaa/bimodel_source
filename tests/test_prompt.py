from . import *
from core.prompt import Prompt
from .test_preprocessing import file_name, Preprocessor

@pytest.fixture
def p():
    return Prompt()

def test_parse_flag(p):
    string = "--dud=['1','2'] -X=lolcol, -Z=True"
    
    p._parse_flags(string)

    assert 0

def test_parse_preprocess(p):
    string = "-X='aver', -R=(0,180)"
    pp = Preprocessor.read_excel(file_name)
    df = pp.mirror_angular_data(p._parse_flags(string))
    print(df)
    assert 0