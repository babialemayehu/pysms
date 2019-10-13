import _global
_global._import()

import sys, json
from pysms import Sms
from pygsm.errors import GsmError, GsmConnectError, GsmModemError, GsmWriteError

try:
    sms = Sms("/dev/ttyUSB0", logger = True)
    messages = json.loads(sys.argv[1]); 
    responce = sms.sendSmses(messages)
    print(json.dumps(responce))
except GsmConnectError as err:
    print ("connect error", err)
except GsmModemError as err:
    print ("modem error", err)
except GsmWriteError as err:
    print ("write error", err)
except GsmError as err:
    print ("error", err)
except IndexError as err:
    print ("Phone number and message list are required")
