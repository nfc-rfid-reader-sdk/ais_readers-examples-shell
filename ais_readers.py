'''
Created on Nov 8, 2015

@author: Vladan
'''
import os
import sys
import threading
import time
from platform import platform

from ctypes import *

from constants import *
from dl_status import *
from ais_readers_list import *
from ais_readers_list import E_CARD_ACTION




class log_t(Structure):
    _fields_ = [("index", c_int),    
    ("action",c_int),
    ("reader_id",c_int),
    ("card_id",c_int),
    ("system_id",c_int),
    ("nfc_uid",(c_uint8 * NFC_UID_MAX_LEN)),
    ("nfc_uid_len",c_int),
    ("timestamp",c_uint64)]
 
class device_t(Structure):
    _fields_ = [("hnd",c_void_p),
                ("status",c_long),
                ("RealTimeEvents",c_int),
                ("LogAvailable",c_int),
                ("cmdResponses",c_int),
                ("cmdPercent",c_int),
                ("TimeoutOccurred",c_int),
                ("Status",c_int),
                ("log",log_t)]
    

class PythonBB(threading.Thread):
  
    def __init__(self):
        self._mySO = self.GetPlatformLib()        
        self. DL_STATUS = c_long()
        self._HND_AIS = c_void_p()
        self.devCount = c_long()
        self.buff = c_long()
        #self.DEV_HND = POINTER(device_t)
        self.DEV_HND = device_t()
        self.obj = None
        self._pass = '1111'
    
#         t = threading.Thread(target=self.RTEListen).start()
#         t.daemon = True
#         t.start()
    
    def GetPlatformLib(self):
       
        if sys.platform.startswith("win32"):
            return windll.LoadLibrary(os.getcwd() + '\\lib\\' + CWIN32)
        elif sys.platform.startswith("linux"):
            return cdll.LoadLibrary(os.getcwd() + '//lib//' + CLINUX)
        elif platform().lower().find('armv7l-with-debian') > -1:
            return cdll.LoadLibrary(os.getcwd() + '//lib/' + CARMHF) #CARM

    
    
    def EraseAllDevicesForCheck(self):
        self._mySO.AIS_List_EraseAllDevicesForCheck()
        
        
    
    
    def GetDevicesForCheck(self):          
        myStr = c_char_p()
        myStr = self._mySO.AIS_List_GetDevicesForCheck()                        
        return string_at(myStr)
    
    
    
    def AddDeviceForCheck(self,devType,devId):            
        return self._mySO.AIS_List_AddDeviceForCheck(devType,devId)
    
    def UpdateAndGetCount(self):
          
        return self._mySO.AIS_List_UpdateAndGetCount()


    def GetListInformation(self):
         
        print("\n#AIS_List_GetInformation#") 
               
        devSerial      = c_char_p()
        devType        = c_int()
        devID          = c_int()
        devFW_VER      = c_int()
        devCommSpeed   = c_int()
        devFTDI_Serial = c_char_p()
        devOpened      = c_int()
        devStatus      = c_int()
        systemStatus   = c_int()
        mojFormat      = "{0:3d} | {1} | {2} | {3}  | {4}  | {5}  | {6} | {7} | {8:6d}  | {9:9d}  | {10} |"
        
         
        print("----!------------------+----------+----------+-----+-----++--------+----------++--------+-----------+-----------")
        print("indx|  Reader HANDLE   | SerialNm | Type h/d | ID  | FW  || speed  | FTDI: sn || opened | DevStatus | SysStatus") 
         
        #self.obj = [device_t() for i in range(0,self.devCount)]
         
        for i in range(0,self.devCount):                       
            self.DL_STATUS = self._mySO.AIS_List_GetInformation(byref(self._HND_AIS),byref(devSerial),byref(devType),byref(devID),
                                                                byref(devFW_VER),byref(devCommSpeed),
                                                                byref(devFTDI_Serial),byref(devOpened),byref(devStatus),
                                                                byref(systemStatus)
                                                                )
         
            #self.obj[i].hnd = self._HND_AIS.value #<--- probati ovako...??
            
                                         
                                          #self._HND_AIS.value  
            print(mojFormat . format( i+1,self._HND_AIS.value,devSerial.value.decode("utf-8"),devType.value,devID.value,
                                      devFW_VER.value,devCommSpeed.value,devFTDI_Serial.value.decode("utf-8"),devOpened.value,
                                      devStatus.value,
                                      systemStatus.value
                                    )
                  )
            
          

    
    def AISOpen(self):
        print("\n#AIS_Open#")
        self.DL_STATUS = self._mySO.AIS_Open(self._HND_AIS)
        return self.DL_STATUS
         
    def AISGetTime(self):
        print("\n#AIS_GeTTime#")
        currTime = c_uint64()
        self.DL_STATUS = self._mySO.AIS_GetTime(self._HND_AIS,byref(currTime))
        return currTime.value, '|' + time.ctime() 
      
    
    def PrintRTE(self):
  
        log_index     = c_int()
        log_action    = c_int()
        log_reader_id = c_int()
        log_card_id   = c_int()
        log_system_id = c_int()
        nfc_uid       = (c_uint8 * NFC_UID_MAX_LEN)()
        nfc_uid_len   = c_int()
        timestamp     = c_uint64() 
          
        print(self.ReadRTECount())
                
        print("= RTE Real Time Events = ")
#         print("-----+----------------------------------+-------+---------+-------+--------------------------+------------+--------------------------")
#         print(" Idx |              action              | RD ID | Card ID | JobNr |    NFC [length] : UID    | Time-stamp |       Date - Time")
         
        while(True):                
            self.DL_STATUS = self._mySO.AIS_ReadRTE(self._HND_AIS,byref(log_index),byref(log_action),byref(log_reader_id),byref(log_card_id),
                                                byref(log_system_id),nfc_uid,byref(nfc_uid_len),byref(timestamp))
              
             
            if self.DL_STATUS != 0:
                break
 
            print("%4d |%s| %5d | %7d | %5d | [%1d] | %s | %s" %(log_index.value,E_CARD_ACTION[log_action.value],log_reader_id.value,log_card_id.value,
                                                 log_system_id.value,nfc_uid_len.value,timestamp.value,time.ctime()))

            
#             print("log_index :{0}\n log_action :{1}\n log_reader_id :{3}\n log_card_id :{4}\n log_system_id :{5}\n nfc_uid :{6}\n nfc_uid_len :{7}\n timestamp :{7}\n " . 
#                   format(log_index.value,E_CARD_ACTION[log_action.value],log_reader_id.value,log_card_id.value,log_system_id.value,nfc_uid,
#                          nfc_uid_len.value,timestamp.value)) 


#             print(" | [%1d]" %nfc_uid_len.value)
            
#             for i in range(0,nfc_uid_len.value):
#                 print(":%02X" %nfc_uid[i])
#             for i in range(0,7):
#                 print("    ")
                 
#             print(" | %1064d | " %timestant.value)
             
            print("-----+----------------------------------+-------+---------+-------+--------------------------+------------+--------------------------")
 
 
 
 
 
    def MainLoop(self):
        print("\n#MainLoop#")
        
        RealTimeEvents  = c_int()
        LogAvailable    = c_int()
        cmdResponses    = c_int()
        cmdPercent      = c_int()
        TimeoutOccurred = c_int()
        status          = c_int()
        

        self.DL_STATUS = self._mySO.AIS_MainLoop(self._HND_AIS,
                                                 byref(RealTimeEvents),
                                                 byref(LogAvailable),
                                                 byref(cmdResponses),                                                 
                                                 byref(cmdPercent),
                                                 byref(TimeoutOccurred),
                                                 byref(status)) 
         
        if status.value:
            print("AIS_MainLoop()",status.value)
            return False
         
        
        print('RTE = %d\n' % RealTimeEvents.value)
         
         
        if RealTimeEvents.value:
            print('RTE = %d\n' % RealTimeEvents.value)
            self.PrintRTE()
            
        if LogAvailable.value:
            print("LOG= %d\n" % LogAvailable.value)
            self.PrintLOG()
            
        if TimeoutOccurred.value:
            print("TimeoutOccurred= %d\n" % TimeoutOccurred.value) 
        
        if cmdResponses.value:
            print("\n COMMAND FINISH !")   
                
        return True
    
    
    def GetLog(self):
        print("#GetLog_Set()#")
        self.DL_STATUS = self._mySO.AIS_GetLog_Set(self._HND_AIS,self._pass)
        print(self.DL_STATUS,hex(self.DL_STATUS),E_ERROR_CODES[self.DL_STATUS])        
        if self.DL_STATUS !=0: 
            return
        self.PrintLOG()
        
    
        
    def PrintLOG(self):
        
        print("#=- Print LOG -=#")
        
        log_index     = c_int()
        log_action    = c_int()
        log_reader_id = c_int()
        log_card_id   = c_int()
        log_system_id = c_int()
        nfc_uid       = (c_uint8 * NFC_UID_MAX_LEN)()
        nfc_uid_len   = c_int()
        timestamp     = c_uint64() 
            
        self.DL_STATUS = self._mySO.AIS_ReadLog(self._HND_AIS,byref(log_index),byref(log_action),byref(log_reader_id),byref(log_card_id),
                                                byref(log_system_id),nfc_uid,byref(nfc_uid_len),byref(timestamp)
                                            )    
        
       
        
        while True:
            if self.DL_STATUS != 0:
                break
            
            print("log_index :%s\n log_action :%s\n log_reader_id :%s\n log_card_id :%s\n log_system_id :%s\n nfc_uid :%s\n nfc_uid_len :%s\n timestamp :%s " % 
                  (log_index.value,
                         E_CARD_ACTION[log_action.value],
                         log_reader_id.value,
                         log_card_id.value,
                         log_system_id.value,
                         nfc_uid,
                         nfc_uid_len.value,
                         timestamp.value
                         )
                  )
            
            
    def WhiteListRead(self):
        whiteListSize = c_int()
        whiteList = c_int()
        print("#White List Read#")
        self.DL_STATUS = self._mySO.AIS_Whitelist_Read(self._HND_AIS,self._pass,byref(whiteList))
        if len(str(whiteList.value)):
            whiteListSize = whiteList.value
        else:
            whiteListSize = 0
        print("AIS_Whitelist_Read(pass:%s): size= %d > %s\n" % (self._pass,whiteListSize,E_ERROR_CODES[self.DL_STATUS]))    
    
    
    def BlackListRead(self):
        blackListSize = c_int()
        blackList = c_int()
        print("#Black List Read")
        self.DL_STATUS = self._mySO.AIS_Blacklist_GetSize(self._HND_AIS,self._pass,byref(blackListSize))
        print("AIS_Blacklist_GetSize(pass:%s): size= %d > %s\n" %(self._pass,blackListSize.value,E_ERROR_CODES[self.DL_STATUS]))
        if self.DL_STATUS != 0 or blackListSize.value <= 0:
            return
        self._mySO.AIS_Blacklist_Read(self._HND_AIS,byref(blackList))
        print(blackList.value)
         
             
  
    def ReadRTECount(self):
        count = c_int()
        count = self._mySO.AIS_ReadRTE_Count(self._HND_AIS)        
        print("\n#ReadRTE Count: %d\n" % count)        
           
    

    
        
    
    def RTEListen(self):
        stop_time = c_uint64()
        stop_time = time.time() + 10
        print("Wait for RTE...")
        
        while (time.ctime(time.time()) <time.ctime(stop_time)) :                     
            self.MainLoop()
            time.sleep(.8)
                
        
    def ListDevices(self):
            
        deviceType = E_KNOWN_DEVICE_TYPES['DL_XRCA']
        deviceId = 0 
        
        print("AIS_List_GetDevicesForCheck() BEFORE / DLL STARTUP")
        print(self.GetDevicesForCheck())
        self.EraseAllDevicesForCheck()
        
        self.DL_STATUS = self.AddDeviceForCheck(deviceType, deviceId) 
        print("AIS_List_AddDeviceForCheck(type: %d, id: %d)> { %s }\n" % (deviceType,deviceId,self.DL_STATUS))

        print("AIS_List_GetDevicesForCheck() AFTER LIST UPDATE")
        print(self.GetDevicesForCheck())

        print("checking...")
        self.devCount = self.UpdateAndGetCount()
        print("AIS_List_UpdateAndGetCount()= %d\n" % self.devCount)
        if self.devCount:
            self.GetListInformation()
            self.AISOpen()
        else:
            print("NO DEVICES")
            






if __name__ == "__main__":
    pbb = PythonBB()
    
    pbb.ListDevices()
    pbb.RTEListen()
    pbb.ReadRTECount()
    pbb.PrintLOG()
    pbb.GetLog()
    pbb.WhiteListRead()
    pbb.BlackListRead()
    print(pbb.AISGetTime())
   
    
    
    
    

