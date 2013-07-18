#!/usr/bin/env python
# shutdown the system when we are on battery power for awhile

import logging
import logging.handlers


import sys, time
from daemon import Daemon
import powerstatus # Beaglebone's PMIC
import os
def ledOn(n=1):
    if(n<0 or n>3):
        return
    os.system("echo none > /sys/class/leds/beaglebone:green:usr%d/trigger"%n)
    os.system("echo 255 > /sys/class/leds/beaglebone:green:usr%d/brightness"%n)

def ledOff(n=1):
    if(n<0 or n>3):
        return
    os.system("echo none > /sys/class/leds/beaglebone:green:usr%d/trigger"%n)
    os.system("echo 0 > /sys/class/leds/beaglebone:green:usr%d/brightness"%n)

def fixLEDs():
    triggers=["heartbeat","mmc0","cpu0","mmc1"]
    n=0
    for t in triggers:
        os.system("echo %s > /sys/class/leds/beaglebone:green:usr%d/trigger"%(t,n))
        n+=1

def flashLEDs(n=6, period=0.5, leds=[2,3]):
    # flash it!
    for x in range(0,n):
        for led in leds:
            ledOn(led)
        time.sleep(period)
        for led in leds:
            ledOff(led)
        time.sleep(period)
        
class SafeShutdownDaemon(Daemon):
        def stopping(self):
            fixLEDs();
                      
        def run(self):
                my_logger = logging.getLogger('Safe Shutdown Service')
                my_logger.setLevel(logging.INFO)
                handler = logging.handlers.SysLogHandler(address = '/dev/log')
                my_logger.addHandler(handler)

                my_logger.info("Starting Safe Shutdown and Charge Monitor")
                
                fixLEDs()
                
                
                BATT_SHUTDOWN_S=10
                lastNotifySecond=0
                notifyMod = int(BATT_SHUTDOWN_S / 5.0) # notify five times in log

                timeOnBattery = 0;
                lastOnBattery = 0
                onBattery = False
                charging=False
                tmpCharging=False
                tmpBattery = False
                
                while True:
                        tmpBattery = powerstatus.onBattery()
                        tmpCharging = powerstatus.charging()
                        
                        ledOn(2) if(tmpBattery) else ledOff(2)
                        ledOn(3) if(tmpCharging) else ledOff(3)
                        if(charging!=tmpCharging):
                            msg = "Started Charging Battery" if tmpCharging else "Stopped Charging Battery"
                            my_logger.info(msg)
                         
                        if(onBattery!= tmpBattery):
                            lastOnBattery=time.time() # start counting
                            msg = "Switched to Battery Power" if tmpBattery else "Switched to wired power"
                            my_logger.info(msg)
                            
                        
                        onBattery=tmpBattery
                        charging=tmpCharging
                        
                        if(onBattery):
                            timeOnBattery+=(time.time()-lastOnBattery)
                            lastOnBattery=time.time()

                            if(timeOnBattery > BATT_SHUTDOWN_S):
                                my_logger.info("On Battery power for %d secs - shutdown NOW!"%timeOnBattery)
                                flashLEDs(n=4, period=0.5, leds=[0,1,2,3])
                                fixLEDs()
                                os.system("shutdown now")

                            elif(int(timeOnBattery) > lastNotifySecond and int(timeOnBattery)%notifyMod ==0):
                                lastNotifySecond=int(timeOnBattery)
                                my_logger.info("On Battery Power -- auto-shutdown in %d seconds"%(BATT_SHUTDOWN_S-int(timeOnBattery)))
                            time.sleep(0.5)
                        else: 
                            timeOnBattery=0
                            time.sleep(5)
                        
                       
 
if __name__ == "__main__":
        daemon = SafeShutdownDaemon('/tmp/safe-shutdown-daemon.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        print "Starting safe shutdown script"
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        print "Stopping safe shutdown"
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        print "Restarting safe shutdown"
                        daemon.restart()
                elif 'test' == sys.argv[1]:
                        print "Running daemon directly for testing"
                        daemon.run()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
               # print "usage: %s start|stop|restart" % sys.argv[0]
               daemon.start(True)