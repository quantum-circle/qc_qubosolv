from cryptography.utils import CryptographyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from qc_qubosolv.solver import Solver