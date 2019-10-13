import _global
_global._import()

import sys
from pysms import Sms
from pygsm.errors import GsmError, GsmConnectError, GsmModemError, GsmWriteError

try:
    sms = Sms("/dev/ttyUSB0", logger = True)
    responce = sms.sendSms({
        "phone": sys.argv[1], 
        "message": sys.argv[2]
    })
    print(responce)
except GsmConnectError as err:
    print ("connect error", err)
except GsmModemError as err:
    print ("modem error", err)
except GsmWriteError as err:
    print ("write error", err)
except GsmError as err:
    print ("error", err)
except IndexError as err:
    print ("Phone number and message are required")
