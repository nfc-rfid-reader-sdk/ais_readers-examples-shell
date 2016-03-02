

from dl_status import E_ERROR_CODES
import ctypes


CWIN32    = 'ais_readers-x86.dll'
CLINUX    = 'libais_readers-x86_64.so'
CARM      = 'libais_readers-arm.so'
CARMHF    = 'libais_readers-armhf.so'
THD_SLEEP = .7
RTE_JOIN  = 1.0 #timeout 3.0
SERV_JOIN = 3.0 #timeout

#pass
PASS      = '1111'


NFC_UID_MAX_LEN = 10
DL_STATUS       = E_ERROR_CODES
 
#url_query_string
START_INDEX      = 'start_index'
END_INDEX        = 'end_index'
START_TIME       = 'start_time'
END_TIME         = 'end_time'
BLACK_LIST_WRITE = 'black_list_write'
WHITE_LIST_WRITE = 'white_list_write'
NEW_PASS         = 'new_pass'


#apache mysql
HTTP            = 'http://'
SERVER_NAME     = 'localhost'
USER_NAME       = 'root'
RTE_EVENTS      = '/events.php'

#local mysql
SERVER_NAME      = 'localhost'
SERVER_USER_NAME = 'root'
SERVER_PASSWORD  = 'vladan' #dlogic654
DATABASE_NAME    = 'ais_readers_db' #AISReaders
TABLE_NAME       = 'rte'

LOG_INDEX        = 'log_index'
LOG_ACTION       = 'log_action'
LOG_READER_ID    = 'log_reader_id'
LOG_CARD_ID      = 'log_card_id'
LOG_SISTEM_ID    = 'log_system_id'
NFC_UID          = 'nfc_uid'
NFC_UID_LEN      = 'nfc_uid_len'
TIMESTAMP        = 'timestamp'
M_TIME           = 'm_time'

#http
HTTP_SERVER_NAME = ''
HTTP_SERVER_PORT = 8080 #8080