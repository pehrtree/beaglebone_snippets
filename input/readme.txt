beagle with Linux uses the event-driven device input system.
things like joysticks show up in /dev/input/event0, etc
we can use python and the pyevdev library to easily query them.

python evdevlist.py will query all input devices and print out their capabilities. 
This should work on any modern Linux system not just Beagle.


Below is sample output showing the default event0 which is the power button from the PMIC

/dev/input/event0    tps65217_pwr_but                 
        Event types [('EV_KEY', 1L), ('EV_SYN', 0L)]: 
        1 Buttons:
                0: ('KEY_POWER', 116L)
        0 Relative Axes:
        0 Absolute Axes:
        0 Misc Events:
                []
        6 Sync Events:
                [('SYN_REPORT', 0L), ('SYN_CONFIG', 1L), ('?', 761L), ('?', 762L), ('?', 764L), ('?', 765L)]
        0 Forcefeedback capabilities:
                []
        HID LEDs: []
