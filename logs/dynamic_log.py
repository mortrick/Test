import platform

def logpath():
    if platform.system() == 'Windows':
        logdir = 'C:\\Users\Davidy\Dropbox\Projects\CryptoAPI\logs'
    else:
        logdir = '/home/ubuntu/cryptoapi/Tracker/logs'
    return logdir

