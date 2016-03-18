#!/usr/bin/env python

"""

@author: Vladan S
@version: 2.0.1.7  (lib:4.9.4)    

"""


import os
import sys
import time
from platform import platform
from ctypes import *
from constants import *
from dl_status import *
from ais_readers_list import *
import device_list 


DL_STATUS = E_ERROR_CODES
HND_LIST  = []
HND_AIS   = c_void_p()    
devCount  = c_long()  
DEV_HND   = device_list .S_DEVICE()
log_t     = device_list .S_LOG()
const     = {}
global mySO 


def GetPlatformLib():       
            if sys.platform.startswith("win32"):                                    
                return windll.LoadLibrary(os.getcwd() + LIB_PATH + WIN_PATH + LIB_WIN32)
            elif sys.platform.startswith("linux"):
                return cdll.LoadLibrary(os.getcwd() + LIB_PATH + LINUX_PATH + LIB_LINUX) #ARMHF_PATH + LIB_ARMHF (for BeagleBoneBlack)
            elif platform().lower().find('armv7l-with-debian') > -1:
                return cdll.LoadLibrary(os.getcwd() + LIB_PATH+ LINUX_PATH + LIB_ARM) #CARM    

mySO = GetPlatformLib()
                
def AISGetVersion():        
        hardware_type    = c_int() 
        firmware_version = c_int() 
        dev              = DEV_HND    
        DL_STATUS = mySO.AIS_GetVersion(dev.hnd,byref(hardware_type),byref(firmware_version))                   
        return "AIS_GetVersion() |>>hw = %d | fw = %d\n" % (hardware_type.value,firmware_version.value)    
        
    
    
def AISUpdateAndGetCount():            
        return mySO.AIS_List_UpdateAndGetCount()
    
def AISOpen():       
        dev = DEV_HND
        res = ""  
        for hnd in HND_LIST:
            aop     = mySO.AIS_Open(hnd) 
            dev.hnd = hnd
            res    += "AIS_Open(0x%X):{ %d(%s):%s} hnd[0x%X]\n" % (dev.hnd,aop,hex(aop),E_ERROR_CODES[aop],hnd)              
            if aop == 0:               
                res  += AISGetTime()
                res  += sys_get_timezone_info()                            
        return res 
        
def AISClose(): 
        res = ""
        for hnd in HND_LIST:
            aop = mySO.AIS_Close(hnd)
            res += "AIS_Close():{ %d(%s):%s} hnd[0x%X]\n" % (aop,hex(aop),E_ERROR_CODES[aop],hnd)
        return res 
         
def AISGetTime():        
        dev      = DEV_HND       
        currTime = c_uint64()        
        timezone = c_int()
        DST      = c_int()
        offset   = c_int()                       
        dev.status = mySO.AIS_GetTime(dev.hnd,byref(currTime),byref(timezone),byref(DST),byref(offset))                            
        if dev.status:
            return wr_status("AIS_GetTime()",dev.status)                      
             
        active_device()        
        res =  "AIS_GetTime(dev[%d] hnd=0x%X)> {%d(%s):%s} = (tz= %d | dst= %d | offset= %d)  %d | %s\n" % (dev.idx,dev.hnd,dev.status,hex(dev.status), \
                 E_ERROR_CODES[dev.status],timezone.value,DST.value,offset.value,currTime.value, time.ctime(currTime.value))                                        
        return res
        
        
    
def AISSetTime():
    pass 
    currTime = c_uint64
    timez    = c_int
    DST      = c_int
    offset   = c_int 
    dev      = DEV_HND    
    currTime = int(time.time())
    timez    = sys_get_timezone()
    DST      = sys_get_daylight()
    offset   = sys_get_dstbias()       
    ais_set_time          = mySO.AIS_SetTime
    ais_set_time.argtypes = (c_void_p,c_char_p,c_uint64,c_int,c_int,c_int)
    ais_set_time.restype  = c_int
    result   = ais_set_time(dev.hnd,PASS,currTime,timez,DST,offset)
    active_device()
    res    = "AIS_SetTime(dev[%d] : pass:%s)> timezone=%d | DST=%d |offset=%d {%d(%s)%s}|%s\n" % \
             (dev.idx,PASS,timez,DST,offset,result,hex(result),E_ERROR_CODES[result],time.ctime(currTime))    
    return res
      
    
def AISGetDevicesForCheck():                    
        myStr = mySO.AIS_List_GetDevicesForCheck           
        myStr.restype = c_char_p                                  
        return myStr()
        
    
def AISEraseAllDevicesForCheck():
        mySO.AIS_List_EraseAllDevicesForCheck()
        
   
def AISAddDeviceForCheck(devType,devId):            
        return mySO.AIS_List_AddDeviceForCheck(devType,devId)
    

def AISGetLibraryVersionStr():
    dll_ver = mySO.AIS_GetLibraryVersionStr       
    dll_ver.restype = c_char_p
    return dll_ver()    
    

def active_device():  
    pass      
    dev     = DEV_HND
    dev.idx = HND_LIST.index(dev.hnd) 
    dev.idx +=1    
    res     = "Active device [%d] | hnd= 0x%X" % (dev.idx,dev.hnd) 
    return res    

def whitelist_read():       
    white_list_size = c_int()
    white_list      = c_char_p()    
    dev             = DEV_HND       
    dev.status      = mySO.AIS_Whitelist_Read(dev.hnd,PASS,byref(white_list))    
    if white_list.value:
        white_list_size = len(white_list.value)
    else:
        white_list_size = 0    
    res = "AIS_Whitelist_Read(pass:%s): size= %d >%s\n" % (PASS,white_list_size,dl_status2str(dev.status))    
    return res,white_list.value
                 
  
def blacklist_read():   
    list_size       = c_int()  
    str_black_list  = c_char_p()      
    dev             = DEV_HND
    dev.status      = mySO.AIS_Blacklist_Read(dev.hnd,PASS,byref(str_black_list))
    if dev.status == 0: 
        list_size = len(str_black_list.value)    
    re = "AIS_Blacklist_Read(pass:%s): black_list(size= %d | %s) > %s\n" % (PASS,list_size,str_black_list.value,dl_status2str(dev.status))        
    if dev.status and  black_list_size.value <= 0:        
        return res  
    return res,[str_black_list.value]
         
    
                                           

def blacklist_write(black_list_write):
    dev              = DEV_HND
    dev.status       = mySO.AIS_Blacklist_Write(dev.hnd,PASS,black_list_write)
    return "AIS_Blacklist_Write(pass:%s):b_list= %s > %s\n" %  (PASS,black_list_write,dl_status2str(dev.status))
    


def whitelist_write(white_list_write):      
    dev              = DEV_HND      
    dev.status       = mySO.AIS_Whitelist_Write(dev.hnd,PASS,white_list_write)
    return "\nAIS_Whitelist_Write(pass:%s):w_list= %s > %s\n" %  (PASS,white_list_write,dl_status2str(dev.status))
 

def print_percent_hdr():
        return
        i = c_int
        sys.stdout.write("%")
        for i in range(0,101):           
            sys.stdout.write(str(i % 10))
        sys.stdout.write("\n%=")
  
    
def dev_list():         
        list_init = c_bool
        list_init = False
        dev       = DEV_HND
        if not list_init:
            ListDevices()   #prepare device list
            list_init = True
        print"checking...please wait..."       
        devCount = AISUpdateAndGetCount()
        print("AIS_List_UpdateAndGetCount()= [%d]\n" % (devCount))        
        if devCount:
            print GetListInformation()
            AISOpen()
            dev.hnd = HND_LIST[0]                
            print active_device()
        else:
            print("NO DEVICE FOUND")
            
            
def DoCmd():    
    dev = DEV_HND
    dev.print_percent_hdr = True    
    while True:
        if not MainLoop():
            break        
        if dev.cmdResponses !=0:
            break
  
            
def log_get():    
    dev        = DEV_HND         
    dev.status = mySO.AIS_GetLog(dev.hnd,PASS)
    res = wr_status('AIS_GetLog()',dev.status)        
    if dev.status != 0:
        return res   
    DoCmd()
    log = PrintLOG() 
    return res,log
    
def log_by_index(start_index,stop_index):
   
    dev         = DEV_HND          
    dev.status  = mySO.AIS_GetLogByIndex(dev.hnd,PASS,start_index,stop_index)        
    res = 'AIS_GetLogByIndex:(pass: %s [ %d - %d ] >> %s)' % (PASS,start_index,stop_index,E_ERROR_CODES[dev.status])    
    if dev.status != 0:
        return res
    DoCmd()    
    PrintLOG()
    return res
    
    
def log_by_time(start_time,end_time):          
    dev        = DEV_HND       
    dev.status = mySO.AIS_GetLogByTime(dev.hnd,PASS,start_time,end_time)
    res = 'AIS_GetLogByTime:(pass: %s [ %10d - %10d ] >> %s)' % (PASS,start_time.value,end_time.value,E_ERROR_CODES[dev.status])    
    if dev.status !=0:
        return res
    DoCmd()    
    PrintLOG()  
    return res
    
def get_unread_log_one():
    log_available = c_uint32()
    r_log         = c_int   
    dev           = DEV_HND
    
    
    def u_log_info():
        r_log = mySO.AIS_ReadLog_Count(dev.hnd)    
        if r_log:
            print "AIS_ReadLog_Count() %d\n" % r_log
        
        r_log = mySO.AIS_ReadRTE_Count(dev.hnd)
        if r_log:
            print "AIS_ReadRTE_Count() %d\n" % r_log
            
    def u_log_count():
       
        MainLoop()
        print "LOG unread (incremental) = %d\n" % dev.UnreadLog
        u_log_info()
        
    def u_log_get():
        logIndex     = c_int()
        logAction    = c_int()
        logReaderId  = c_int()
        logCardId    = c_int()
        logSystemId  = c_int()
        nfcUid       = (c_uint8 * NFC_UID_MAX_LEN)()
        nfcUidLen    = c_int()
        timeStamp    = c_uint64() 
        nfcUid       = str()
        
        print rte_list_header[0],'\n', \
              rte_list_header[1],'\n', \
              rte_list_header[2]
        
        dev.status = mySO.AIS_UnreadLOG_Get(dev.hnd,
                                            byref(logIndex),
                                            byref(logAction),
                                            byref(logReaderId),
                                            byref(logCardId),
                                            byref(logSystemId),
                                            nfcUid,
                                            byref(nfcUidLen),
                                            byref(timeStamp)
                                           )
        if dev.status:            
            return 
        nfcuid = ''    
        for i in range(0,nfcUidLen.value):                
            nfcuid += ":%02X" % nfcUid[i]
            
        uid_uid_len = '[' + str(nfcUidLen.value) + '] | ' + nfcuid 
        print rte_format.format (logIndex.value,                                     
                                 dbg_action2str(logAction.value),
                                 logReaderId.value,
                                 logCardId.value,
                                 logSystemId.value,
                                 #uidUidLen,#nfc_uid + nfc_uid_len                                    
                                 uid_uid_len,
                                 timeStamp.value,
                                 time.ctime(timeStamp.value)
                                    )                            
        print rte_list_header[2]                                          
        
        print wr_status("AIS_UnreadLOG_Get()",dev.status)
        
        u_log_info()
        
    def u_log_ack():
        rec_to_ack = c_uint32()
        rec_to_ack = RECORDS_TO_ACK
        dev.status = mySO.AIS_UnreadLOG_Ack(dev.hnd,rec_to_ack)
        print wr_status("AIS_UnreadLOG_Ack()",dev.status)
        if dev.status:
            return
        u_log_info()
        
    def print_meni():
        print """            
               1 : Count | 2 : Get | 3 : Ack | x : Exit              
              
              """
              
    print_meni()          
    
    while True:
        m_char = sys.stdin.read(1)
        if m_char == '1':
            u_log_count()
        elif m_char == '2':
            u_log_get()
        elif m_char == '3':
            u_log_ack()
        
        elif m_char == 'x':            
            break
            
    print ShowMeni()
    
def get_io_state():
    pass
    dev      = DEV_HND
    intercom = c_uint32()
    door     = c_uint32()
    relay_state = c_uint32()
    dev.status = mySO.AIS_GetIoState(dev.hnd,byref(intercom),byref(door),byref(relay_state))
    if dev.status != 0:
        print wr_status("AIS_GetIoState()",dev.status)
        return
    print "IO STATE= intercom= %d, door= %d, relay_state= %d\n" % (intercom.value,door.value,relay_state.value)
    
    
def relay_toogle():
    dev  = DEV_HND
    get_io_state()
    dev.relay_state = not dev.relay_state
    dev.status = mySO.AIS_RelayStateSet(dev.hnd,dev.relay_state)
    print "AIS_RelayStateSet(RELAY= %d)" % dev.relay_state
    print wr_status("AIS_RelayStateSet()",dev.status)
    
def lock_open():
   
    dev            = DEV_HND
    pulse_duration = c_uint32()
    pulse_duration = int(PULSE_DURATION)
    
    dev.status     = mySO.AIS_LockOpen(dev.hnd,pulse_duration)    
    print "AIS_LockOpen(pulse_duration= %d ms)" % pulse_duration
    print wr_status("AIS_LockOpen()",dev.status)
        
    
 
def edit_device_list():
    dev_name  = c_char_p()
    dev_dsc   = c_char_p()
    status    = DL_STATUS
    
    max_dev   = E_KNOWN_DEVICE_TYPES['DL_AIS_SYSTEM_TYPES_COUNT'] 
    grid      =["-------------------------------------------------------------------",             
                "------------+-----------------+------------------------------------"
               ]
    
    def print_available_devices(): #1.        
     
        print grid[0]
        print"Look at ais_readers_list.h for Device enumeration"
        print "Known devices ( supported by %s )" % AISGetLibraryVersionStr()
        print grid[0]
        print " Dev.type   |   Short  name   | Long name"
        print grid[1]
        for i in range(1,max_dev):
            status = mySO.dbg_device_type(i,byref(dev_name),
                                byref(dev_dsc),0,0,0,0,0)                                
            sys.stdout.write("\t %2d | " % i)
            if status:
                sys.stdout.write("NOT SUPORTED! \n")
            else:
                sys.stdout.write("%15s | %s\n" % (dev_name.value,dev_dsc.value))
    
    def show_actual_list(): #forChecking 2.
        
        print "Show actual list for checking:"
        print grid[0]
        print " Dev.type   |  ID  |      Short  name   | Long name"
        print "------------+------+--------------------+--------------------------"
        get_dev = AISGetDevicesForCheck()
        a       = get_dev.split('\n')        
        for i in range(0,len(a)-1):
            c = a[i]
            b = c.split(':')
            status = mySO.dbg_device_type(int(b[0]),byref(dev_name),byref(dev_dsc),0,0,0,0,0)
            sys.stdout.write("\t%2s  | \t%2s | %18s | %s\n" % (b[0],b[1],dev_name.value,dev_dsc.value))                   
            
    def clear_list():
        print "Clear list for checking !"
        AISEraseAllDevicesForCheck()
    
   
    def print_meni():
        print """            
            1 : show known device types
            2 : show actual list for checking 
            3 : clear list for checking
            4 : add device for check
            5 : erase device from checking list
            ------------------------------------
            m : print meni
            x : Exit
            """
    def loop_meni():
        while True:
            choise = sys.stdin.read(1)
            if choise == 'm':
                print_meni()
            elif choise == '1':
                print_available_devices()
            elif choise == '2':
                show_actual_list()
            elif choise == '3':
                clear_list()
            elif choise == '4':
                add_device_for_check()
            elif choise == '5':
                erase_device()
                
            elif choise == 'x':
                break
    
    def do_dev_action(f_name,device_type,device_id):
        deviceType  = c_int()
        deviceId    = c_int()
        deviceType  = device_type
        deviceId    = device_id
        
        # list_erased = False
        status      = DL_STATUS 
        print "Enter device type and then enter device BUS ID for check"    
        while True:          
            sys.stdin.read(1)   #<==== proveriti        
            
            r = raw_input("Enter device type (1,2, ... , %d) ('x' for exit)  : " % (max_dev-1))                        
            if r == "x":
                break
            elif r.isdigit():
                deviceType = int(r) 
               
            r = raw_input("Enter device bus ID (if full duplex then enter 0) : ")           
            if  r == 'x':
                deviceId = 0
            elif r.isdigit():                  
                deviceId = int(r)    
         
            
            if f_name == 'AIS_List_AddDeviceForCheck':    
                status = mySO.AIS_List_AddDeviceForCheck(deviceType,deviceId)
                
            elif f_name == 'AIS_List_EraseDeviceForCheck':
                status = mySO.AIS_List_EraseDeviceForCheck(deviceType,deviceId)
            
            print "%s(type: %d, id: %d)> { %s }\n" % (f_name,deviceType,deviceId,dl_status2str(status))
            
            
        print "\nFinish list edit."        
        print "AFTER UPDATE CYCLE \n%s" % AISGetDevicesForCheck()
    
    
    def add_device_for_check():      
        print "AIS_List_AddDevicesForCheck() ..."
        do_dev_action('AIS_List_AddDeviceForCheck',0,0)
        
    
    
    def erase_device(): #from checking list 
        print "AIS_List_EraseDeviceForCheck()..."
        do_dev_action('AIS_List_EraseDeviceForCheck',0,0)
    
    
    print_meni()
    loop_meni() 
    
    
    

def change_password():
    
    print "Old password is actual application password: %s " % const['PASS']
    dev      = DEV_HND
    sys.stdin.read(1)
    new_pass = raw_input("Enter new password for units ( and application ): ")
    if  len(new_pass) == 0:
        print 'Patch - new pass = default pass'
        new_pass = const['PASS']       
    
    print 'old pass = %s\nnew pass = %s\n' % (PASS,new_pass)
    dev.status = mySO. AIS_ChangePassword(dev.hnd,PASS,new_pass)
    print 'AIS_ChangePassword (old pass= %s new pass= %s |%s\n' %(PASS,new_pass,dl_status2str(dev.status))
    if dev.status == 0:
        PASS = new_pass
        print 'New default application password = %s\n' % PASS

def set_default_password():
    
    print "Actual application password is :%s " % PASS
    sys.stdin.read(1)
    new_pass = raw_input("Enter new default application password :")
    if  len(new_pass) == 0:
        print 'Patch - new pass = default pass'
        new_pass = PASS    
    PASS = new_pass
    print 'New default application password = %s\n' % PASS
            
 
def PrintLOG():
        pass
        rte_res      = ""         
        logIndex     = c_int()
        logAction    = c_int()
        logReaderId  = c_int()
        logCardId    = c_int()
        logSystemId  = c_int()
        logNfcUid    = (c_uint8 * NFC_UID_MAX_LEN)()
        logNfcUidLen = c_int()
        logTimeStamp = c_uint64() 
        nfcuid       = str()
                   
        dev          = DEV_HND 
        rte_hed = rte_list_header[0],'\n', \
                rte_list_header[1],'\n', \
                rte_list_header[2]   
                
        while True:            
            dev.status =  mySO.AIS_ReadLog(dev.hnd,byref(logIndex),
                                               byref(logAction),
                                               byref(logReaderId),
                                               byref(logCardId),
                                               byref(logSystemId),
                                               logNfcUid,
                                               byref(logNfcUidLen),
                                               byref(logTimeStamp)
                                          )
       
            
            dev.log.log_index       = logIndex.value
            dev.log.log_action      = logAction.value
            dev.log.log_reader_id   = logReaderId.value
            dev.log.log_card_id     = logCardId.value
            dev.log.log_system_id   = logSystemId.value
            dev.log.log_nfc_uid     = logNfcUid
            dev.log.log_nfc_uid_len = logNfcUidLen.value
            dev.log.log_timestamp   = logTimeStamp.value
            
            
            if dev.status != 0:
                break
            
            nfcuid = '' 
            for i in range(0,dev.log.log_nfc_uid_len):                
                nfcuid += ":%02X" % (dev.log.log_nfc_uid[i])
            
            uidNfcUidLen = '[' + str(dev.log.log_nfc_uid_len) + '] | ' + nfcuid  
          
            
            
            rte_res += (log_format.format(dev.log.log_index,
                                    #string_at(mySO.dbg_action2str(dev.log.log_action)).decode('utf-8'),
                                    dbg_action2str(dev.log.log_action),
                                    dev.log.log_reader_id,
                                    dev.log.log_card_id,
                                    dev.log.log_system_id,
                                    uidNfcUidLen,                                    
                                    dev.log.log_timestamp,
                                    time.ctime(dev.log.log_timestamp)
                                   )
                 )
       
            res = rte_res + rte_list_header[2]
        return rte_hed + res #+ '\n' + wr_status('AIS_GetLog()', dev.status)
       

def RTEListen():
    pass 
    stop_time = c_uint64()
    stop_time = time.time() + 10 #10
    dev       = DEV_HND
    print"Wait for RTE for %d..." % SECONDS       
    while (time.ctime(time.time()) < time.ctime(stop_time)) :
        for hnd in HND_LIST:
            dev.hnd = hnd            
            MainLoop()                       
        time.sleep(THD_SLEEP)     
    print "End RTE listen"    
    
            
            
def AIS_GetLog_Set():
    dev       = DEV_HND
    DL_STATUS =  mySO.AIS_GetLog_Set(dev.hnd,PASS)
    res       =  DL_STATUS,hex( DL_STATUS),E_ERROR_CODES[ DL_STATUS]
    return res     

        
             
def GetInfoAndDeviceCount():            
        print  AISUpdateAndGetCount()
         
def GetTime():                
        print  AISGetTime()
     

def ListDevices():
            
        deviceType = E_KNOWN_DEVICE_TYPES['DL_AIS_BASE_HD_SDK']               
        print("AIS_List_GetDevicesForCheck() BEFORE / DLL STARTUP : %s" % ( AISGetDevicesForCheck()))         
        AISEraseAllDevicesForCheck()        
        
        
        deviceId = 1        
        DL_STATUS =  AISAddDeviceForCheck(deviceType, deviceId) 
        print("AIS_List_AddDeviceForCheck(type: %d, id: %d)> DL_STATUS{ %s }" % (deviceType,deviceId, DL_STATUS))
            
        deviceId = 3        
        DL_STATUS =  AISAddDeviceForCheck(deviceType, deviceId) 
        print("AIS_List_AddDeviceForCheck(type: %d, id: %d)> DL_STATUS{ %s }" % (deviceType,deviceId, DL_STATUS))
        
        print("AIS_List_GetDevicesForCheck() AFTER LIST UPDATE : \n%s" % ( AISGetDevicesForCheck()))


def GetListInformation():
        res_0,res_1 = "",""
        res = ""        
        hnd            = c_void_p()
        devSerial      = c_char_p()
        devType        = c_int()
        devID          = c_int()
        devFW_VER      = c_int()
        devCommSpeed   = c_int()
        devFTDI_Serial = c_char_p()
        devOpened      = c_int()
        devStatus      = c_int()
        systemStatus   = c_int()    
        
        res_0 = format_grid[0] + '\n' + format_grid[1] + '\n' + format_grid[2] + '\n'
      
        devCount =  AISUpdateAndGetCount()                 
        del HND_LIST[:]   #erase all in list
        
       
        
        for i in range(0,devCount):                             
            DL_STATUS =  mySO.AIS_List_GetInformation(byref(hnd),
                                                     byref(devSerial),
                                                     byref(devType),
                                                     byref(devID),
                                                     byref(devFW_VER),
                                                     byref(devCommSpeed),
                                                     byref(devFTDI_Serial),
                                                     byref(devOpened),
                                                     byref(devStatus),
                                                     byref(systemStatus)
                                                    )            
            HND_LIST.append(hnd.value)                                 
            res_1 += (mojFormat.format(i+1,
                                   hnd.value,
                                   devSerial.value.decode("utf-8"),
                                   devType.value,
                                   devID.value,
                                   devFW_VER.value,
                                   devCommSpeed.value,
                                   devFTDI_Serial.value.decode("utf-8"),
                                   devOpened.value,
                                   devStatus.value,
                                   systemStatus.value
                                   )
                )
                              
            res  = res_1 + format_grid[0]
        return res_0 + res
    
    
def PrintRTE():
        
      
        logIndex     = c_int()
        logAction    = c_int()
        logReaderId  = c_int()
        logCardId    = c_int()
        logSystemId  = c_int()
        nfcUid       = (c_uint8 * NFC_UID_MAX_LEN)()
        nfcUidLen    = c_int()
        timeStamp    = c_uint64() 
        nfcUid       = str()
        rteCount     = c_int
        dev          = DEV_HND
        rte_count    =  mySO.AIS_ReadRTE_Count(dev.hnd)
        
        print 'AIS_ReadRTE_Count = %d\n' % rte_count        
        print("= RTE Real Time Events = \n")       
        print rte_list_header[0],'\n', \
              rte_list_header[1],'\n', \
              rte_list_header[2]
        
        
        while True:                
            DL_STATUS =  mySO.AIS_ReadRTE(dev.hnd,
                                           byref(logIndex),
                                           byref(logAction),
                                           byref(logReaderId),
                                           byref(logCardId),
                                           byref(logSystemId),
                                           nfcUid,
                                           byref(nfcUidLen),
                                           byref(timeStamp)
                                         )
                        
            dev.log.log_index       = logIndex.value
            dev.log.log_action      = logAction.value
            dev.log.log_reader_id   = logReaderId.value
            dev.log.log_card_id     = logCardId.value
            dev.log.log_system_id   = logSystemId.value
            dev.log.log_nfc_uid     = nfcUid
            dev.log.log_nfc_uid_len = nfcUidLen.value
            dev.log.log_timestamp   = timeStamp.value
            
            
            
            if  DL_STATUS != 0:            
                break  
            nfcuid = ''    
            for i in range(0,dev.log.log_nfc_uid_len):                
                nfcuid += ":%02X" % dev.log.log_nfc_uid[i]
            
            uid_uid_len = '[' + str(dev.log.log_nfc_uid_len) + '] | ' + nfcuid 
            print rte_format.format (dev.log.log_index,                                     
                                     dbg_action2str(dev.log.log_action),
                                     dev.log.log_reader_id,
                                     dev.log.log_card_id,
                                     dev.log.log_system_id,
                                     uid_uid_len,#nfc_uid + nfc_uid_len                                    
                                     dev.log.log_timestamp,
                                     time.ctime(dev.log.log_timestamp)
                                    )                            
            print rte_list_header[2] 
        print "LOG unread (incremental) = %d" % dev.UnreadLog             
        print  wr_status('AIS_ReadRTE()', DL_STATUS)
    
def MainLoop():
                       
        real_time_events  = c_int()
        log_available     = c_int()
        unreadLog         = c_int()
        cmd_responses     = c_int()
        cmd_percent       = c_int()
        device_status     = c_int()
        time_out_occurred = c_int()
        _status           = c_int()
        
        
        
        dev               = DEV_HND         
        dev.status        =  mySO.AIS_MainLoop(dev.hnd,
                                             byref(real_time_events),
                                             byref(log_available),
                                             byref(unreadLog),
                                             byref(cmd_responses),                                                 
                                             byref(cmd_percent),
                                             byref(device_status),
                                             byref(time_out_occurred),
                                             byref(_status)
                                            ) 
             
        dev.RealTimeEvents  = real_time_events.value
        dev.LogAvailable    = log_available.value
        dev.UnreadLog       = unreadLog.value
        dev.cmdResponses    = cmd_responses.value                                                 
        dev.cmdPercent      = cmd_percent.value
        dev.DeviceStatus    = device_status.value
        dev.TimeoutOccurred = time_out_occurred.value
        dev.Status          = _status.value
         
        if dev.status:                            
            return False           
        
        if dev.RealTimeEvents:                 
            PrintRTE()
        
        if dev.LogAvailable:
            print("LOG= %d\n" % dev.LogAvailable)
            PrintLOG()
        
        
        if dev.UnreadLog_last <> dev.UnreadLog:                                
                   # print "LOG unread (incremental) = %d" % dev.UnreadLog                 
                    dev.UnreadLog_last = dev.UnreadLog
                    
                  
        if dev.TimeoutOccurred:
            print("TimeoutOccurred= %d\n" % dev.TimeoutOccurred)  
            
            
        if dev.cmdPercent:
            if dev.print_percent_hdr:
                print_percent_hdr()
                dev.percent_old = -1
                dev.print_percent_hdr = False
            
            while (dev.percent_old != dev.cmdPercent):
                if dev.percent_old < 100:
                    sys.stdout.write(".")                    
                    dev.percent_old +=1
        
        if dev.cmdResponses:            
            print "\n-- COMMAND FINISH !\n"
        
       
       
        return True 
    
def TestLights():
        
        green_master = False
        red_master   = False
        green_slave  = False
        red_slave    = False
        dev          = DEV_HND
        
        light_meni   = """
                       g : green master | r : red master | G : green slave | R : red slave  || x : exit 
                       """ 
                
        print light_meni
        def light_control():
            DL_STATUS = mySO.AIS_LightControl(dev.hnd,green_master,red_master,green_slave,red_slave)
            print "AIS_LightControl(master:green= %d | master:red= %d || slave:green= %d | slave:sred= %d) > %s\n" %  (green_master,red_master,green_slave,red_slave,E_ERROR_CODES[ DL_STATUS])
                                              
       
        while True:
            choise = sys.stdin.read(1)
            if choise == 'g':
                green_master = not green_master
                light_control()
            elif choise == 'r':
                red_master = not red_master
                light_control()
            elif choise == 'G':
                green_slave = not green_slave
                light_control()
            elif choise == 'R':
                red_slave = not red_slave
                light_control()    
        
            elif choise == 'x':
                break
       
        print ShowMeni()

 

def init():   
        
    print AISGetLibraryVersionStr()     
    dev_list()        
    print ShowMeni()
    



                
def ShowMeni():  #q,d,o,c,d,t,T,E,p,l,n,N,w,W,b,B,r,g,R,G,v,F,i,m,x,u
        my_meni = """
        
        --------------------------
        Press key to select action\n
        q : List devices\t\t\to : Open device\t\t\t\tc : Close device        
        d : Get devices count\t\t\tt : Get time\t\t\t\tT : Set time                    
        r : Real Time Events\t\t\tP : Set application password\t\tp : Change device password
        l : Get log\t\t\t\tn : Get log by Index\t\t\tN : Get log by Time       
        u : Get unread log\t\t\tw : White-list Read\t\t\tW : White-list Write                       
        b : Black-list Read\t\t\tB : Black-list Write\t\t\tL : Test Lights
        g : Get IO state\t\t\tG : Open gate/lock\t\t\ty : Relay toggle state 
        v : Get Library Version\t\t\tf : Get Firmware Version\t\ti : Device Information        
        m : Meni\t\t\t\tQ : Edit device list for checking                       
        x : EXIT 
        --------------------------
                
        """      
        return my_meni

 
def MeniLoop():        
        m_char = sys.stdin.read(1) 
        dev    = DEV_HND    
        if m_char.isdigit(): 
            dev.hnd = HND_LIST[int(m_char) -1]    
            dev.idx = HND_LIST.index(dev.hnd)        
            print active_device()
            
        if m_char == 'x': 
            print 'EXIT\n'
            AISClose()
            return False 
        
        elif m_char == 'Q':
            edit_device_list()
        
        elif m_char == 'w': 
            print "-= Read White List =-" 
            print active_device()    
            whitelist_read()
            
        elif m_char == 'W':            
            print "=- Write White List -=" 
            print active_device()    
            print "Enter white-list UIDs (in HEX format delimited with '.' or ':' or not)"
            print "Each UID separate by ',' or space eg. 37:0C:96:69,C2.66.EF.95 01234567\n"  
            sys.stdin.read(1)
            white_list_write = raw_input('Enter White List UID: ') 
            print whitelist_write(white_list_write)
        
        elif m_char == 'b': 
            print "-= Read Black List =-" 
            print active_device()    
            print blacklist_read() 
        
        elif m_char == 'B':            
            print "=- Write Black List -="
            print active_device()
            print "Try to write black-list decimal numbers (delimited with anything)"
            print "eg. 2, 102 250;11\n"
            sys.stdin.read(1)
            black_list_write = raw_input('Enter Black List: ')        
            print blacklist_write(black_list_write)
        
        elif m_char == 'q':                    
            print GetListInformation()
               
        elif m_char == 'o':
            AISOpen()            
        
                 
        elif m_char == 'c':
            AISClose()             
        
        elif m_char == 'i':        
            print AISGetVersion()
            AISGetTime()
            print sys_get_timezone_info()
        
        elif m_char == 'l':            
            print log_get()
        
        elif m_char == 'n':
            print '#=- Print log by index -=#'
            sys.stdin.read(1)
            start_index = int(raw_input("Enter index start:"))
            stop_index  = int(raw_input("Enter index stop :"))
            print log_by_index(start_index,stop_index)
            
        elif m_char == 'N':
            print '#=- Read LOG by Time (time-stamp) range -=#'        
            start_time = c_uint64
            end_time   = c_uint64
            sys.stdin.read(1)
            start_time = c_uint64(input("Enter time-stamp start:"))    
            end_time   = c_uint64(input("Enter time-stamp stop :"))
            print log_by_time(start_time,end_time)
        
        elif m_char == 'u':
            get_unread_log_one()
        
        elif m_char == 'g':
            get_io_state()
        
        elif m_char == 'G':
            lock_open()
         
        elif m_char == 'y':
            relay_toogle()
        
        elif m_char == 't':  
            
            AISGetTime()
        
        elif m_char == 'T':
            AISSetTime()
            
        elif m_char == 'r':
            RTEListen()
        
        elif m_char == 'L':
            TestLights()
        
        elif m_char == 'v':
            print AISGetLibraryVersionStr()
        
        elif m_char == 'f':            
            print AISGetVersion() 
        
        elif m_char == 'd':
            print 'GET DEVICE COUNT : %d\n' % AISUpdateAndGetCount() 
        
        elif m_char == 'p':
            change_password()
            
        elif m_char == 'P':
            set_default_password()
       
        elif m_char == 'm':
            print(ShowMeni())
         
        return True
  

#================ helper functions ===================
    
def wr_status(funct_name,dl_status):
    res = funct_name + ': {%d(%s): %s}\n' % (dl_status,hex(dl_status),E_ERROR_CODES[dl_status])    
    return res
        
# def dbg_action2str(action_value):    
    # res = '[%d(%s):%s]' % (action_value,hex(action_value),E_CARD_ACTION[action_value])
    # return res
   
# def dl_status2str(status):
    # res = '[%d(%s):%s]' % (status,hex(status),E_ERROR_CODES[status])
    # return res

    
    
def dbg_action2str(action_value):
    dbg_a = mySO.dbg_action2str
    dbg_a.argtype = c_int
    dbg_a.restype = c_char_p    
    return dbg_a(action_value)

def dl_status2str(status):
    dl_s = mySO.dl_status2str
    dl_s.argtype = DL_STATUS
    dl_s.restype = c_char_p    
    return dl_s(status)

def sys_get_timezone():
    s_tz = mySO.sys_get_timezone
    s_tz.restype = c_long
    return s_tz()

def sys_get_daylight():
    s_dl  = mySO.sys_get_daylight
    s_dl.restype = c_int
    return s_dl()    

def sys_get_dstbias():
    s_dstb = mySO.sys_get_dstbias
    s_dstb.restype = c_long
    return s_dstb()  

def sys_get_timezone_info():
    s_tzinfo = mySO.sys_get_timezone_info
    s_tzinfo.restype = c_char_p
    return s_tzinfo()

#====================================================
  
  
  
  
  
mojFormat      = "| {0:3d} | {1:016X} | {2} | {3:7d}  | {4:2d}  | {5}  | {6:7d} | {7:10s} | {8:5d}  | {9:8d}  | {10:9d} |\n"    

format_grid = ["--------------------------------------------------------------------------------------------------------------------",
               "| indx|  Reader HANDLE   | SerialNm | Type h/d | ID  | FW   | speed   | FTDI: sn   | opened | DevStatus | SysStatus |",
               "--------------------------------------------------------------------------------------------------------------------"
              ]    


rte_list_header=["-----------------------------------------------------------------------------------------------------------------------------------------",
                 "| Idx   |              action              | RD ID | Card ID | JobNr |    NFC [length] : UID    | Time-stamp |       Date - Time        |",
                 "----------------------------------------------------------------------------------------------------------------------------------------"
                ]


rte_format = "| {0:5d} | {1:28s} | {2:5d} | {3:7d} | {4:5d} | {5:24s} | {6:10d} | {7:s} | "

log_format = "| {0:5d} | {1:32s} | {2:5d} | {3:7d} | {4:5d} | {5:24s} | {6:#10d} | {7:s} | "




if __name__ == '__main__':      
    #global mySO   
    #mySO = GetPlatformLib() 
    init() 
    while True:
        if not MeniLoop():
            break
          
    if sys.platform.startswith('linux'):
        os.system('pkill -9 python')
    elif sys.platform.startswith('win'):            
        sys.exit(0)
        
           
    
    
        
        
                    
 
