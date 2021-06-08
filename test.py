a = "0000100000001000"

octets = []
for i in range(0, len(a), 8):
    octets.append(int(a[i:i + 8], 2))


f1 = open("test.txt", 'w')
f1.write(str(16) + "|\n")
f1.close()
f2 = open("test.txt", 'ab')
f2.write(bytearray(octets))
f2.close()
f3 = open("test.txt", 'r')
C = f3.readline()
f3.close()
f4 = open("test.txt", 'rb')
D = f4.read()
f4.close()
print(C)
print(D)
E=D.split(b'|\r\n')
print(E)

