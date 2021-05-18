import os
import sys
import json
from pathlib import Path

import numpy as np
from keycloak.keycloak_openid import KeycloakOpenID

import qc_qubosolv
from qc_qubosolv import qc_qubosolv_api
from qc_qubosolv.qc_qubosolv_api.rest import ApiException



_DEFAULT_temp_start = 5
_DEFAULT_temp_end = 0.1
_DEFAULT_tau = 0.9999
_DEFAULT_beta = 0.02
_DEFAULT_maximize = False
_DEFAULT_algorithm = None



def bs_to_array(bs):
    """Convert bitstring bs (str) to numpy.ndarray of int8."""
    return np.array([int(x) for x in bs], dtype="int8")



class SolverResult:
    def __init__(self, response, offset):
        self._response = response
        self.optimal_bitstring = np.array([int(x) for x in self._response['opt_bitstring']])
        self.energies = np.array(self._response['energies']) + offset
        self.bitstrings = np.array([bs_to_array(bs) for bs in self._response['bitstrings']])
        self.optimal_energy = self._response["opt_energy"] + offset
        self.duration = self._response['duration']
        self.solver_config = self._response['solver_config']
        
        
    def __repr__(self):
        return f"SolverResult({self.optimal_energy})"



class Solver:
    """Quantum-Cirlce Annealer
    """
    SERVER_URL = "https://keycloak.quantum-circle.com/auth/"
    CLIENT_ID = "quantum-client"
    REALM_NAME = "quantum"
    
    def __init__(self, username=None, password=None, file=None, token=None):
        """Quantum-Cirlce Annealer

        First Time using the Solver username and password are needed. Afterwards they will be
        saved in the package directory, such that the credential are not needed anymore.

        Parameters
        ----------
        username : string
            username for the developer portal
        password : string
            password for the corresponding username
        file : string, optional
            file, where to save the credentials (username and password). By default it will be saved
            in the package directory
        token : string, optional
            token, which can be obtained from the developer portal, by default None

        Raises
        ------
        ValueError
            If username and/or password is not given
        """
        FILE_NAME = 'client_secrets.json'
        
        self.response = None
        self.keycloak_openid = KeycloakOpenID(
            server_url=self.SERVER_URL,
            client_id=self.CLIENT_ID,
            realm_name=self.REALM_NAME,
        )
        # Get WellKnow
        self.config_well_know = self.keycloak_openid.well_know()
        #check file
        if file is not None:
            if Path(file).is_dir():
                file += "client_secrets.json"
            if not str(file).endswith('.json'):
                file += '.json'
        else:
            file = Path(qc_qubosolv.__file__.rsplit('/', 1)[0] + '/' + FILE_NAME)
        #check username and password
        if username is not None and password is not None:
            if Path(file).exists():
                with open(file) as config_file:
                    data = json.load(config_file)
                    data['username'] = username
                    data['password'] = password
                with open(file, 'w') as config_file:
                    json.dump(data, config_file, indent = 4)
            else:
                with open(Path(file), 'w') as config_file:
                    account = {
                        'username': username,
                        'password': password
                    }
                    json.dump(account, config_file, indent = 4)
        elif username is None and password is None:
            if not Path(file).exists():
                raise ValueError("File does not exist and username/password is not given")
            else:
                pass
        elif username is None or password is None:
            raise ValueError("Only Username or Password is given, but both are needed")
        
        # load token or username/password
        if token is not None:
            self.configuration = qc_qubosolv_api.Configuration()
            self.configuration.access_token = token
        else:
            with open(Path(file)) as config_file:
                data = json.load(config_file)
            try:
                response_token = self.keycloak_openid.token(
                    data['username'],
                    data['password']
                )
            except KeyError:
                raise ValueError(
                    "username and password is not saved, therefore token "
                    "cannot be generated or token is not given"
                )
            self.configuration = qc_qubosolv_api.Configuration()
            self.configuration.access_token = response_token["access_token"]

        

    def solve(self, matrix, offset=0, temp_start=_DEFAULT_temp_start,
              temp_end=_DEFAULT_temp_end, tau=_DEFAULT_tau, beta=_DEFAULT_beta,
              maximize=_DEFAULT_maximize, algorithm=_DEFAULT_algorithm):
        """
        Solves a QUBO matrix with the Main Incubator Annealer.

        Parameters
        ----------
        matrix : list
            must be either symmetric or uppertriangular matrix
        offset : int or float
            constant or offset factor of the QUBO
        temp_start : int or float
            is the start temperature, by default 5
        temp_end : int or float
            is the end temperature by default 0.001
        tau : int or float
            is the stepwidth of decreasing temperature, where the
            temperature is changed with Temp_new = tau * Temp, by default 0.9999
        beta : int or float
            influences the acceptance probability, which is exp(-dE*beta),
            by default 0.02
        maximize : boolean
            maximize or minimize the energy function, by default False
        algorithm : str
            'bf' for bruteforce solver, 'sa' for simulated annealing or
            'sqa' for simulated quantum annealing

        Returns
        -------
        SolverResult
            an object containing the result
        """
        self.api_instance = qc_qubosolv_api.ProblemApi(
            qc_qubosolv_api.ApiClient(self.configuration)
        )
        self.body = qc_qubosolv_api.Task()

        if isinstance(matrix, np.ndarray):
            self.body.matrix = matrix.tolist()
        else:
            self.body.matrix = matrix

        self.body.parameter = qc_qubosolv_api.Parameter()
        self.body.parameter.temp_start = temp_start
        self.body.parameter.temp_end = temp_end
        self.body.parameter.tau = tau
        self.body.parameter.beta = beta
        self.body.parameter.maximize = maximize
        self.body.parameter.algorithm = algorithm
        response_json = self.api_instance.task_post(self.body)
        self.response = SolverResult(json.loads(response_json), offset)
        return self.response
