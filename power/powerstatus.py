#!/usr/bin/python
## Read some values from the PMIC and print out what we find
### example i2cget -y -f  0 0x24 0x3

import subprocess

I2C_DEVICE = 0

CHIP_ADDRESS = 0x24

# register addresses we are interested in
PPATH = 0x1
CHGCONFIG0 = 0x3


STATUS = 0xA
PGOOD = 0xC

# some bitmasks

STATUS_AC = 1<<3
STATUS_USB = 1<<2

CHGCONFIG0_ACTIVE = 1<<3 # we are charging the battery

# these labels are interpreted from the TPS65217 datasheet
CHG0_LABELS = ["Temp sense error","Pre-charge Timedout","Charge Timedout","Active (charging)","Charge Termination Current","Thermal Suspend", "DPPM Reduction","Thermal Regulation"]
STATUS_LABELS=["Push Button",None,"USB Power", "AC Power"]# skip the rest
PGOOD_LABELS=["LDO2 power-good","LDO1 power-good","DCDC3 power-good","DCDC2 power-good","DCDC1 power-good", "LDO4 power-good","LDO3 power-good"]


# get the I2C register, strip off \n and cast to int from hex
# -y means non-interactive mode (just do it!)
# -f forces the connection
def query(reg=0):
    return  int(subprocess.check_output(["i2cget","-y" ,"-f", str(I2C_DEVICE), str(CHIP_ADDRESS), str(reg)]).strip(),16)

# display value of each bit in the register, along with its label
def describe_bits(val,labels):
    for x in range(0,len(labels)):
        if(not labels[x]): # skip None labels
            continue
        msk = 1<<x
        print "%s = %d"%(labels[x],(val&msk)!=0)


# query a register, print out value breakdown
def show_reg(reg,title,labels):
    val = query(reg)
    print
    print "%s: r[0x%x]=0x%x\r\n"%(title,reg,val)
    describe_bits(val,labels)
    print 

# specific helpers
def onBattery():
    return query(STATUS) & (STATUS_AC | STATUS_USB) == 0
    
def charging():
    return query(CHGCONFIG0) & (CHGCONFIG0_ACTIVE) !=0
 
  
if __name__ == "__main__":
    
    print "Querying Beaglebone Black Power Management IC on i2c-%s device 0x%x"%(I2C_DEVICE, CHIP_ADDRESS)
    
    print "On battery power only? %d\r\n"%onBattery()
    print "Charging Battery? %d\r\n"%charging()

    show_reg(STATUS,"STATUS",STATUS_LABELS)

    show_reg(CHGCONFIG0,"CHARGER",CHG0_LABELS)

    show_reg(PGOOD,"PGOOD",PGOOD_LABELS)


  
