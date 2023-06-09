from core import db_connection
from . import *
from core.db import Cyclotrone



#* basic structure of database

population_test1 = {
    "name": "test1",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "13.6MeV",
    "groups": "28",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.061', 'S': '59.119', 'W': '0.118', 'E1': '0.500', 'E2': '1.000'}, 
            "1": {'A': '0.064', 'S': '54.668', 'W': '0.107', 'E1': '1.000', 'E2': '1.500'}, 
            "2": {'A': '0.069', 'S': '47.197', 'W': '0.099', 'E1': '1.500', 'E2': '2.000'}, 
            "3": {'A': '0.077', 'S': '40.463', 'W': '0.085', 'E1': '2.000', 'E2': '2.500'}, 
            "4": {'A': '0.085', 'S': '35.234', 'W': '0.070', 'E1': '2.500', 'E2': '3.000'}, 
            "5": {'A': '0.093', 'S': '30.995', 'W': '0.062', 'E1': '3.000', 'E2': '3.500'}, 
            "6": {'A': '0.100', 'S': '28.551', 'W': '0.056', 'E1': '3.500', 'E2': '4.000'}, 
            "7": {'A': '0.111', 'S': '25.058', 'W': '0.051', 'E1': '4.000', 'E2': '4.500'}, 
            "8": {'A': '0.119', 'S': '23.252', 'W': '0.044', 'E1': '4.500', 'E2': '5.000'}, 
            "9": {'A': '0.124', 'S': '22.252', 'W': '0.038', 'E1': '5.000', 'E2': '5.500'}, 
            "10": {'A': '0.127', 'S': '21.640', 'W': '0.033', 'E1': '5.500', 'E2': '6.000'}, 
            "11": {'A': '0.132', 'S': '20.840', 'W': '0.029', 'E1': '6.000', 'E2': '6.500'}, 
            "12": {'A': '0.136', 'S': '20.084', 'W': '0.025', 'E1': '6.500', 'E2': '7.000'}, 
            "13": {'A': '0.137', 'S': '19.925', 'W': '0.022', 'E1': '7.000', 'E2': '7.500'}, 
            "14": {'A': '0.136', 'S': '20.155', 'W': '0.020', 'E1': '7.500', 'E2': '8.000'}, 
            "15": {'A': '0.134', 'S': '20.343', 'W': '0.018', 'E1': '8.000', 'E2': '8.500'}, 
            "16": {'A': '0.131', 'S': '20.700', 'W': '0.017', 'E1': '8.500', 'E2': '9.000'}, 
            "17": {'A': '0.125', 'S': '21.899', 'W': '0.016', 'E1': '9.000', 'E2': '9.500'}, 
            "18": {'A': '0.127', 'S': '21.506', 'W': '0.015', 'E1': '9.500', 'E2': '10.000'}, 
            "19": {'A': '0.126', 'S': '21.805', 'W': '0.014', 'E1': '10.000', 'E2': '10.500'}, 
            "20": {'A': '0.126', 'S': '22.147', 'W': '0.013', 'E1': '10.500', 'E2': '11.000'}, 
            "21": {'A': '0.132', 'S': '20.954', 'W': '0.011', 'E1': '11.000', 'E2': '11.500'}, 
            "22": {'A': '0.131', 'S': '21.193', 'W': '0.009', 'E1': '11.500', 'E2': '12.000'}, 
            "23": {'A': '0.114', 'S': '24.857', 'W': '0.007', 'E1': '12.000', 'E2': '12.500'}, 
            "24": {'A': '0.113', 'S': '25.031', 'W': '0.006', 'E1': '12.500', 'E2': '13.000'}, 
            "25": {'A': '0.073', 'S': '45.139', 'W': '0.005', 'E1': '13.000', 'E2': '13.500'}, 
            "26": {'A': '0.075', 'S': '43.742', 'W': '0.005', 'E1': '13.500', 'E2': '14.000'}, 
            "27": {'A': '0.079', 'S': '41.449', 'W': '0.005', 'E1': '14.000', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test2 = {
    "name": "test2",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test3 = {
    "name": "test3",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "4mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test4 = {
    "name": "test4",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "3mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test5 = {
    "name": "test5",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Li",
    "thick": "5mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test6 = {
    "name": "test6",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "11MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test7 = {
    "name": "test7",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "15MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "watt",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "0.104"
        }
}

population_test8 = {
    "name": "test8",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "maxwell",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "1"
        }
}

insert_test = {
    "name": "test7",
    "source_type": "cyclotrone",
    "particle" : "deutron",
    "target": "Be",
    "thick": "5mm",
    "beam": "13.6MeV",
    "groups": "14",
    "template": "pceld",
    "angular_function": "laplace",
    "angular_params":
        {
            "0": {'A': '0.187', 'S': '56.718', 'W': '0.221', 'E1': '0.500', 'E2': '1.500'},
            "1": {'A': '0.218', 'S': '43.907', 'W': '0.182', 'E1': '1.500', 'E2': '2.500'},
            "2": {'A': '0.265', 'S': '33.377', 'W': '0.131', 'E1': '2.500', 'E2': '3.500'},
            "3": {'A': '0.313', 'S': '27.149', 'W': '0.107', 'E1': '3.500', 'E2': '4.500'},
            "4": {'A': '0.361', 'S': '23.012', 'W': '0.083', 'E1': '4.500', 'E2': '5.500'},
            "5": {'A': '0.382', 'S': '21.706', 'W': '0.063', 'E1': '5.500', 'E2': '6.500'},
            "6": {'A': '0.403', 'S': '20.470', 'W': '0.049', 'E1': '6.500', 'E2': '7.500'},
            "7": {'A': '0.402', 'S': '20.517', 'W': '0.039', 'E1': '7.500', 'E2': '8.500'},
            "8": {'A': '0.381', 'S': '21.689', 'W': '0.033', 'E1': '8.500', 'E2': '9.500'}, 
            "9": {'A': '0.368', 'S': '22.745', 'W': '0.029', 'E1': '9.500', 'E2': '10.500'}, 
            "10": {'A': '0.376', 'S': '22.431', 'W': '0.024', 'E1': '10.500', 'E2': '11.500'},
            "11": {'A': '0.357', 'S': '23.782', 'W': '0.017', 'E1': '11.500', 'E2': '12.500'}, 
            "12": {'A': '0.277', 'S': '32.615', 'W': '0.012', 'E1': '12.500', 'E2': '13.500'}, 
            "13": {'A': '0.239', 'S': '40.368', 'W': '0.010', 'E1': '13.500', 'E2': '14.500'}
    },
    "energetic_function": "maxwell",
    "energetic_params" :
        {
            "a": "2.488", "b": "0.788", "c": "1"
        }
}

delete_test = "test7"

@pytest.fixture
def test_coln():
    return db_connection().test_ns.test_cln

def test_insert(test_coln):
    test_coln.insert_many(
        [
            population_test1, population_test2, population_test3,
            population_test4, population_test5, population_test6,
            population_test7, population_test8
        ]
    )
    assert 0

def test_query(test_coln):
    res = test_coln.find({"source_type": "cyclotrone"})
    print(next(res)["target"])
    assert 0
def test_delete(test_coln):
    test_coln.delete_one({"thick":"5mm"})

@pytest.fixture
def cyclotrone():
    return Cyclotrone(db_connection())

def test_cycl_fetch(cyclotrone):
    cyclotrone.fetch({"target": "Be"})
    assert 0

def test_get_all_names(cyclotrone):
    assert \
    ['test1', 'test2', 'test3', 'test4', 'test5', 'test6', 'test7', 'test8']\
    == cyclotrone.get_all_names()

def test_get_source(cyclotrone):
    assert "test7" == cyclotrone.get_source("test7")["name"]

def test_insert(cyclotrone):
    res = cyclotrone.insert(insert_test)
    print(res)
    assert 0

def test_update(cyclotrone):
    name = "test7"
    upd = {
        "$set":{
            "thick": "5mm"
        }
    }

    res = cyclotrone.update(name, upd)
    print(res)
    assert "55mm" == cyclotrone.get_source("test7")["thick"]

def test_delete(cyclotrone):
    res = cyclotrone.delete(delete_test)
    print(res)
    assert 0





    