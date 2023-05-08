from abc import abstractmethod
from typing import List, Union, Dict, TypeVar, Callable
import subprocess
import re
import inspect
from weakref import CallableProxyType
import prompt_toolkit


from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, checkboxlist_dialog
from prompt_toolkit.styles import Style


from . import config, questions, db_connection, load_dotenv
from .preprocessing import Preprocessor
from .fit import Fit
from .db import Cyclotrone
from .writer import PlainPhitsSourceWriter, SourceWriter, StructuredSourceWriter

import fire
import pprint

load_dotenv()

style = Style.from_dict({
        'dialog': 'bg:#a9cfd0',
        'dialog.body': 'bg:#a9cfd0',
        'frame.label': '#000000',
})

ConvertedValue = TypeVar("ConvertedValue", str, bool, list)
Config = TypeVar("Config", bound=Dict[str, Union[str, list, bool]])

class PromptInterface(object):
    #* module to call and initiate CLI
    def __init__(
        self, 
        config: Config,
        questions: dict,
        collection: str = "cyclotrone"
    ) -> None:

        self.i = Inquirer(config, questions, collection)
        self.c = Commands(config, collection)


class Prompt:
    # print(
    # "\
    # Welcome to PHITSNeutronSourceTool builder\n\
    # The tool main purpose is to build a source file\n\
    # upon angle distributions fitted to a particular fitting functions\n\
    # to use in your PHITS code\
    # ")
    def __init__(
        self,
        config: Config,
        collection: str = "cyclotrone"
    ) -> None:
        self.source = collection
        self.collection = self._initialize(collection)
        self.ps = PromptSession()
        self.config = config  #* injected config

    def _initialize(self, source):
        match source:
            case "cyclotrone":
                return Cyclotrone(db_connection()) #! not good practice

class Commands(Prompt):

    def __init__(
        self,
        config: Config,
        collection: str = "cyclotrone"
    ) -> None:
        super().__init__(config, collection)
        
    
    def add_source(self):
        '''
        #* Checks the .json file
        #* if the file exists, all required fields filled
        #* after check passed calls db method
        #* to add data to db
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
        file = "to_add.json" #! hardcoded

        SourceWriter.file_checker(file)
        res = self.collection.insert(SourceWriter.read_json(file))
        print(res)

    
    def get_source(self, name: str, out:bool=True) -> None:
        res = self.collection.get_source(name)
        pprint.pprint(res)

        if out:
            StructuredSourceWriter(
                source_params=res["angular_params"],
                energetic_params=res["energetic_params"]
            ).fit_to_template()

        

    def update_source(self, name: str):
        '''
        #* updates existing source
        #* use <name> as a query specifing doc to update
        #* loads .json file, checks fields
        #* if there are any empty fields drops it
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
        file = "to_upd.json" #! hardcoded
        SourceWriter.file_checker(file)
        res = self.collection.update(name, SourceWriter.read_json(file))
        print(res)

    def get_sources_names(self):
        res = self.collection.get_all_names()
        print(res)

    def delete_source(self, name:str):
        res = self.collection.delete(name)
        print(res)


class Inquirer(Prompt):
    def __init__(
        self,
        config: dict,
        questions: dict,
        collection: str = "cyclotrone"
        
    ) -> None:
        super().__init__(config, collection)
        self.ps = PromptSession()
        self.questions: dict = questions
        self.querys_chain: dict = {}
   
    #* new source data
    #! uses only for sequences: preprocessing, fitting, writing
    #todo modify to dialogs
    def new_source_data(self) -> None:
        res = subprocess.run(["ls"], capture_output=True)
        res = str(res.stdout.decode("utf-8")).split("\n")
        wc_ls = WordCompleter(res)
        wc_flags = WordCompleter(list(self.config.get("prompt").get("flag").keys()))
        
        input_ = self.ps.prompt("Provide name of excel file: ",
        completer=wc_ls)

        # isprep = self.ps.prompt("Is preprocessing of input required?: ")
        # if isprep == "yes" or isprep == "Y" or isprep == "y":
        print("""
        * Flags
        * ---------
        * X_col_name : str, positional
        *   X axis of data    
        *   -X=X_col_name
        *
        *
        * cos: bool, optional
        *   stands for is angular data is in units of cos
        *   --cos=cos
        *
        * dsd: Union[tuple, None]=("_", None), optional
        *   drop_secondary_data where the tuple is (key, ignore) params
        *   --dsd=dsd
        *
        * dud: Union[List[str], None]=None, optional
        *   drop_unused_data takes array of str as a columns name to drop
        *   --dud=dud
        *
            """)

        prep_flags = self.ps.prompt(
            "Provide flags for preprocessing tool:\n> ",
            completer=wc_flags
        )
        kv_prep = self._parse_flags(prep_flags)
        pp_df, width, weigths, groups = \
            Preprocessor.read_excel(input_).angular_data(**kv_prep)
        print("File successfully processed")
        print(pp_df)
        print("""\
            * Flags
            * ---------
            * X_col_name: str, positional
            *   variable indicates the X axis column
                -X=X_col_name
            * ff: str
            *  name of fitting function in a string format
            """
        )

        #* new flags will be avaliable:
        #*    width: float
        df_fit_flags = self.ps.prompt(
            "Provide flags for fitting tool:\n> ",
            completer=wc_flags)
        kv_fit = self._parse_flags(df_fit_flags)
        coeffs, fitted = Fit(
            pp_df, self.config.get("fit"), kv_fit["ff"]
        ).df_fit(
            kv_fit["X_col_name"],
            width=width,
            weights=weigths)
        
        PlainPhitsSourceWriter(
            source_params=coeffs, 
            groups=groups, 
            config=self.config
        ).make_json()
   

    #! manual
    #! under dev
    def make_source(self) -> None:

        '''
        #* <Back> navigation has not been implemented yet
        #* method uses to create a source file by sequantially
        #* picking the params of the source
        #* when questioning finished fetches source data
        #* by query and writes a file
        #* Parameters
        #* ----------
        #* -
        #* Raises
        #* ----------
        #* KeyError
        #*  when there are no matches in config file - finish of questioning
        #* Returns
        #* ----------
        #* None
        '''
        res: list | str | None = None
        run: bool = True
        q_counter: int = 1

        while run:
            try:
                q = self._key_maker(q_counter)
                name = f"{q}{self.source}"
                #* do fetch
                q_values = self._get_values(name, res)
                self._fill_questions(name, q_values)
                dialog = self._get_dialog_type(self.questions[f"{name}_details"]["type"])
                
                res = self.run_dialog(dialog, self.questions[name])
            
                print(res)

                q_counter += 1  #* increment to get next question
            
            #todo when back navigation used pop last added key
            except KeyError: #* when no more questions exist
                run = False
                q_counter -= 1 #* decrement to get last valid question
                q = self._key_maker(q_counter)
                name = f"{q}{self.source}"

                self.querys_chain[self.questions[f"{name}_details"]["key"]] = res
                
        source_params = self._get_source_params() #* fetch

        #todo final source file consists of bunch of paramters 
        #todo among which are x,y,z
        #todo Writer must include functionality to handle default and custom
        #todo parameters when makes a phits source file

        StructuredSourceWriter(
            source_params=source_params["angular_params"],
            energetic_params=source_params["energetic_params"]

        ).fit_to_template()

    def run_dialog(self, dialog: Callable, q:dict):
        print(q)
        return dialog(**q).run()

    def convert_flag(self, flag:str) -> str:
        '''
        #* convert given flag to variable according to config
        #* Parameters
        #* ----------
        #* flag: str, positional
        #*  flag string to convert into string name of variable
        #* Returns
        #* ----------
        #*  string name of variable from config file
        '''
        return self.config.get("prompt").get("flag").get(flag)

    def convert_dtype(
        self,
        flag: str, 
        val:str
    ) -> ConvertedValue:
        """
        #* converts flag values from string 
        #* to dtype according to config file
        #* Parameters:
        #* -----------
        #* flag: str, positional
        #*  flag name to fetch dtype from config
        #* val: str, positional
        #*  flag value to convert to dtype
        #* Returns:
        #* -----------
        #* ConvertedValue
        #*  converted value that assotiates with flag dtype
        """
        val_type = eval(self.config.get("prompt").get("dtype").get(flag)) #* use eval method to get explicit class object
        if val_type == bool:
            return self._bool_conversion(val)
        elif val_type == list:
            return val.replace(" ", "").split(",")
        else:
            return val_type(val)

    def validate_flag(self, flag:str) -> bool:
        '''
        #* flag validtion method to validate 
        #* wether given flag written correct
        #* Parameters
        #* ----------
        #* flag: str, positional
        #*  used to validate given flag 
        #* Raises
        #* ----------
        #* KeyError
        #*  If given name does not exists in config file
        #* Returns
        #* ----------
        #* True that indicates that flag validated
        '''
        if self.config.get("prompt").get("flag").get(flag) is None:
            raise KeyError(f"Given flag <{flag}> does not exist")
        return True

    def _parse_flags(
        self, 
        line: str
    ) -> Dict["str", ConvertedValue]:
        """
        #* accepts a string with flag=value pattern
        #* find and extract flag, value pair
        #* validates flag by compare with config file data
        #* if flag validated converts it to variable string 
        #* converts value to value of flag dtype
        #* Parameters
        #* ----------
        #* line: str, positional
        #*  string from input with flag and its value
        #* Returns
        #* ----------
        #* kv: dict
        #*  dictionary consists of key: value that stands
        #*  for validated and converted flag (variable) and its value
        """
        rigth_part = r"[A-Za-z0-9_[\](\)',]+"
        pattern = rf"[a-z_]+={rigth_part}|[A-Z]+={rigth_part}"
        kv: dict = {}

        for i in re.findall(pattern, line):
            key, val = i.split("=")
            if self.validate_flag(key):
                key = self.convert_flag(key)
                val = self.convert_dtype(key, val)
                kv[key] = val
        return kv
            
    

    def _bool_conversion(self, string:str) -> bool:
        '''
        #* converts given strings literal to bool type
        #* Parameters
        #* ----------
        #* string: str, positional
        #* Raises
        #* ----------
        #* ValueError
        #*  If given literal does not match any conditions
        #* Returns
        #* ----------
        #* True or False of boolean type
        '''
        string = string.upper()
        if string == "TRUE" or string == "T":
            return True
        elif string == "FALSE" or string == "F":
            return False
        else:
            raise ValueError(
                "Given string do not assotiates either with True or False"
            )

    def _get_values(
        self, 
        name: str, 
        res: list | str | None
    ) -> list:
        '''
        #* dialog values constructor
        #* the aim of method is to get values for new dialog
        #* all values are taken from db 
        #* Parameters
        #* ----------
        #* name: str
        #*  name of question (Q1cyclotrone)
        #* res: list | str | None
        #*  result (value picked) from previous question
        #* Raises
        #* ----------
        #* ValueError
        #*  if no result found
        #* Returns
        #* ----------
        #* list of values to use in dialog
        '''
        query_key = list(self.questions[f"{name}_details"]["query"].keys())[0]
        if res is not None:
            #* fill query key from .json to to make rigth fetch 
            self.questions[f"{name}_details"]["query"][query_key] = res 

        fetch = self.collection.fetch(
            {
                **self.querys_chain,
                **self.questions[f"{name}_details"]["query"]
            }
        )
        if fetch is None:
            raise ValueError("No results found for a given query")
        #* add to querys chain to save query history
        self.querys_chain[query_key] = self.questions[f"{name}_details"]["query"][query_key]
        
        values = [  
            v for i in fetch
            for k, v in i.items()
            if k == self.questions[f"{name}_details"]["key"]
        ]
        return list(set(values))

    def _fill_questions(self, key, values):
        tuple_values: list = []
        for i in range(len(values)):
            tuple_values.append((values[i], values[i]))

        self.questions[key]["values"] = tuple_values


    def _get_source_params(self):
        '''
        #* final fetch to get source params
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
        res = self.collection.fetch(self.querys_chain) #* fetch by query
        source: dict = {}
        for n, i in enumerate(res):
            if n > 0:
                raise("There are more than 1 source with a given query")
            #! a bit of hardcode
            source["angular_params"] = i["angular_params"]
            source["energetic_params"] = i["energetic_params"]
        return source

    def _get_dialog_type(self, name:str) -> Callable:
        '''
        #* dialog type definer
        #* accepts str and look up for match
        #* returns method to call
        #* Parameters
        #* ----------
        #* name: str
        #*  name of dialog to get attr and return method
        #* Returns
        #* ----------
        #* method (callable)
        '''
        match name:
            case "radio":
               return getattr(prompt_toolkit.shortcuts, "radiolist_dialog")
            case "checkbox":
               return getattr(prompt_toolkit.shortcuts, "checkboxlist_dialog")

    def _key_maker(self, order:int):
        '''
        #* converts int value to str format
        #* Parameters
        #* ----------
        #* order: int
        #*  int value
        #* Returns
        #* ----------
        #* str value
        '''
        return f"Q{order}"


if __name__ == "__main__":
    fire.Fire(PromptInterface(config(), questions()))
