Beaglebone Black power management IC

TI TPS65217  http://www.ti.com/product/tps65217C

The chip on board the BBB has an I2C interface that tells us stuff about how it is being powered and if it is charging a battery.

[Using a battery]
Note that when hooking up a LiPo battery (such as the thin ones from Sparkfun)  you must make all the connections to enable charging:

TP5/BAT => Battery+
TP6/SENSE=> BAT pin on PCB
TP7/TS => 10K NTC thermistor to ground. Or perhaps a 10K resistor to fool it.
TP8/GND => Battery-

[Safe shutdown]
You can treat the battery like a UPS - when we detect we are on battery-only for too long, issue a safe linux shutdown command to prevent file system corruption.
See safe_shutdown.py for an example that can be used as a Linux daemon to run on startup.

[Reading the PMIC]
PMIC  is on I2C-0 address 0x24
Easy to get started: use i2cget from the shell to query specific registers. 
The specific register addresses and their meanings are in the datasheet.

Example: get the STATUS (0xA) register which tells us which power inputs (USB, AC) are active. 
If neither are true then we must be on battery! 

i2cget -y -f 0 0x24 0xA

powerstatus.py uses this easy shell cmd to query a couple useful regs and print the results

Sample output of powerstatus.py for an AC powered beagle with no battery:

Querying Beaglebone Black Power Management IC on i2c-0 device 0x24
On battery power only? 0

Charging Battery? 0


STATUS: r[0xa]=0x88

Push Button = 0
USB Power = 0
AC Power = 1


CHARGER: r[0x3]=0x1

Temp sense error = 1
Pre-charge Timedout = 0
Charge Timedout = 0
Active (charging) = 0
Charge Termination Current = 0
Thermal Suspend = 0
DPPM Reduction = 0
Thermal Regulation = 0


PGOOD: r[0xc]=0x7f

LDO2 power-good = 1
LDO1 power-good = 1
DCDC3 power-good = 1
DCDC2 power-good = 1
DCDC1 power-good = 1
LDO4 power-good = 1
LDO3 power-good = 1
