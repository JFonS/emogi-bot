f = open("color2emogi.txt","r")
o = open("color2emogiREMAP.txt", "w")
color2emoji = []

def remap(n, currMin, currMax, newMin, newMax):
    return (n - currMin) / (currMax - currMin) * (newMax - newMin) + newMin

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

lines = f.readlines()
for line in lines:
	data = line.split(" ")
	data[1] = int(translate(int(data[1]), 83, 255, 0, 255))
	data[2] = int(translate(int(data[2]), 83, 255, 0, 255))
	data[3] = int(translate(int(data[3]), 83, 255, 0, 255))
	l = ' '.join(str(e) for e in data)
	o.write(l)

f.close()
o.close()