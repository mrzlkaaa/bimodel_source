import yaml
import os
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
import json

load_dotenv()

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config_file_path = os.path.join(
    #* binds the location of config file to __init__ location
    os.path.split(os.path.abspath(__file__))[0],
    #* move to .env to prevent safety issues
    "config.yaml"  
)

def config():
    with open(config_file_path, "r") as stream:
        config = yaml.load(stream, Loader=Loader)
    return config

#! add db initialization

def db_connection():
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    DB = os.environ.get("DB")

    cn = MongoClient(f"mongodb://{HOST}:{PORT}/")[DB]

    return cn

def questions():
    with open(
        os.path.join(
            os.path.dirname(__file__),
            "source_questions.json"
        )
    ) as f:
        return json.loads(f.read())
    
    
