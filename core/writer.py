from abc import ABC, abstractmethod
from functools import reduce
from typing import Any, Dict, Union, List, TypeVar
import os
from string import Template
import numpy as np
import json
from . import config

Config = TypeVar("Config", bound=Dict[str, Union[str, list, bool]])

T = TypeVar("T")
V = TypeVar("V")

class SourceWriter(ABC):

    SOURCE_PARAMS = "source_params"
    def __init__(
        self,
        #* config injection required in order to get energy distr params
        #* if order is not given accepts source_params as a dict
        source_template:str = "poly_laplace",
        config: Config | None = None
        # deutrons_en: float = 13.6
    ):
        self.config = config

        self.default_source_params:\
            Dict[str, str] = self._default_params_payload()

        self.template = self._template_path(source_template)

    def fit_to_template(self):
        '''
        #* Method description
        #* Parameters
        #* ----------
        #*
        #* Raises
        #* ----------
        #*
        #* Returns
        #* ----------
        #*
        '''
        #! template of source can be dynamic
        #! move it to __init__
        with open(self.template, "r") as s:
            cont = s.read()
        t = Template(cont)
        #* iterate over dynamic params
        for i in range(len(self.source_params)):
            self.write(t.safe_substitute(**self.source_params[f"{i}"], **self.default_source_params))

    def write(self, block: str) -> None:
        '''
        #* Write a datablock to a file
        #* If file exists appends to 
        #* Parameters
        #* ----------
        #* block: str
        #* datablock to write
        
        '''
        with open("source", "a+") as f:
            f.write(block)


    def _template_path(self, source_template: str) -> str:
        '''
        #* Method description
        #* Parameters
        #* ----------
        #*
        #* Raises
        #* ----------
        #*
        #* Returns
        #* ----------
        #*
        '''
        path = os.path.join(
            
            os.path.split(os.path.abspath(__file__))[0],
            "templates",
            source_template
        )
        self.file_checker(path)

        return path

    def _default_params_payload(self):
        '''
        #* Does load of source parameters
        #* from a file
        #* Parameters
        #* ----------
        #*
        #* Raises
        #* ----------
        #*
        #* Returns
        #* ----------
        #*
        '''     
        kv: Dict[str, str] = dict()
        #* if source params are not in folder use default params fron template
        path = os.path.join(
            os.getcwd(),
            self.SOURCE_PARAMS
        )
        try:
            self.file_checker(path)
        except FileNotFoundError:
            path = self._template_path(self.SOURCE_PARAMS)

        with open(path, "r") as f:
            sp = list(map(lambda x: x.strip().replace(" ", ""), f.readlines()))
        
        for i in sp:
            k,v = i.split("=")
            kv[k] = v 
        
        return kv

    @staticmethod
    def file_checker(path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError

    @staticmethod
    def read_json(file):
        with open(file) as f:
            return json.loads(f.read())
    
    @staticmethod
    def write_json(file, file_name="out.json"):
        with open(file_name, "w+") as f:
            return f.write(json.dumps(file, indent=4))

    
#* to write source directly from chain 
#* Preprocessing -> Fit -> Write (so do not save to db)
#* can be applied only for discrete energetic distr
class PlainPhitsSourceWriter(SourceWriter):
    params_order: str | None = "ASWE"
    
    def __init__(
        self,
        #* config injection required in order to get energy distr params
        source_params: T,
        groups: list | None,
        config: dict,
        #* if order is not given accepts source_params as a dict
        source_template:str = "poly_laplace",        
    ) -> None:
        super().__init__(source_template, config)
        self.groups = groups
        self.monoenergy:bool = True \
           if source_template == "mono"\
          else False 
        
        self.source_params: V = self._source_params_refactorer(source_params)

    def make_json(
        self, 
        func_key: str  = "AF",
        func_name: str = "laplace",
        params_key: str = "AP"
    ) -> None:
        
        '''
        #* Creates .json file that will be used
        #* to add source data to db
        #* It's intermediate step between preprocessing-fitting
        #* and adding final version to db
        #* At current step .json fullfills with function name
        #* (angular/energetic) and it's params
        #* Parameters
        #* ----------
        #* func_key: str
        #*  
        #* func_name:: str
        #*  
        #* params_key:: str
        #*  
        #* Returns
        #* ----------
        #* None
        '''
        #todo add exception to trigger if there are any None
        func_key = self._get_key_word(func_key)
        func_name = self.config.get("fit").get("ff").get(func_name)
        params_key = self._get_key_word(params_key)


        template = self._template_path("add.json") #* better to be defined as init param
        #! not as clear as should
        #todo create method - loads_json

        #* load json

        jsn = self.read_json(template)        
        #* populate json
        jsn[func_key] = func_name
        jsn[params_key] = self.source_params

        self.write_json(jsn)


    def write(self, block: str) -> None:
        '''
        #* Write a datablock to a file
        #* If file exists appends to 
        #* Parameters
        #* ----------
        #* block: str
        #* datablock to write
        
        '''
        with open("source", "a+") as f:
            f.write(block)

    # def _template_path(self, source_template):
    #     '''
    #     #* Method description
    #     #* Parameters
    #     #* ----------
    #     #*
    #     #* Raises
    #     #* ----------
    #     #*
    #     #* Returns
    #     #* ----------
    #     #*
    #     '''
    #     return os.path.join(
    #         os.path.split(
    #             os.path.split(os.path.abspath(__file__))[0]
    #         )[0],
    #         "templates",
    #         source_template
    #     )

    def _source_params_refactorer(self, source_params: T) -> V:
        
        '''
        #! update description
        #* Refactors array of params 
        #* from [[params1], [params2], ... paramnsN]] 
        #* to {n1 : {param_key1: param1, param_key1: param2} ...}
        #* n1 - stands for index of N-th array <[paramsN]>
        #* dict datatype will be unpacked to string Template
        #* Parameters
        #* ----------
        #* source_params: T, positional
        #*  the 2D array of parameters whick order assotiates with params_order var
        #* params_order: str, positional
        #*  order of params to use as a keys of dict (default: "ASE")
        #* Returns
        #* ----------
        #* dictionary with key, value pairs
        #* key is index [0, ... N], 
        #* v is dict of params {A: val, S: val, W: val, E: val} - mono
        #* v is dict of params {A: val, S: val, W: val, E1: val, E2: val} - poly 
        #* keys of v are from a given order
        '''
        #! e-type=1 approach must be implemented
        #! from E (average energy) need to get lower and 
        #! upper energies (as a delta between given energies)
        #! to use in e-type=1
        
        kv: dict = dict()
        k = list(self.params_order.upper())

        #! if groups are given
        if not self.monoenergy and self.groups: 
            #* if condition triggers
            #* replace and extends k "ASWE" to "ASWE1E2"
            Eind = k.index('E')  #* index of E letter
            source_params = self._get_boundaries(Eind, source_params)
            k = k[:Eind] + ["E1", "E2"] + k[Eind:]

        self._validate_source_params(source_params)

        for i in range(len(source_params)):
            kv[str(i)] = {}
            for n, j in enumerate(source_params[i]):
                kv[str(i)][k[n]] = self._str_fmt(j)
        print(kv)
        return kv

    def _validate_source_params(self, source_params: T) -> None:
        if len(source_params[0]) != len(self.params_order) and self.monoenergy:
            raise ValueError(
                "The lengths of source_params and params_order do not match",
                f"The length of params_order is {len(self.params_order)} when source_paramns has length of {len(source_params[0])}"
            )

        elif len(source_params[0]) == len(self.params_order) and not self.monoenergy:
            raise ValueError(
                "The lengths of source_params and params_order are match",
                f"The length of params_order is {len(self.params_order)} when for poly source the source_params length should be {len(self.params_order) - 1}"
            )
    
    def _get_boundaries(self, ind: int, source_params: T):
        '''
        #* Method description
        #* Parameters
        #* ----------
        #*
        #* Raises
        #* ----------
        #*
        #* Returns
        #* ----------
        #*
        '''
        for i in range(len(source_params)):
            source_params[i] = \
                source_params[i][:ind] + [self.groups[i], self.groups[i+1]]
        return source_params

    def _str_fmt(self, val: Any):
        return "{:.3f}".format(float(val))

    def _get_key_word(self, key: str) -> str:
        match key:
            case "AF":
                return "angular_function"
            case "AP":
                return "angular_params"
            case "EF":
                return "energetic_function"
            case "EP":
                return "energetic_params"


class StructuredSourceWriter(SourceWriter):
    
    def __init__(
        self,
        #* config injection required in order to get energy distr params
        source_params: V,
        #* stands for PolyContiniousEnergyLaplaceDistribution
        source_template:str = "pceld",
        energetic_params: dict | None = {}
    ):
        super().__init__(
            source_template
        )

        self.source_params = source_params
        #* adds energetic coeffs to default params
        self.default_source_params = { 
            **self.default_source_params,
            **energetic_params
        }

    