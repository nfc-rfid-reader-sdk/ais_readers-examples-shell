/*
 * ais_readers_list.h
 *
 *  Created on: 12.10.2015.
 *      Author: srkos
 */
#ifndef AIS_READERS_LIST_H_
#define AIS_READERS_LIST_H_

#include <limits.h>

typedef enum E_KNOWN_DEVICE_TYPES
{
	DL_UNKNOWN_DEVICE = 0,
	//--------------------
	DL_AIS_100,
	DL_AIS_20,
	DL_AIS_30,
	DL_AIS_35,
	DL_AIS_50,
	DL_AIS_110,
	DL_AIS_LOYALITY,
	DL_AIS_37, // AIS START == BASE BAT USB
	//--------------------
	DL_AIS_BMR, // Barcode NFC Reader, Half-Duplex

	DL_AIS_BASE_HD, // Base HD AIS old, Half-Duplex

	DL_AIS_BASE_HD_SDK, // Base HD AIS SDK, Half-Duplex

	DL_AIS_IO_EXTENDER,

	// ... new readers ...

	//--------------------
	DL_AIS_SYSTEM_TYPES_COUNT,
	//--------------------
	// patch to force enumeration to 32 bits
	Internal_ForceMyEnumIntSize = INT_MAX
	//--------------------
} device_e;

/**
 * See helper functions:
 *
 * dbg_device_type()
 *
 * device_type_str2enum()
 * device_type_enum2str()
 *
 */

#endif /* AIS_READERS_LIST_H_ */
