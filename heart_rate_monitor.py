from machine import Pin, Signal, ADC
# Write your code here :-)
adc = ADC(0)

# On my board on = off, need to reverse.
led = Signal(Pin(2, Pin.OUT), invert=True)

MAX_HISTORY = 250

# Maintain a log of previous values to
# determine min, max and threshold.
history = []

while True:
    v = adc.read()

history.append(v)
