from ctypes import c_int,c_uint8,c_uint32,c_uint64,c_void_p,c_bool,c_long
import constants



class S_LOG:
    log_index         = c_int(),
    log_action        = c_int(),
    log_reader_id     = c_int(),
    log_card_id       = c_int(),
    log_system_id     = c_int(),
    log_nfc_uid       = (c_uint8 * constants.NFC_UID_MAX_LEN)(),
    log_nfc_uid_len   = c_int(),
    log_timestamp     = c_uint64()
    

class S_DEVICE:
    idx               = c_int,
    hnd               = c_void_p()
    print_percent_hdr = c_bool(),
    percent_old       = c_int(),
    status            = c_long(),
    RealTimeEvents    = c_int(),
    LogAvailable      = c_int(),
    UnreadLog         = c_int(),
    UnreadLog_last    = c_int(),
    cmdResponses      = c_int(),
    cmdPercent        = c_int(),
    DeviceStatus      = c_int(),
    TimeoutOccurred   = c_int(),
    Status            = c_int(),
    relay_state       = c_uint32(),
    log               = S_LOG()
    
    

        
    