import _global
_global._import()

import sys, json
from pysms import Sms
from pygsm.errors import GsmError, GsmConnectError, GsmModemError, GsmWriteError

try:
    sms = Sms("/dev/ttyUSB0", logger = True)
    if sys.argv[1] == "inbox": 
        responce = sms.inbox("ME")
    elif sys.argv[1] == "outbox": 
        responce = sms.outbox()
    elif sys.argv[1] == "sent": 
        responce = sms.sent()
    elif sys.argv[1] == "fiald": 
        responce = sms.faildMessages()
    elif sys.argv[1] == "new": 
        responce = sms.newMessages()
    elif sys.argv[1] == "seen": 
        responce = sms.seen()
    else: 
        responce = sms.storedSms()

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
