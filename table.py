import struct
import os

class Table:

    def __init__(self, filename, formatString):
        self.filename = filename
        self.formatString = formatString
        self.recordSize = struct.calcsize(self.formatString)
        
        if os.path.exists(self.filename):
            fileSize = os.path.getsize(self.filename)
            self.rowCount = fileSize // self.recordSize
        else:
            self.rowCount = 0
    
    def insert(self, entry):
        with open(self.filename, "ab") as f:
            packed = struct.pack(self.formatString, False, entry[0], entry[1])
            f.write(packed)
        self.rowCount += 1

    def select(self, rowNr):
        with open(self.filename, "rb") as f:
            if rowNr >= self.rowCount:
                raise ValueError("Row does not exist!")
            f.seek(self.recordSize * rowNr)
            rawBytes = f.read(self.recordSize)
            unpacked = struct.unpack(self.formatString, rawBytes)
            is_deleted = unpacked[0]
            if is_deleted == True:
                raise ValueError("Row has been deleted!")
            rawData = unpacked[2]
            cleanData = rawData.decode('utf-8').strip('\x00')
            print("Data from file, read: " + cleanData)

    def delete(self, rowNr):
        with open(self.filename, "r+b") as f:
            if rowNr >= self.rowCount:
                raise ValueError("Row does not exist!")
            f.seek(self.recordSize * rowNr)
            f.write(struct.pack("?", True))