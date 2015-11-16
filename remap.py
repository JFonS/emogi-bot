f = open("color2emogi-sub.txt","r")
o = open("color2emogi-subREMAP.txt", "w")
color2emoji = []

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
    data[1] = int(translate(int(data[1]), 53, 255, 0, 255))
    data[2] = int(translate(int(data[2]), 53, 255, 0, 255))
    data[3] = int(translate(int(data[3]), 53, 255, 0, 255))

    data[4] = int(translate(int(data[4]), 53, 255, 0, 255))
    data[5] = int(translate(int(data[5]), 53, 255, 0, 255))
    data[6] = int(translate(int(data[6]), 53, 255, 0, 255))

    data[7] = int(translate(int(data[7]), 53, 255, 0, 255))
    data[8] = int(translate(int(data[8]), 53, 255, 0, 255))
    data[9] = int(translate(int(data[9]), 53, 255, 0, 255))

    data[10] = int(translate(int(data[10]), 53, 255, 0, 255))
    data[11] = int(translate(int(data[11]), 53, 255, 0, 255))
    data[12] = int(translate(int(data[12]), 53, 255, 0, 255))

    l = ' '.join(str(e) for e in data)
    o.write(l)

f.close()
o.close()