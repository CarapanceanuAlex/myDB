import struct
def main():
    recordSize = 50
    rowNr = 5
    formatString = "i46s"
    rows = [(1, b"Alex"), (2, b"Edi"), (3, b"Bazinga")]
    #writeToFile("data.bin", formatString, rows)
    readFromFile("data.bin", formatString, recordSize, rowNr)

def writeToFile(file, format, data_list):
    with open(file, "wb") as f:
        for entry in data_list:
            packed = struct.pack(format, entry[0], entry[1])
            f.write(packed)
    return packed

def readFromFile(file, format, recordSize, rowNr):
    with open(file, "rb") as f:
        f.seek(recordSize * rowNr)
        rawBytes = f.read(recordSize)
    unpacked = struct.unpack(format, rawBytes)
    rawData = unpacked[1]
    cleanData = rawData.decode('utf-8').strip('\x00')
    print("Data from file, read: " + cleanData)

if __name__ == "__main__":
    main()

"""
formatString = "i20s"
packed = struct.pack(formatString, 42, b"hello")
#--------------------------------------------------------------------------------------------------------------------------------------
unpacked = struct.unpack(formatString, packed)
rawName = unpacked[1]
cleanName = rawName.decode('utf-8').strip('\x00') #or use rstrip(b'\x00') to actually remove the zero-bytes and then decode
print(len(cleanName))
#--------------------------------------------------------------------------------------------------------------------------------------
with open("mydata.bin", "wb") as f:
    f.write(packed)
#--------------------------------------------------------------------------------------------------------------------------------------
with open("mydata.bin", "rb") as f:
    rawBytes = f.read()
#print(rawBytes)
#--------------------------------------------------------------------------------------------------------------------------------------
unpacked = struct.unpack(formatString, rawBytes)
rawString = unpacked[1]
cleanString = rawString.decode("utf-8").strip("\x00")
print(cleanString)
"""

