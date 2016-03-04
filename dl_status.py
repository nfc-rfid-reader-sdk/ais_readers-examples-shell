'''
Created on Nov 16, 2015

@author: Vladan
'''

E_ERROR_CODES = {    
    0x00:'DL_OK',    
    0x01:'TIMEOUT_ERROR',
    0x02:'NULL_POINTER',
    0x03:'PARAMETERS_ERROR',
    0x04:'MEMORY_ALLOCATION_ERROR',
    0x05:'NOT_INITIALIZED',
    0x06:'ALREADY_INITIALIZED',
    0x07:'TIMESTAMP_INVALID',
    0x08:'EVENT_BUSY',

   
    0x1000:'ERR_SPECIFIC',
    
    0x1001:'CMD_BRAKE_RTE', 

    0x1002:'USB_RF_ACK_FAILED',
    0x1003:'NO_RF_PACKET_DATA',

    0x1004:'TRANSFER_WRITING_ERROR',

    0x1005:'EVENT_WAKEUP_BUSY',

  
    0x2000:'RESOURCE_NOT_ACQUIRED',
    0x2001:'RESOURCE_ALREADY_ACQUIRED',
    0x2002:'RESOURCE_BUSY',

    
    0x3000:'FILE_OVERSIZE',
    0x3001:'FILE_EMPTY',
    0x3002:'FILE_LOCKED', 
    0x3004:'FILE_NOT_FOUND',
    0x3005:'ERR_NO_FILE_NAME',
    0x3006:'ERR_DIR_CAN_NOT_CREATE',

   
    0x4000:'ERR_DATA',
    0x4001:'ERR_BUFFER_EMPTY',
    0x4002:'ERR_BUFFER_OVERFLOW',
    0x4003:'ERR_CHECKSUM',
    0x4004:'LOG_NOT_CORRECT',

   
    0x7000:'LIST_ERROR',
    0x7001:'ITEM_IS_ALREADY_IN_LIST',
    0x7002:'ITEM_NOT_IN_LIST',

    
    0x8000:'NO_DEVICES',    
    0x8001:'DEVICE_OPENING_ERROR',
    0x8002:'DEVICE_CAN_NOT_OPEN',
    0x8003:'DEVICE_ALREADY_OPENED',
    0x8004:'DEVICE_NOT_OPENED',
    0x8005:'DEVICE_INDEX_OUT_OF_BOUND',
    0x8006:'DEVICE_CLOSE_ERROR',
    0x8007:'DEVICE_UNKNOWN',

  
    0x9000:'ERR_COMMAND_RESPONSE',
    0x9001:'CMD_RESPONSE_UNKNOWN_COMMAND',
    0x9002:'CMD_RESPONSE_WRONG_CMD',
    0x9003:'CMD_RESPONSE_COMMAND_FAILED',
    0x9004:'CMD_RESPONSE_UNSUCCESS',
    0x9005:'CMD_RESPONSE_NO_AUTHORIZATION',
    0x9006:'CMD_RESPONSE_SIZE_OVERFLOW',
    0x9007:'CMD_RESPONSE_NO_DATA',

    
    0xA000:'THREAD_FAILURE',
    0xA001:'ERR_OBJ_NOT_CREATED',    
    0xA002:'ERR_CREATE_SEMAPHORE',

    
    0xB000:'ERR_STATE_MACHINE',
    0xB001:'ERR_SM_IDLE__NO_RESPONSE',
    0xB002:'ERR_SM_COMMAND_IN_PROGRESS',
    0xB003:'ERR_SM_NOT_IDLE',
    0xB004:'ERR_SM_CMD_NOT_STARTED',

    0xD000:'READER_ERRORS_',
    0xD001:'READER_UID_ERROR',
    0xD002:'READER_LOG_ERROR',

  
    0xE000:'DL_HAMMING_ERROR',
    0xE001:'DL_HAMMING_NOT_ACK',
    0xE002:'DL_HAMMING_WRONG_ACK',
    0xE003:'DL_HAMMING_WRONG_REPLAY',
    0xE004:'ERROR_SOME_REPLAY_FAULT',

    
    0xE005:'DL_HAMMING_TERR_TIMEOUT',
    0xE006:'DL_HAMMING_TERR_BAD_FRAME',
    0xE007:'DL_HAMMING_TERR_BAD_SUM',
    0xE008:'DL_HAMMING_TERR_BAD_CODE',
    0xE009:'DL_HAMMING_TERR_TOO_OLD',
    0xE00A:'DL_HAMMING_TERR_NOISE', 
    0xE00B:'DL_HAMMING_TERR_ERROR_MASK',

    0xF000:'NO_FTDI_COMM_DEVICES',
    0xF001:'NO_FTDI_COMM_DEVICES_OPENED',

    0xF002:'ERR_FTDI',
    0xF003:'ERR_FTDI_READ',
    0xF004:'ERR_FTDI_READ_LESS_DATA',
    0xF005:'ERR_FTDI_WRITE',
    0xF006:'ERR_FTDI_WRITE_LESS_DATA',
    0xF007:'DL_FT_ERROR_SET_TIMEOUT',

    
    0xF100:'DL_FT_',
    0xF101:'DL_FT_INVALID_HANDLE',
    0xF102:'DL_FT_DEVICE_NOT_FOUND',
    0xF103:'DL_FT_DEVICE_NOT_OPENED',
    0xF104:'DL_FT_IO_ERROR',
    0xF105:'DL_FT_INSUFFICIENT_RESOURCES',
    0xF106:'DL_FT_INVALID_PARAMETER',
    0xF107:'DL_FT_INVALID_BAUD_RATE',

    0xF108:'DL_FT_DEVICE_NOT_OPENED_FOR_ERASE',
    0xF109:'DL_FT_DEVICE_NOT_OPENED_FOR_WRITE',
    0xF10A:'DL_FT_FAILED_TO_WRITE_DEVICE',
    0xF10B:'DL_FT_EEPROM_READ_FAILED',
    0xF10C:'DL_FT_EEPROM_WRITE_FAILED',
    0xF10D:'DL_FT_EEPROM_ERASE_FAILED',
    0xF10E:'DL_FT_EEPROM_NOT_PRESENT',
    0xF10F:'DL_FT_EEPROM_NOT_PROGRAMMED',
    0xF110:'DL_FT_INVALID_ARGS',
    0xF111:'DL_FT_NOT_SUPPORTED',
    0xF112:'DL_FT_OTHER_ERROR',
    0xF113:'DL_FT_DEVICE_LIST_NOT_READY',

    
    0xFFFFFFFE:'NOT_IMPLEMENTED',
    
    0xFFFFFFFF:'UNKNOWN_ERROR',

    0xFFFFFFFF:'MAX_DL_STATUS',
    0xFFFFFFFF:'LAST_ERROR' 
}