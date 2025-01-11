import random

class GrowthsRando():

    def __init__(self, fileObj: bytearray):
        self.fileEditObj = fileObj


    # Proficiency Growths Randomization; Uses indexes 7~9 of the options list
    def handleGrowthsRando(self, growthsOpt, romVer):
        fileIndex = 4075967         # File index (in base-10) for Julian's growths, at 0x3E31BF, 16 bytes long per character

        if romVer == 1:
            fileIndex += 512        # Push forward if in the header'd EN ROM

        if growthsOpt[1] == 0:
            return self.fileEditObj
        
        splitTatyana = growthsOpt[0]
        growthChance = growthsOpt[2]
        growthMax = growthsOpt[3] + 1
        newGrowth = 0
        i = 0

        charCount = 32


        if splitTatyana == True:
            charCount = 41

        
        
        try:
            for l in growthsOpt: print(l)

            while i < charCount:
                
                for j in range(16):
                    
                    if j == 11: continue

                    roll = random.randrange(0, 100)

                    if roll > growthChance:
                        self.fileEditObj[fileIndex + j] = 0
                    else:
                        if growthMax == 1:
                            newGrowth = 1
                        else:
                            newGrowth = random.randrange(1, growthMax)

                        self.fileEditObj[fileIndex + j] = newGrowth

                        if i == 18 and not splitTatyana:             # Gotta compensate for Tatyana

                            tatyanaIndex = fileIndex + 240      #* you will not best me today, child
                            
                            for k in range(8):

                                self.fileEditObj[tatyanaIndex + j] = newGrowth
                                tatyanaIndex += 16
                            #fileIndex -= 368

                print("Char",i,"growths done")
                fileIndex += 16
                i += 1

            return self.fileEditObj

        except Exception as e: 
            print("Error in growths randomization: ", e)
            raise
        # Jump 240, -352



    def main(self, optlist: list, seed, romVer):
        random.seed(seed)
        return self.handleGrowthsRando(optlist, romVer)