
from . import *
from core.prompt import Prompt, Inquirer
from .test_preprocessing import file_name, Preprocessor
from core import config, questions
from core.db import Cyclotrone
from core.writer import PlainPhitsSourceWriter
from prompt_toolkit.shortcuts import input_dialog
import inspect


# from PyInquirer import prompt

def test_initialize_collection():
    p = Prompt(config)
    assert type(p.collection) == Cyclotrone

@pytest.fixture
def p():
    c = config()
    return Inquirer(c, questions)

def test_parse_flag(p):
    string = "--dud=1,2 -S=true -Z=True --dud=l,r"
    
    p._parse_flags(string)

    assert 0

def test_parse_preprocess(p):
    string = "-X=aver -S=true -Z=true --dud=l,r"
    pp = Preprocessor.read_excel(file_name)
    df = pp.mirror_angular_data(**p._parse_flags(string))
    print(df)
    assert 0

@pytest.mark.parametrize("flag, inp, expected", 
    [("X_col_name", "123", "123"),
    ("scale", "FALSE", False),
    ("dud", "l, r", ["l","r"])]
)
def test_convert_value(p, flag, inp, expected):
    assert p.convert_value(flag, inp) == expected

def test_make_source(p):
    p.make_source()
    # prompt(questions)
    assert 0

@pytest.mark.parametrize("inp, res, expected", 
    [
        ("Q1cyclotrone", None, "deutron"),
        ("Q2cyclotrone", "deutron", ["Li", "Be"]),
        ("Q3cyclotrone", "Be", ["3mm","4mm", "5mm"]),
        
    ]
)
def test_get_values(p, inp, res, expected):
    vals = p._get_values(inp, res=res)
    print(vals, expected)
    print(p.querys_chain)
    assert 0

def test_get_source_params(p):
    d = {
        'source_type': 'cyclotrone', 
        'particle': 'deutron', 
        'target': 'Be', 
        'thick': '5mm', 
        'beam': '13.6MeV', 
        'groups': '14', 
        'angular_function': 'laplace', 
        'energetic_function': 'watt'
    }

    p.querys_chain = d
    source = p._get_source_params()
    print(source)
    assert 0

def test_new_source_data(p):
    p.new_source_data()

@pytest.fixture
def Commands():
    return Commands(config)


def test_write_source():
    d = {
        'angular_params': {
            '0': {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            '1': {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'}, 
            '2': {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'}, 
            '3': {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'}, 
            '4': {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'}, 
            '5': {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'}, 
            '6': {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'}, 
            '7': {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'}, 
            '8': {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            '9': {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            '10': {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'}, 
            '11': {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            '12': {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            '13': {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
        }, 
        'energetic_params': {'a': '2.488', 'b': '0.788', 'c': '0.104'}
    }

    # PlainPhitsSourceWriter(
    #     d["angular_params"], 
    #     params_order=None,
    #     energetic_params=d["energetic_params"]
    # ).fit_to_template()

def test_inspect_dialog():
    print(dir(input_dialog))
    print(inspect.getmembers(input_dialog))
    assert 0