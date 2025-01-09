class OpenFile():
    
    def __init__(self, RS3File: str):


        #!TODO Add support for Mana Sword EN TL
            # Magno's ES translation is somehow compatible?

            # Defining a set of 16 bytes that can be found a 0x1B20. Should match each of the roms
        romJPCheck = [b'\x1B',b'\x6B',b'\xA5',b'\x76',b'\xF0',b'\x22',b'\xA5',b'\x77',
                      b'\x0A',b'\x0A',b'\x18',b'\x65',b'\x77',b'\xC2',b'\x20',b'\x29']
        
        romENCheck = [b'\xC2',b'\x20',b'\xC6',b'\x93',b'\xC6',b'\x8D',b'\xC6',b'\x8D',
                      b'\xE2',b'\x20',b'\xBD',b'\xAC',b'\xD5',b'\x0A',b'\x85',b'\x90']

        romESCheck = [b'\x1B',b'\x6B',b'\xA5',b'\x76',b'\xF0',b'\x2E',b'\xA5',b'\x77',
                      b'\x0A',b'\x0A',b'\x18',b'\x65',b'\x77',b'\x18',b'\x65',b'\x77']

        tempList = []

        self.romVersion = -1

        try:
            self.RS3File : str = RS3File
            self.RS3Open = open(RS3File, 'rb')
            print("RS3 Opened")
            
            self.RS3Open.seek(6944)
            for i in range(16):            
                tempList.append(self.RS3Open.read(1))

            if tempList == romJPCheck:
                self.romVersion = 0
            elif tempList == romENCheck:
                self.romVersion = 1
            elif tempList == romESCheck:
                self.romVersion = 2
            else:
                raise ValueError("Incompatible ROM Selected")

            self.RS3Open.seek(0)
            self.RS3Read = self.RS3Open.read()
            self.RS3Open.close()
    
        except OSError as e:
            print("Problem with opening the file", e)
            raise
        except ValueError as e:
            raise

    def getData(self):
        print("From backend: Returned bytestream object")
        returnArr = [self.RS3Read, self.romVersion]
        return returnArr