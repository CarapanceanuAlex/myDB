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
        nameBytes = entry[1]
        if len(nameBytes) > 46:
            raise ValueError("Name too long, max 46 bytes!")
        
        if self.find_ID(entry[0]) is not None:
            raise ValueError("An entry with this ID already exists!")

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

    def select_all(self):
        if self.rowCount <= 0:# in case theres no file, else it would crash
            return None       #
        with open(self.filename, "rb") as f:      
            for row in range(self.rowCount):
                f.seek(self.recordSize * row)
                rawBytes = f.read(self.recordSize)
                unpacked = struct.unpack(self.formatString, rawBytes)
                is_deleted = unpacked[0]
                rowID = unpacked[1]
                rawData = unpacked[2]
                status = ""
                if is_deleted == True:
                    status = "Deleted"
                else:
                    status = "Active"

                cleanData = rawData.decode('utf-8').strip("\x00")
                print(str(rowID) + "-" + cleanData + "-" + status)


    """def delete(self, rowNr):
        with open(self.filename, "r+b") as f:
            if rowNr >= self.rowCount:
                raise ValueError("Row does not exist!")
            f.seek(self.recordSize * rowNr)
            f.write(struct.pack("?", True))""" # this deletes by row number, not really useful
    
    def delete_ID(self, targetID):
        if self.rowCount <= 0:
            return None
        with open(self.filename, "r+b") as f:
            for row in range(self.rowCount):
                f.seek(self.recordSize * row)
                rawBytes = f.read(self.recordSize) # read moves the cursor forward, consumes bytes and advances the cursor
                unpacked = struct.unpack(self.formatString ,rawBytes)
                is_deleted = unpacked[0]
                rowID = unpacked[1]

                if is_deleted == True:
                    continue

                if targetID == rowID:
                    f.seek(self.recordSize * row)   # move cursor back to the start of THIS row
                    f.write(struct.pack("?", True))
                    return
        raise ValueError("No row with that ID exists!3") 

    def find_ID(self, targetID):
        if self.rowCount <= 0:  #added these two lines, cuz in case theres no file, else it would crash
            return None         #
        with open(self.filename, "rb") as f:
            for rowNr in range(self.rowCount):
                f.seek(self.recordSize * rowNr)
                rawBytes = f.read(self.recordSize)
                unpacked = struct.unpack(self.formatString, rawBytes)
                is_deleted = unpacked[0]
                rowID = unpacked[1]
                rawData = unpacked[2]

                if is_deleted == True:
                    continue

                if targetID == rowID:
                    cleanData = rawData.decode('utf-8').strip('\x00')
                    return(rowID, cleanData)
        return None