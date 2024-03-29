#!/usr/bin/env python

import os, sys

sys.path.append(os.getcwd()+"/../pygsm")

from pygsm.gsmmodem import GsmModem

import re

class Sms: 
    gsm = None
    logger = ""

    def __init__(self, port, logger = False): 
        self.logger = logger
        if(logger):
            self.gsm = GsmModem(port = port, logger = GsmModem.debug_logger).boot()
        else:
            self.gsm = GsmModem(port = port).boot(); 

    def _decode(self, text):
        try:
            return text.replace("\"","").decode("hex").replace("\x00", "")
        except Exception:
            return text
        
    def _compose(self, msg, properties = ["id", "status", "phone", "x"]):
        date_pattern = re.compile(r'\d\d/\d\d/\d\d,\d\d:\d\d:\d\d\+\d\d').search(msg)
        date = ""

        if date_pattern: 
            date = date_pattern.group()

        message = msg.split(",")
        if self.logger == GsmModem.debug_logger: 
            print("")
            print("messages")
            print("===============================")
            print(message)
            print("===============================")
        if(self.gsm.query("AT+CMGF?")[-1] == 0):
            print("encoded")
            obj = {properties[i]: self._decode(message[i]) for i in range(0, len(properties))  }
        else:
            obj = {properties[i]: message[i] for i in range(0, len(properties))  }
        obj["date"] = date
        obj["status"] = re.compile(r'"\w+\s?\w+"').search(obj["status"]).group().replace("\"","")
        
        return obj

    def storedSms(self, filter, _from="SM"):
        self.gsm.command("AT+CPMS=\"" + _from + "\",\"" + _from + "\",\"" + _from + "\"")
        self.gsm.command("AT+CMGF=1")

        print("AT+CMGL=\"" + filter + "\"")

        messages = self.gsm.query_list("AT+CMGL=\"" + filter + "\""); 
        message_objs = []; 
        if self.logger == GsmModem.debug_logger:
            print("*************************")
            for msg in messages: 
                print(msg)
            print("*************************")
        for msg in messages:
            message = msg.split(",")
            if(len(message) != 1): 
                obj = self._compose(msg)
            else:
                message_objs[-1]["message"] = self._decode(message[0])

            message_objs.append(obj)
            
        return message_objs
    
    def getMessage(self, id, _from="SM"): 
        self.gsm.command("AT+CPMS=\"" + _from + "\",\"" + _from + "\",\"" + _from + "\"")
        self.gsm.command("AT+CMGF=1")

        message = self.gsm.query_list("AT+CMGR=" + str(id))
        obj = self._compose(message[0], properties = ["status", "phone"])
        obj["message"] = self._decode(message[1])
        
        return obj
    
    def inbox(self, _from="SM"): 
        unseen = self.storedSms(filter = "REC UNREAD", _from= _from)
        seen = self.storedSms(filter = "REC READ", _from= _from)
        return unseen + seen 

    def outbox(self, _from="SM"): 
        unsent = self.storedSms(filter = "STO UNSENT", _from= _from)
        sent = self.storedSms(filter = "STO SENT", _from= _from)
        return unsent + sent

    def sent(self, _from="SM"): 
        sent = self.storedSms(filter = "STO SENT", _from= _from)
        return sent

    def newMessages(self, _from="SM"): 
        unseen = self.storedSms(filter = "REC UNREAD", _from= _from)
        return unseen
    
    def seen(self, _from="SM"): 
        unseen = self.storedSms(filter = "REC READ", _from= _from)
        return unseen

    def faildMessages(self, _from="SM"): 
        unsent = self.storedSms(filter = "STO UNSENT", _from= _from)
        return unsent
    
    def sendSms(self, message):      
        phone_pattern = re.compile(r'^\+\d{12}$')

        if(message["phone"][0] == "0"): 
            message["phone"] = "+251" + message["phone"][1:len(message["phone"])]
        message["phone"] = message["phone"].encode("ascii")
 
        if(len(message["message"]) > 160): 
            raise Exception("Message is too long"+str(len( message["message"]))+", the messasage should not be graterthan 160 characters")
        elif(not phone_pattern.search(message["phone"])): 
            raise Exception("The phone number is invalid")
        else:
            self.gsm.wait_for_network()
            return self.gsm.send_sms(message["phone"], message["message"])

    def sendSmses(self, messages):
        print(">>>>")
        phone_pattern = re.compile(r'^\+\d{12}$')
        self.gsm.command("AT+CMGF=1")
        faild_sms = []

        for msg in messages: 
            try:      
                if self.sendSms(msg) == None: 
                    faild_sms.append(msg)
            except Exception as e:
                print(e)
                faild_sms.append(msg)
                
        return faild_sms
    