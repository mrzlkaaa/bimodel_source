import subprocess
import re
import inspect
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from .preprocessing import Preprocessor




class Prompt:
    print(
    "\
    Welcome to PHITSNeutronSourceTool\n\
    The tool main purpose is to build a source file\n\
    upon angle distributions fitted to a particular fitting functions\n\
    to use in your PHITS code\
    ")
    d = {
        "X": "X_col_name",
        "dud": "dud",
        "Z": "zero_centered",
        "R": "range_"
    }
    def __init__(self):
        self.ps = PromptSession()

    def run(self):
        res = subprocess.run(["ls"], capture_output=True)
        res = str(res.stdout.decode("utf-8")).split("\n")
        wc = WordCompleter(res)
        
        input_ = self.ps.prompt("Provide name of excel file: ",
        completer=wc)
        isprep = self.ps.prompt("Is preprocessing of input required?: ")
        if isprep == "yes" or isprep == "Y" or isprep == "y":
            print("""
            * Parameters
            * ---------
            * X_col_name : str, positional
            *   X axis of data    
            *   -X=X_col_name
            *
            * range_: tuple, positional
            *   indicates the range of data (min, max values)
            *   -R=range_
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
            * scale: bool, optional
            *   scale a given column by a max value
            *   -S=scale
            *
            * zero_centered: bool, optional, default: True
            *   helper to normalize and zero center X axis
            *   -Z=zero_centered
            """)

            prep_flags = self.ps.prompt("")
            kv=self._parse_flags(prep_flags)
            print(Preprocessor.read_excel(input_).mirror_angular_data(**kv))

    def _parse_flags(self, line: str):
        rigth_part = r"[A-Za-z0-9_[\](\)',]+"
        pattern = rf"[a-z_]+={rigth_part}|[A-Z]+={rigth_part}"
        kv = {
            self.convert_flag(i.split("=")[0]): i.split("=")[-1] 
            for i in re.findall(pattern, line)
            if self.validate_flag(i.split("=")[0]) 
        }
        print(kv)

    def convert_flag(self, flag):
        return self.d.get(flag)

    def validate_flag(self, flag):
        if self.d.get(flag) is None:
            raise KeyError(f"Given flag <{flag}> does not exist")
        return True

    # def _parse_to_key_value(self, arr:str):
    #     kv = dict()
    #     pattern = r""
    #     # for i in arr:



if __name__ == "__main__":
    Prompt().run()
