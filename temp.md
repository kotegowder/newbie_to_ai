
# Porting Guide - TBSA-v8M Architecture test suite 
-----------------------------------------------------

## Introduction
The TBSA-v8M Architecture test suite contains a platform abstraction layer (PAL) which abstracts platform specific information from the tests.
 - The PAL layer interface functions need to be implemented/ported to the target platform.
 - The target config file must be created/updated to match the details of the target platform.

This document provides details on the porting steps and the PAL APIs.

## Porting steps

### Target configuration

  You must populate your system configuration and provide it as an input to test suite.

This is captured in a single static input configuration file that is named as tbsa_tgt.cfg. This file is available at syscomp_tbsa_m/platform/board/<platform_name>/. <br />

An example of the input configuration file is as shown.

	//PERIPHERALS
	timer.num = 2;
	timer.0.vendor_id = 0x0;
	timer.0.device_id = 0x0;
	timer.0.base = 0x50000000;
	timer.0.intr_id = 0x8;
	timer.0.attribute = SECURE_PROGRAMMABLE;
	//MEMORY
	sram.num = 2;
	sram.1.start = 0x30000000;
	sram.1.end = 0x303FFFFF;
	sram.1.attribute = MEM_SECURE;
	sram.1.mem_type = TYPE_NORMAL_READ_WRITE;
	sram.1.dpm_index = 0;

  More details on the structure of the input can be obtained from val/include/val_target.h.


### Create a new target

  Since TBSA-v8M test suite is agnostic to various system targets, before building the tests, you must port the files mentioned in the following steps.

**Procedure**
----------------
  - Create a new directory in platform/board/<platform_name>. For reference, see the existing platform fvp.
  - The peripheral code exists inside platform/peripherals/<peripheral_name>. If <platform_name> is using the peripherals that already exist in platform/peripherals/<peripheral_name>,
    then this code can be reused. Otherwise, the code must be ported for platform specific peripherals.
  - Update platform/board/<platform_name>/Makefile with the appropriate path of the peripherals used.
  - Update platform/board/<platform_name>/src/pal_baremetal_intf.c or pal_cmsis_intf.c with the correct instance of the peripherals used.
  - Update the primary input for the TBSA-v8M tests, that is, target configuration file in platform/board/<platform_name>/tbsa_tgt.cfg. Use platform/boards/fvp/tbsa_tgt.cfg as reference.
  - Refer val/include/val_target.h for structure details.

**Note**:
  pal_nvram_read and pal_nvram_write of the reference FVP platform code simulate non-volatility of the data across resets by ensuring that the memory range is not initialized across warm boots.
  A partner board may choose to simulate the same or provide NVRAM using external storage or Internal Flash.

## PAL API list
  These functions will require implementation/porting to the target platform. <br />

**Note**:  
The NVIC functions are CMSIS compliant. The CMSIS repository on Github is cloned during build. A partner need not port the NVIC functions if there are no platform specific changes.

| No |  Prototype   |  Description  |   Parameters  |
|----|--|---|---|
| 01 |  void pal_NVIC_EnableIRQ(uint32_t intr_num); |  Enable Interrupt |  intr_num: Interrupt number   |
| 02 |  void pal_NVIC_DisableIRQ(uint32_t intr_num);    |  Disable Interrupt    |  intr_num: Interrupt number   |
| 03 |  uint32_t pal_NVIC_ClearTargetState(uint32_t intr_num);  |  Clear Interrupt Target State |  intr_num: Interrupt number   |
| 04 |  void pal_NVIC_SetPriority(uint32_t intr_num, uint32_t priority);    |  Set Interrupt Priority   |  intr_num: Interrupt number   |
|    |  |   |  priority: Priority to set    |
| 05 |  uint32_t pal_NVIC_GetPriority(uint32_t intr_num);   |  Get Interrupt Priority   |  intr_num: Interrupt number   |
| 06 |  void pal_NVIC_SetPendingIRQ(uint32_t intr_num); |  Set Pending Interrupt    |  intr_num: Interrupt number   |
| 07 |  void pal_NVIC_ClearPendingIRQ(uint32_t intr_num);   |  Clear Pending Interrupt  |  intr_num: Interrupt number   |
| 08 |  uint32_t pal_NVIC_GetPendingIRQ(uint32_t intr_num); |  Get Pending Interrupt    |  intr_num: Interrupt number   |
| 09 |  uint32_t pal_NVIC_GetActive(uint32_t intr_num); |  Get Active Interrupt |  intr_num: Interrupt number   |
| 10 |  int32_t pal_i2c_init(addr_t addr);  |   Initialize I2C peripheral   |   addr : Address of the peripheral    |
| 11 |  int32_t  pal_i2c_read(uint32_t slv_addr, uint8_t \*rd_data, uint32_t len);   |  Read peripheral using I2C   |   slv_addr: Slave address |
|    |  |   |   rd_data : Pointer to buffer for data to receive from I2C Slave  |
|    |  |   |   num     : Number of data bytes to receive   |
| 12 |   int32_t  pal_i2c_write(uint32_t slv_addr, uint8_t \*wr_data, uint32_t num); |  Read peripheral using I2C   |   slv_addr: Slave address |
|    |  |   |   wr_data : Pointer to buffer with data to transmit to I2C slave  |
|    |  |   |   num     : Number of bytes to transfer   |
| 13 |  int32_t pal_spi_init(addr_t addr);  |  Initialize SPI peripheral    |   addr : Address of the peripheral    |
| 14 |  int32_t  pal_spi_read(addr_t addr, void \*data, uint32_t num);  |  Read peripheral using SPI commands   |   addr : Address of the peripheral    |
|    |  |   |   data : Read buffer  |
|    |  |   |   num  : Number of bytes to receive   |
| 15 |  int32_t  pal_spi_write(addr_t addr, const void \*data, uint32_t num);   |  Write peripheral using SPI commands  |   addr : address of the peripheral    |
|    |  |   |   data : write buffer |
|    |  |   |   num  : Number of bytes to transfer  |
| 16 |  int  pal_timer_init(addr_t addr, uint32_t time_us, uint32_t timer_tick_us); |  Initializes a hardware timer |   addr          : Address of the peripheral   |
|    |  |   |   time_us       : Time in micro seconds   |
|    |  |   |   timer_tick_us : Number of ticks per micro seconds   |
| 17 |  int  pal_timer_enable(addr_t addr); |   Enables a hardware timer    |   addr : Address of the peripheral    |
| 18 |  int  pal_timer_disable(addr_t addr);    |   Disables a hardware timer   |   addr : Address of the peripheral    |
| 19 |  int  pal_timer_interrupt_clear(addr_t addr);    |   Clears the interrupt status of timer    |   addr : Address of the peripheral    |
| 20 |  int  pal_wd_timer_init(addr_t addr, uint32_t time_us, uint32_t timer_tick_us);  |   Initializes a hardware watchdog timer   |   addr          : Address of the peripheral   |
|    |  |   |   time_us       : Time in micro seconds   |
|    |  |   |   timer_tick_us : Number of ticks per micro second    |
| 21 |  int  pal_wd_timer_enable(addr_t addr);  |   Enables a hardware watchdog timer   |   addr : Address of the peripheral    |
| 22 |  int  pal_wd_timer_disable(addr_t addr); |   Disables a hardware watchdog timer  |   addr : Address of the peripheral    |
| 23 |  int  pal_is_wd_timer_enabled(addr_t addr);  |   Checks whether hardware watchdog timer is enabled   |   addr : Address of the peripheral    |
| 24 |  void pal_crypto_init(addr_t crypto_base_addr);  |   Initializes the cryptographic functions |   crypto_base_addr : base address of the crypto module    |
| 25 |  int  pal_crypto_aes_generate_key(uint8_t \*key, uint32_t size); |   Generates AES key using various specified entropy sources   |   key  : The buffer where the generated key is stored |
|    |  |   |   size : Size of the key to be generated. Valid options are:  |
|    |  |   |          - 128 bits   |
|    |  |   |          - 192 bits   |
|    |  |   |          - 256 bits   |
| 26 |  int  pal_crypto_compute_hash(unsigned char \*input, size_t ilen, unsigned char \*output, int algo); |   Calculates the SHA-224 or SHA-256 checksum of a buffer. |   input   : The buffer holding the data.  |
|    |  |   |   ilen    : The length of the input data. |
|    |  |   |   output  : The SHA-224 or SHA-256 checksum result.   |
|    |  |   |   algo    : Determines which function to use  |
|    |  |   |             0: Use SHA-256.   |
|    |  |   |             1: Use SHA-224.   |
| 27 |  void \*uart_get_cmsis_driver(addr_t addr);  |   Gets the CMSIS structure address    |   addr : Address of the peripheral    |
| 28 |  int32_t pal_uart_init(addr_t addr); |   This function initializes the uart  |   addr : Address of the peripheral    |
| 29 |  int32_t pal_uart_tx(addr_t addr, const void \*data, uint32_t num);  |   Send data to UART TX FIFO   |   addr : Address of the peripheral    |
|    |  |   |   data : Data to be written to TX FIFO    |
|    |  |   |   num  : Number of bytes  |
| 30 |  void \*pal_get_target_cfg_start(void);  |   Provides the database source location   |   |
| 31 |  int  pal_nvram_write(addr_t base, uint32_t offset, void \*buffer, int size);    |   Writes 'size' bytes from buffer into NVRAM at a given 'base + offset'.  |   base      : Base address of NVRAM   |
|    |  |   |   offset    : Offset  |
|    |  |   |   buffer    : Pointer to source address   |
|    |  |   |   size      : Number of bytes |
| 32 |  int  pal_nvram_read(addr_t base, uint32_t offset, void \*buffer, int size); |   Reads 'size' bytes from NVRAM at a given 'base + offset' into given buffer  |   base      : Base address of NVRAM   |
|    |  |   |   offset    : Offset  |
|    |  |   |   buffer    : Pointer to source address   |
|    |  |   |   size      : Number of bytes |
| 33 |  void  pal_system_warm_reset(void);  |   Generates system warm reset.    |   |
| 34 |  void  pal_system_cold_reset(void);  |   Generates system cold reset.    |   |
| 35 |  int  pal_is_cold_reset(void);   |   |   |
| 36 |  int  pal_is_warm_reset(void);   |   |   |
| 37 |  int pal_dpm_set_access_ns_only(uint32_t index, bool_t access_ns);   |   Set the debug permission based on the input arg |   index          : DPM index  |
|    |  |   |   access_ns      : TRUE  - allow debug access only for non-secure address |
|    |  |   |                    FALSE - allow debug access to both secure and non-secure addresses |
| 38 |  int pal_mpc_configure_mem_to_nonsecure(addr_t start_addr,addr_t end_addr);  |   Allow a memory region to be configured as Non-Secure via MPC    |    start_addr : Start of memory address to be configured by MPC   |
|    |  |   |   end_addr   : End of memory address to be configured by MPC  |
| 39 |  int pal_mpc_configure_mem_to_secure (addr_t start_addr,addr_t end_addr);    |   Allow a memory region to be configured as Secure via MPC    |   start_addr : Start of memory address to be configured by MPC    |
|    |  |   |   end_addr   : End of memory address to be configured by MPC |
| 40 |  int pal_fuse_read(addr_t addr, uint32_t \*data, size_t size);   |  Read the value of given fuse address |   addr     : Address of the fuse  |
|    |  |   |   data     : Buffer to store the data |
|    |  |   |   size     : Number of words to be read   |
| 41 |  int pal_fuse_write(addr_t addr, uint32_t \*data, size_t size);  |  Write the value in given fuse address    |   addr     : Address of the fuse  |
|    |  |   |   data     : Data to be written   |
|    |  |   |   size     : Number of words to write |
| 42 |  int pal_fuse_count_zeros_in_rotpk(uint32_t \*zero_cnt); |  Count the number of Zeros in ROTPK   |   zero_cnt : Buffer to store the zero count   |
| 43 |  void pal_fuse_count_zeros(uint32_t value, uint32_t \*zero_cnt); |  Count the number of Zeros in the given value    |   value    : Number of zeros to be determined |
|    |  |   |   zero_cnt : Buffer to store the zero count   |
| 44 |  int pal_fuse_get_lcs(uint32_t \*pLcs);   |  Reads the LCS register  |   pLcs : Buffer to store the LCS value    |
| 45 |  int pal_crypto_validate_certificate(uint32_t certificate_base_addr, uint32_t public_key_addr, uint32_t certificate_size, uint32_t public_key_size); |   Validates the certificate using public key. |   certificate_base_addr : Base address of the certificate where it is stored in memory    |
|    |  |   |   public_key_addr       : Base address of the public key where it is stored in memory |
|    |  |   |   certificate_size      : Certificate memory size |
|    |  |   |   public_key_size       : Public key memory size  |
| 46 |  int pal_crypto_get_uniqueID_from_certificate(uint32_t certificate_base_addr, uint32_t public_key_addr, uint32_t certificate_size, uint32_t public_key_size);    |   Get unique ID from valid certificate using public key   |   certificate_base_addr : Base address of the certificate where it is stored in memory    |
|    |  |   |   public_key_addr       : Base address of the public key where it is stored in memory  |
|    |  |   |   certificate_size      : Certificate memory size |
|    |  |   |   public_key_size       : Public key memory size  |
| 47 |  int pal_rtc_init(addr_t addr);  |   Initialize RTC  |   addr : Address of peripheral    |
| 48 |  int pal_is_rtc_trustable(addr_t addr);  |   RTC validity mechanism to indicate RTC is Trusted/Non-trusted   |   addr : Address of peripheral    |
| 49 |  int pal_is_rtc_synced_to_server(addr_t addr);   |   RTC validity mechanism to indicate RTC is synced with server or not |   addr : Address of peripheral    |
| 50 |  int pal_crypto_get_dpm_from_key(uint32_t public_key_addr, uint32_t public_key_size, uint32_t \*dpm_field);   |  Get DPM field from public key   |   public_key_addr : Base address of the public key where it is stored in memory   |
|    |  |   |   public_key_size : Public key memory size    |
|    |  |   |   dpm_field       : Buffer to store DPM number    |
| 51 |  int pal_crypto_get_dpm_from_certificate(uint32_t certificate_base_addr, uint32_t certificate_size, uint32_t \*dpm_field);   |    Get DPM field from certificate |   certificate_base_addr : Base address of the certificate where it is stored in memory    |
|    |  |   |   certificate_size      : certificate memory size |
|    |  |   |   dpm_field             : Buffer to store DPM number  |
| 52 |  int pal_firmware_version_update(uint32_t instance, uint32_t firmware_version_type, uint32_t fw_ver_cnt);    |   Update the firmware version |   instance              : Instance of the firmware |
|    |  |   |   firmware_version_type : 0 - Trusted, 1 - Non-trusted    |
|    |  |   |   fw_ver_cnt            : Version of the firmware |
| 53 |  int pal_firmware_version_read(uint32_t instance, uint32_t firmware_version_type);   |   Read the firmware version   |   instance              : Instance of the firmware |
|    |  |   |   firmware_version_type : 0 - Trusted, 1 - Non-trusted    |

## License
Arm TBSA-v8M Architecture test suite is distributed under Apache v2.0 License.

--------------

*Copyright (c) 2018, Arm Limited and Contributors. All rights reserved.*