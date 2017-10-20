/*
 * ais_readers.h
 *
 * library version : 4.12.10
 *
 *  Created on: 04.07.2011.
 *      Author: srkos
 */

#ifndef AIS_READERS_H_
#define AIS_READERS_H_

////////////////////////////////////////////////////////////////////////////////////////////////////
typedef enum E_CARD_ACTION
{
	// new card type
	// new card type
//	//-----------------
//	ACTION_REJECTED_BLACKLIST,
//	ACTION_REJECTED_FOREIGN,
//
//	ACTION_UNLOCKED_WHITELIST,
//
//	ACTION_REJECTED_BAD_CRC, // known key
//	ACTION_REJECTED_UNKNOWN_KEY, //
//	ACTION_REJECTED_AUTH, //
//	ACTION_REJECTED_OTHER, // ?
	// new card type
	// new card type
	// new card type


	// CARD_FOREIGN
	// strange card - card from different system
	// BASE> LOG = 0x83 | RTE = 0x00
	ACTION_CARD_FOREIGN = 0x00,

	// DISCARDED
	// blocked card - card on blacklist, no valid access right, has no right of passage
	// BASE> LOG= 0xC3 | RTE= 0x20
	// (32 dec)
	ACTION_CARD_DISCARDED = 0x20,

	// CARD_HACKED
	// Mifare key OK - CRC OK - but bad user data
	// Bad protective data
	// BASE> LOG= 0x84 | RTE= 0x40
	// (64 dec)
	ACTION_CARD_HACKED = 0x40,

	// CARD_BAD_DATA
	// Mifare key OK - CRC BAD
	// Cards with invalid data - BAD CRC
	// BASE> LOG= 0x-- | RTE= 0x82
	// (80 dec)
	ACTION_CARD_BAD_DATA = 0x50,

	// CARD_NO_DATA
	// unreadable card - card without or unknown Mifare key
	// BASE> LOG= 0x-- | RTE= 0x81
	// (96 dec)
	ACTION_CARD_NO_DATA = 0x60,

	// UNLOCKED
	// The correct card
	// BASE> LOG= 0xC2 | RTE= 0x80(+++)
	// TWR> 0x80 (128 dec) - A regular passage (P)
	// TWR> 0x90 (144 dec) - Official exit (S)
	// TWR> 0xA0 (160 dec) - Vehicle pass (V)
	// TWR> 0xB0 (176 dec) - Approved exit (O)
	ACTION_CARD_UNLOCKED = 0x80,
	ACTION_CARD_UNLOCKED_1,
	ACTION_CARD_UNLOCKED_2,
	ACTION_CARD_UNLOCKED_3,
	ACTION_CARD_UNLOCKED_4,
	ACTION_CARD_UNLOCKED_5,
	ACTION_CARD_UNLOCKED_6,
	ACTION_CARD_UNLOCKED_7,

	UNLOCKED_WHITELIST,
	UNLOCKED_UID,

	UNLOCKED_INTERCOM,
	UNLOCKED_DIG_IN,

	ACTION_QR_UNLOCKED = 0x70,
	ACTION_QR_BLOCKED = 0x71,
	ACTION_QR_UNKNOWN = 0x72,
// not used anymore
//#define CARD_OK			0x85

	ACTION_IO_EXPANDER_OK = 0x90,
	ACTION_IO_EXPANDER_FAIL = 0x91,

// non valid status
// not used status
//	ACTION_DEVICE_MISSING = 0xA1,
//	ACTION_BREAK_THROUGH = 0xA2,
//	ACTION_DOOR_LEFT_OPEN = 0xA3,

	//--------------------
	ACTION_CARD_UNKNOWN	= 0xFF
} e_card_action;
////////////////////////////////////////////////////////////////////////////////////////////////////
//##############################################################################

//--------------------------------------------------------------------------------------------------
#include <stdint.h>
#include <stdbool.h>

//--------------------------------------------------------------------------------------------------
#ifndef IN
#define IN
#endif

#ifndef OUT
#define OUT
#endif
//--------------------------------------------------------------------------------------------------

#ifdef __cplusplus
#	define EXTC_ extern "C"
#else
#	define EXTC_
#endif

#if __linux__ || __APPLE__
#	define DL_API EXTC_
#else
// WINDOWS
#	if defined DL_API_STATIC
#		define DL_API EXTC_
#	elif defined DL_API_EXPORTS
#		define DL_API EXTC_ __declspec(dllexport) __stdcall
#	else
#		define DL_API EXTC_ /* __declspec(dllimport) */ __stdcall
#	endif
#endif

#ifdef DL_API_STATIC
#	define DL_APIS	DL_API
#endif

#if defined(DL_API_EXPORTS)
#	include "handler.h"
#else
	typedef void * HND_AIS;
#endif
////////////////////////////////////////////////////////////////////////////////////////////////////
#include "dl_status.h"
#include "ais_readers_list.h"
////////////////////////////////////////////////////////////////////////////////////////////////////
//--------------------------------------------------------------------------------------------------

#define NFC_UID_MAX_LEN			10

////////////////////////////////////////////////////////////////////
/**
 * Type for representing null terminated char array ( aka C-String )
 * Array is always one byte longer ( for null character ) then string.
 *
 * 1. Only allocate pointer to c_string, no need to allocate memory space for all array:
 *    When function returns type c_string, and when need to get c_string from function
 *
 * 2. Must allocate memory space for c_string before use:
 *    array must be allocated and initialized when need to send data to function
 *    like password, white list sting, ...
 */
typedef const char * c_string;
////////////////////////////////////////////////////////////////////


///**
// *
// * uint32_t library_version;
// * c_string lib_version_str;
// *
// *
// * ### Usage 1: only need version in string format for printing
// *
// * lib_version_str = AIS_GetLibraryVersion(0);
// * puts(lib_version_str); //
// * ### or
// * puts(AIS_GetLibraryVersion(0)); //
// *
// * ### Usage 2: need version in
// * @param library_version
// * @return
// */
//DL_API
//c_string AIS_GetLibraryVersion(uint32_t *library_version);


/**
 * Get version of library in string format
 *
 * e.g. "AIS READERS library version= 4.9.1"
 * @return pointer to string
 */
DL_API
c_string AIS_GetLibraryVersionStr(void);

/**
 * Get version of library in number format
 *
 * @return 32 bit unsigned integer with packet major, minor and build version information
 *   e.g.	if the version of library is 4.9.1 then
 *   			function would return value 0x00040901
 */
DL_API
uint32_t AIS_GetLibraryVersion(void);

////////////////////////////////////////////////////////////////////

/**
 * Clear list of available devices for checking
 *
 */
DL_API
void AIS_List_EraseAllDevicesForCheck(void);

/**
 * Set list of available AIS reader device types
 *
 * @param device_type device_e device type by internal specification (enumeration)
 * @param device_id int Reader ID - set by Mifare Init Card
 * @return DL_STATUS
 */
DL_API
DL_STATUS AIS_List_AddDeviceForCheck(device_e device_type, int device_id);

/**
 * Remove specific reader type from list for checking
 *
 * @param device_type device_e device type by internal specification (enumeration)
 * @param device_id int Reader ID - set by Mifare Init Card
 * @return DL_STATUS
 */
DL_API
DL_STATUS AIS_List_EraseDeviceForCheck(device_e device_type, int device_id);

/**
 * Function return which device will be checked.
 *
 * Return pointer to allocated space on heap.
 *
 * @return pair of Device type and ID on the bus delimited with ':'
 * 		Pairs of type:id are delimited with new line character
 */
DL_API
c_string AIS_List_GetDevicesForCheck(void);

/**
 *
 * @param device_count number of attached devices
 * @return
 */
DL_API
DL_STATUS AIS_List_UpdateAndGetCount(int *device_count);

/**
 *
 * @param pDevice_HND
 * @param pDevice_Serial
 * @param pDevice_Type : look at enum E_KNOWN_DEVICE_TYPES / device_e from the file : ais_readers_list.h
 * @param pDevice_ID
 * @param pDevice_FW_VER
 * @param pDevice_CommSpeed
 * @param pDevice_FTDI_Serial
 * @param pDevice_isOpened
 * @param pDevice_Status
 * @param pSystem_Status
 * @return
 */
DL_API
DL_STATUS AIS_List_GetInformation(    //
		HND_AIS *pDevice_HND, //// assigned Handle
		c_string *pDevice_Serial, //// device serial number
		int *pDevice_Type, //// device type - device identification in AIS database
		int *pDevice_ID, //// device identification number (master)
		int *pDevice_FW_VER, //// version of firmware
		int *pDevice_CommSpeed, //// communication speed
		c_string *pDevice_FTDI_Serial, //// FTDI COM port identification
		int *pDevice_isOpened, //// is Device opened
		int *pDevice_Status, //// actual device status
		int *pSystem_Status //// actual system status
		);

///////////////////////////////////////////////////////////////////////////////

/**
 * AIS_List_OpenByHandle
 *
 * @param device : const HND_AIS DeviceHandle
 *
 * @return
 */
DL_API
DL_STATUS AIS_Open(const HND_AIS device);

DL_API
DL_STATUS AIS_Close(HND_AIS device);

// kill object
DL_API
DL_STATUS AIS_Destroy(HND_AIS device);

// global reset service / library
DL_API
DL_STATUS AIS_Restart(HND_AIS device);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Info functions

DL_API
DL_STATUS AIS_GetVersion( //
		HND_AIS device, //
		int *hardware_type, //
		// TODO : + hardware version
		int *firmware_version // firmware version
		//		int *ais_type // unit type
		//		int *system_status // system status
		);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Main pump

/**
 *
 *
 * command
 * Use this function for long commands if you want to get percent of execution
 *
 * Example AIS_GetLog_Set() start dumping LOG - function with execution about 10 seconds
 *
 * @param device
 * @param RealTimeEvents	indicate new RealTimeEvent(s)
 * @param LogAvailable		indicate new data in log buffer
 * @param LogUnread		    indicate unread LOG from the device (Incremental LOG)
 * @param DeviceStatus		the device status flags
 * @param cmdResponses		indicate command finish
 * @param cmdPercent		indicate percent of command execution - progress
 * @param TimeoutOccurred	debug only
 * @param Status			additional status
 * @return
 */
DL_API
DL_STATUS AIS_MainLoop(HND_AIS device,
		// event part
		int *RealTimeEvents, //
		int *LogAvailable, //
		int *LogUnread,
		// command part
		int *cmdResponses, //
		int *cmdPercent, //
		// status part
		int *DeviceStatus, //
		int *TimeoutOccurred, //
		int *Status //
		);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Time functions

/**
 *
 * @param device
 * @param current_time	GMT timestamp
 * @param timezone		Seconds west of GMT
 * @param DST			is Daylight Saving Time used (If daylight-saving time is ever in use.)
 * @param offset		Seconds west of GMT if Daylight Saving Time used
 * @return
 */
DL_API
DL_STATUS AIS_GetTime(HND_AIS device, uint64_t *current_time, //
		int *timezone, int *DST, int *offset);

/**
 *
 * @param device
 * @param password
 * @param time_to_set	GMT timestamp
 * @param timezone		Seconds west of GMT
 * @param DST			is Daylight Saving Time used (If daylight-saving time is ever in use.)
 * @param offset		Seconds west of GMT if Daylight Saving Time used
 * @return
 */
DL_API
DL_STATUS AIS_SetTime(HND_AIS device, c_string password,
		const uint64_t time_to_set, //
		int timezone, int DST, int offset);

///////////////////////////////////////////////////////////////////////////////

DL_API
DL_STATUS AIS_BatteryGetInfo(HND_AIS device, int *battery_status,
		int *battery_available_percent);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Change password

DL_API
DL_STATUS AIS_ChangePassword(HND_AIS device, c_string old_password,
		c_string new_password);

///////////////////////////////////////////////////////////////////////////////
// XXX :: RTE functions

DL_API
int AIS_ReadRTE_Count(HND_AIS device);

DL_API
DL_STATUS AIS_ReadRTE( //
		HND_AIS device, //
		int * log_index, //
		int * log_action, //
		int * log_reader_id, //
		int * log_card_id, //
		int * log_system_id, //
		uint8_t nfc_uid[NFC_UID_MAX_LEN], //
		int * nfc_uid_len, //
		uint64_t * timestamp //
		);

///////////////////////////////////////////////////////////////////////////////
// XXX :: LOG functions

/**
 * Non-blocking function, must polling (execute) AIS_MainLoop(),
 *    and wait for command_finish become not null (true).
 *    Percent of execution - progress are available too.
 *
 * @param device
 * @param password
 * @return
 */
DL_API
DL_STATUS AIS_GetLog(HND_AIS device, c_string password);

/**
 * Non-blocking function, must polling (execute) AIS_MainLoop(),
 *    and wait for command_finish become not null (true).
 *    Percent of execution - progress are available too.
 *
 * @param device
 * @param password
 * @param start_index
 * @param end_index
 * @return
 */
DL_API
DL_STATUS AIS_GetLogByIndex(HND_AIS device, c_string password,
		uint32_t start_index, uint32_t end_index);

/**
 * Non-blocking function, must polling (execute) AIS_MainLoop(),
 *    and wait for command_finish become not null (true).
 *    Percent of execution - progress are available too.
 *
 * @param device
 * @param password
 * @param time_from
 * @param time_to
 * @return
 */
DL_API
DL_STATUS AIS_GetLogByTime(HND_AIS device, c_string password,
		uint64_t time_from, uint64_t time_to);

// parsed
DL_API
int AIS_ReadLog_Count(HND_AIS device);

/**
 *
 * @param nfc_uid			must provide allocated memory space
 */
DL_API
DL_STATUS AIS_ReadLog( //
		HND_AIS device, //
		int * log_index, //
		int * log_action, //
		int * log_reader_id, //
		int * log_card_id, //
		int * log_system_id, //
		uint8_t nfc_uid[NFC_UID_MAX_LEN], //
		int * nfc_uid_len, //
		uint64_t * timestamp //
		);

DL_API
DL_STATUS AIS_ClearLog(HND_AIS device);

//--- Incremental LOG system with acknowledge

/**
 * Incremental LOG system with acknowledge.
 *
 * Count unread LOG in device.
 *
 * WARNING: No need for this function from version 4.8.0
 *          MainLoop() have new arguments, the one is LogUnread.
 *          LogUnread is log_available.
 *
 * @param device
 * @param log_available how many unread log available in device
 * @return status of function execution
 */
DL_API
DL_STATUS AIS_UnreadLOG_Count(HND_AIS device, uint32_t *log_available);

/**
 * Incremental LOG system with acknowledge
 *
 * Get only one unread LOG from the device.
 *
 * After successful storing read LOG you must send ACK to device.
 * If you don't send acknowledge to the device,
 *   this function would always return same LOG
 *
 * @param device
 * @param log_index
 * @param log_action
 * @param log_reader_id
 * @param log_card_id
 * @param log_system_id
 * @param nfc_uid
 * @param nfc_uid_len
 * @param timestamp
 * @return
 */
DL_API
DL_STATUS AIS_UnreadLOG_Get(HND_AIS device, //
		int * log_index, //
		int * log_action, //
		int * log_reader_id, //
		int * log_card_id, //
		int * log_system_id, //
		uint8_t nfc_uid[NFC_UID_MAX_LEN], //
		int * nfc_uid_len, //
		uint64_t * timestamp //
		);

/**
 * Incremental LOG system with acknowledge
 *
 * Acknowledge to device that LOG is read and store successful.
 * If you don't ACK - AIS_UnreadLOG_Get() would always return the same LOG
 *
 * @param device
 * @param records_to_ack for future use
 * @return
 */
DL_API
DL_STATUS AIS_UnreadLOG_Ack(HND_AIS device, uint32_t records_to_ack);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Blacklist functions

/**
 * Non-blocking function, must polling (execute) AIS_MainLoop(),
 *    and wait for command_finish become not null (true).
 *    Percent of execution - progress are available too.
 *
 * @param device
 * @param password
 * @param str_csv_blacklist comma separated values, start from 1
 * @return
 */
DL_API
DL_STATUS AIS_Blacklist_Write(HND_AIS device, c_string password,
		c_string str_csv_blacklist);

/**
 * Blocking function, no need to polling (execute) AIS_MainLoop().
 *
 * @param device
 * @param password
 * @param str_csv_blacklist
 * @return
 */
DL_API
DL_STATUS AIS_Blacklist_Read(HND_AIS device, c_string password,
		c_string *str_csv_blacklist);

///////////////////////////////////////////////////////////////////////////////
// XXX :: Whitelist functions

/**
 * Non-blocking function, must polling (execute) AIS_MainLoop(),
 *    and wait for command_finish become not null (true).
 *    Percent of execution - progress are available too.
 *
 * @param device : see info about device handle
 * @param password : see info about password
 * @param str_csv_whitelist : eg. "54:A3:34:12, 12.34.56.78, 01234567"
 * 			HEX pairs in UID can be delimited with: ':' or '.' or none
 * 			UID separators: ',' or ';' or other white space
 * 			! NULL or blank string erase white list in device
 * 			UID size can be 4 or 7 bytes
 * @return
 */
DL_API
DL_STATUS AIS_Whitelist_Write(HND_AIS device, c_string password,
		c_string str_csv_whitelist);

/**
 * Blocking function, no need to polling (execute) AIS_MainLoop().
 *
 * @param device
 * @param password
 * @param csv_whitelist
 * @return
 */
DL_API
DL_STATUS AIS_Whitelist_Read(HND_AIS device, c_string password,
		c_string *csv_whitelist);

///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
// XRCA Base HD SDK

/**
 * Open Gate with BMR
 * or
 * Open Strike Gate with Base HD
 *
 * @param device
 * @param pulse_duration in milliseconds
 * @return
 */
DL_API
DL_STATUS AIS_LockOpen(HND_AIS device, uint32_t pulse_duration);

DL_API
DL_STATUS AIS_RelayStateSet(HND_AIS device, uint32_t state);

DL_API
DL_STATUS AIS_GetIoState(HND_AIS device, uint32_t *intercom, uint32_t *door,
		uint32_t *relay_state);

/**
 *
 * set value for light: 0 = off, not null = on
 * @param device
 * @param green_master control green light on master unit
 * @param red_master control red light on master unit
 * @param green_slave control green light on slave unit
 * @param red_slave control red light on slave unit
 * @return
 */
DL_API
DL_STATUS AIS_LightControl(HND_AIS device, //
		uint32_t green_master, uint32_t red_master, //
		uint32_t green_slave, uint32_t red_slave);
///////////////////////////////////////////////////////////////////////////////
// IO Expander

/**
 * Get status about all I/O ports from one IO Expander
 *
 * @param device
 * @param in_count how menu I/O ports are available, and valid in the array
 * @param in_array static array one byte is one I/O port
 * @return
 */
DL_API
DL_STATUS AIS_IOExpander_GetStates(HND_AIS device, uint32_t *in_count, uint8_t **in_array);

/**
 * Send trigger to given position
 *
 * @param device
 * @param position
 * @return
 */
DL_API
DL_STATUS AIS_IOExpander_Set(HND_AIS device, uint32_t position);

///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
//// Functions for prevent writing to the EEPROM

/**
 * Prevent writing into the EEPROM W sectors (keys, passwords or configurations)
 *
 * Affected to the functions for changing configuration, write keys, etc.
 *
 * EE_WriteLock()
 *
 * @param device
 * @param password
 * @return
 */
DL_API
DL_STATUS AIS_EE_WriteProtect(HND_AIS device, c_string password);

/**
 * Enable writing in the EEPROM W sectors.
 *
 * Affected to the functions for changing configuration, write keys, etc.
 *
 * EE_WriteUnlock()
 *
 * @param device
 * @param password
 * @return
 */
DL_API
DL_STATUS AIS_EE_WriteUnProtect(HND_AIS device, c_string password);

///////////////////////////////////////////////////////////////////////////////

/**
 * definition for pointer of Call back function
 * function prototype like : void print_percent(int percent_from_0_to_100);
 *
 * @param
 * @return
 */
typedef void (*F_PROGRESS)(int percent);

/**
 * Update Firmware of the device.
 *
 * Blocking function for firmware update.
 *
 * @param device
 * @param firmware_bin_filename file name of the BIN file
 * @param CB_progress_f : pointer to the progress function,
 *              NULL - without progress function
 * @return
 */
DL_API
DL_STATUS AIS_FW_Update(HND_AIS device, c_string firmware_bin_filename,
		F_PROGRESS CB_progress_f);

///////////////////////////////////////////////////////////////////////////////

/**
 * Send configuration from file to the device
 *
 * @param device
 * @param config_bin_filename configuration input filename
 * @return
 */
DL_API
DL_STATUS AIS_Config_Send(HND_AIS device, c_string config_bin_filename);

/**
 * Read config from device into the file
 *
 * @param device
 * @param password
 * @param config_bin_filename configuration output filename
 * @return
 */
DL_API
DL_STATUS AIS_Config_Read(HND_AIS device, c_string password, c_string config_bin_filename);

///////////////////////////////////////////////////////////////////////////////
//// Helper functions

/***********************************************/
/** Helper function for FTDI serial converter **/

/**
 * Assign address where FTDI serial ( type: C-string ) are stored
 *
 * @param device
 * @param p_p_ftdi_serial
 * @return
 */
DL_API
DL_STATUS AIS_GetFTDISerial(HND_AIS device, char ** p_p_ftdi_serial);

/**
 * Assign address where FTDI handle ( type: void * ) are stored
 *
 * @param device
 * @param ftdi_handle
 * @return
 */
DL_API
DL_STATUS AIS_GetFTDIHandle(HND_AIS device, void **ftdi_handle);

/**
 * Assign address where FTDI serial ( type: C-string ) are stored,
 * and assign address where FTDI handle ( type: void * ) are stored
 *
 * @param device
 * @param ftdi_serial
 * @param ftdi_handle
 * @return
 */
DL_API
DL_STATUS AIS_GetFTDIInfo(HND_AIS device, char **ftdi_serial, void **ftdi_handle);

///////////////////////////////////////////////////////////////////////////////

DL_API
DL_STATUS AIS_GetDeviceResetCounter(HND_AIS device, uint32_t *reset_counter);

/**
 *
 * @param device_status
 * @return pointer to static C string with parsed device status value
 */
DL_API
c_string dbg_DeviceStatus2Str(int device_status);

///////////////////////////////////////////////////////////////////////////////

/************************************************/
/** Helper function for time-zone manipulation **/

/**
 * return Seconds west of GMT
 */
DL_API
long sys_get_timezone(void);

DL_API
int sys_get_daylight(void);

// _Daylight_savings_bias
// FIXME : document work on platform... SDK...
DL_API
long sys_get_dstbias(void);

DL_API
c_string sys_get_timezone_info(void);
/*****************************************/

/**
 * ERROR description
 * Get C-string info about status
 *
 * @param status
 * @return
 */
DL_API
c_string dl_status2str(DL_STATUS status);

DL_API
c_string dbg_status2str(DL_STATUS status);

/**
 * Simple helper function
 *
 * Concatenate pre_msg and status string
 *
 * @param status
 * @param pre_msg
 * @return
 */
DL_API
c_string dbg_prn_status(DL_STATUS status, c_string pre_msg);

/**
 * Get card action in C-string representation
 *
 * @param action
 * @return
 */
DL_API
c_string dbg_action2str(e_card_action action);

/**
 * Parse given timestamp in format
 * "GMT=timestamp_decimal, timestamp long date format"
 * e.g. "GMT= 1455378371, Sat Feb 13 15:46:11 2016"
 *
 * @param gm_timestamp GMT / timestamp
 * @return pointer to static array of characters ( C string )
 */
DL_API
c_string dbg_GMT2str(uint64_t gm_timestamp);

/**
 * Get informations about supported device type by AIS READERS library.
 *
 * If you don't wont specific information set argument to 0.
 *   e.g. if you need only string description for DL_AIS_BMR, type:
 * @code
 *   c_string device_description;
 *   DL_STATUS status = dbg_device_type(DL_AIS_BMR, 0, &device_description, 0, 0, 0, 0, 0);
 *   if (status == DL_OK)
 *   {
 *   	printf("DL_AIS_BMR is %s\n", device_description);
 *   }
 *   else
 *   {
 *   	printf("Wrong device type - not supported in the library.\n");
 *   }
 * @endcode
 *
 * @param dev_type
 * @param name short name
 * @param description device description - full name
 * @param hw_type hardware type in D-LOGIC device enumeration
 * @param speed communication speed of the device
 * @param rte_test how often library test RTE in the device ( in ms )
 * @param is_half_duplex is device half duplex ( if 0 then full-duplex )
 * @param is_alone_on_the_bus only one device on the bus
 * @return error ITEM_NOT_VALID if dev_type not supported
 */
DL_API
DL_STATUS dbg_device_type(IN device_e dev_type, OUT c_string *name,
		OUT c_string *description, OUT uint32_t *hw_type, OUT uint32_t *speed,
		OUT uint32_t *rte_test, OUT uint32_t *is_half_duplex,
		OUT uint32_t *is_alone_on_the_bus);

/**
 * Translate enumeration E_KNOWN_DEVICE_TYPES
 * from string representation to the integer ( enum )
 * e.g. "DL_AIS_BMR" to enum value 9
 *
 * @param dev_type_str
 * @param dev_type_enum
 * @return
 */
DL_API
DL_STATUS device_type_str2enum(IN c_string dev_type_str,
		OUT device_e *dev_type_enum);

/**
 * Translate enumeration E_KNOWN_DEVICE_TYPES
 * from enumeration ( integer ) to the string pointer
 * e.g. 9 translate to pointer to string "DL_AIS_BMR"
 *
 * @param dev_type_enum
 * @param dev_type_str
 * @return
 */
DL_API
DL_STATUS device_type_enum2str(IN device_e dev_type_enum,
		OUT c_string *dev_type_str);

///////////////////////////////////////////////////////////////////////////////
#if defined(DL_API_EXPORTS) || defined(DL_API_STATIC)
#	include "ais_readers_undoc.h"
#endif
///////////////////////////////////////////////////////////////////////////////

#endif /* AIS_READERS_H_ */
