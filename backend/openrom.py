class OpenFile():
    
    def __init__(self, RS3File: str):

        try:
            self.RS3File : str = RS3File
            self.RS3Open = open(RS3File, 'rb')
            print("RS3 Opened")
            self.RS3Read = self.RS3Open.read()
            self.RS3Open.close()
    
        except IOError:
            print("Problem with opening the file")
        except:
            print("Something went REALLY wrong!")

    def getData(self):
        print("From backend: Returned bytestream object")
        return self.RS3Read