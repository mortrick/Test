import platform
from pathlib import Path
import utils as cnf

run_id = cnf.getrunid_str()

def logpath(runid):
    filename = "processlog1" + str(runid) + ".log"
    if platform.system() == 'Windows':
        logdir = Path('C:/Users/Davidy/Dropbox/Projects/CryptoAPI/logs/')
        path = logdir / filename
        return path
    else:
        logdir = Path('~/cryptoapi/Tracker/logs/')
        path = logdir / filename
        return path
