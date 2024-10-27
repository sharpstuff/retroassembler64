import math

# Create a sine wave with 360 values, offset by 128
sine_wave = [int(128 + 127 * math.sin(math.radians(angle))) for angle in range(360)]

idx = 1
output = ""

for b in sine_wave:

	if ( idx % 8 == 1 ):
		output = output + ".byte "

	output = output + "$" + '{:02x}'.format(b) + " "
	
	if ( idx % 8 == 0 ):
		output = output + "\n"

	idx = idx + 1

print (output)