# Use pyevdev to query the /dev/input/event* devices and see what they support
# a helpful way to make sense of which one is which
#
# easy_install pyevdev
#

from evdev import InputDevice, list_devices,ecodes
devices = map(InputDevice, list_devices())

# print an entry with its index
# useful for buttons and axis where we think of them as 0-based
def printlist(lst):
    for idx,val in enumerate(lst):
        print "\t\t%d: %s"%(idx,val)

print
print "Look for /dev/input/event* devices:"
for dev in devices:
    print "="*40
    print( '%-20s %-32s %s' % (dev.fn, dev.name, dev.phys) )
    capav =dev.capabilities(True,True)
    capa =dev.capabilities(False,False)
  
    print "\tEvent types %s: "%(capav.keys()) # EV_KEY, EV_ABS, etc

    print "\t%d Buttons:"%len(capa.get(ecodes.EV_KEY,[]))
    printlist(capav.get(('EV_KEY', 1L),[]))
    
    print "\t%d Relative Axes:"%len(capa.get(ecodes.EV_REL,[]))
    printlist(capav.get(('EV_REL', 2L),[]))

    print "\t%d Absolute Axes:"%len(capa.get(ecodes.EV_ABS,[]))
    printlist(capav.get(('EV_ABS', 3L),[]))
   
    print "\t%d Misc Events:"%len(capa.get(ecodes.EV_MSC,[]))
    print "\t\t%s"%capav.get(('EV_MSC', 4L),[])
    
    print "\t%d Sync Events:"%len(capa.get(ecodes.EV_SYN,[]))
    print "\t\t%s"%capav.get(('EV_SYN', 0L),[])
   
    print "\t%d Forcefeedback capabilities:"%len(capa.get(ecodes.EV_FF,[]))
    print "\t\t%s"%capav.get(('EV_FF', 21L),[])  
   
    print "\tHID LEDs: %s"%dev.leds(verbose=True)
    print

