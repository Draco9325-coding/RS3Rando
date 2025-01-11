import random
from backend.baseslogic import BaseRando
from backend.growthslogic import GrowthsRando

class Randomization():
    
    # ****************************** Initialization method ****************************** #
    def __init__(self, fileBytesObj : bytes, romVer):

        try:
                # Convert from <bytes> to <bytearray>, allowing it to be changed
            self.fileEditObj = bytearray(b'')
            self.romVer = romVer    # Used to change where data is from, depends on ROM version
                
                #!TODO Make this array read from an external file to support custom characters.
                    # How that will be implemented, not too sure

            self.charArr = ['Julian', 'Ellen', 'Sara', 'Thomas', 'Khalid', 'Mikhail', 'Monica', 'Katarina', 'Leonid', 'Shonen', 
                            'Tiberius', 'Wood', 'Paul', 'Robin', 'Fat Robin', 'Muse', 'Sharl', 'Poet', 'Tatyana', 'Yan Fan', 'Undine',
                            'Zhi Lin', 'Herman', 'Fullbright', 'Bai Meiniang', 'Nora', 'Black', 'Catherine', 'Fairy', 'Boston', 'Zho',
                            'Flurry', 'Therese', 'Shebert', 'Millefeuille', 'Candy', 'Crepe', 'Souffle', 'Bavarios', 'Eclair', 'Tart']


            for i in fileBytesObj:
                self.fileEditObj.append(i)
                # Using the self. thing, it should be available to every method in this class.
        except:
            print("Something went wrong")
    

    # ****************************** Write to file ****************************** #

    def writeToSFC(self, fileName):
        try:
            newFileName = fileName[:-4] + ".sfc"    # Not sure if it's fully needed, but ensuring the 
            newFileObj = bytes(self.fileEditObj)    # file has the correct extension shouldn't hurt
            with open(newFileName, "wb") as writeFile:
                writeFile.write(newFileObj)
        except Exception as e:
            print("Error:", e)
            raise
    

    def writeChangelog(self, writeList, path):

        changelogPath = path[:-4] + "_CHANGELOG.txt"
        x = 0
        charCount = 32
        f = open(changelogPath, 'w')

        bBuf = []
        basesIndex = 4064774

        gBuf = []
        growthsIndex = 4075967

        if writeList[1] == True:
            charCount = 41
        
        if self.romVer == 1:
            basesIndex += 512
            growthsIndex += 512
        
        
        headStr1 = "Seed: " + str(writeList[0]) + "\n"
        if writeList[2] == 0:
            headStr2 = "No Personal Stat Randomization\n"
        elif writeList[2] == 1:
            headStr2 = "Personal Stats: Shuffle\n"
        else:
            headStr2 = "Personal Stats: Randomized\n"

        if writeList[3] == 0:
            headStr3 = "No Growth Randomization\n\n\n"
        else:
            headStr3 = "Proficiency Growths: Randomized\n\n\n"

        f.write("RS3 Randomized Changelog\n\n")
        f.write(headStr1)
        f.write(headStr2)
        f.write(headStr3)

        f.write("SL = Slash (Swords)\tHI = Hit (Axe/Mace)\tPI = Pierce (Epee/Lance)\tSH = Shot (Bow)\tKG = Kung Fu\tSup = Support\n\
WI = Wind\tFI = Fire\tEA = Earth\tWA = Water\tSU = Sun\tMO = Moon\n\n")
        f.write("Stats listed here are BEFORE Star Sign/Weapon Specialty stat modifiers.\n\
\t\tTHEY WILL DIFFER SLIGHTLY IN GAME\n\n\n")
        while x < charCount:

            bBuf.clear()
            gBuf.clear()

            if x == 27 or x == 32:
                x += 1
                continue

            indexStr = "Character Index " + str(x) + ": " + self.charArr[x] + "\n\n"

            f.write(indexStr)

            for i in range(7):
                bBuf.append(self.fileEditObj[basesIndex + i])

            for j in range(16):
                if j == 11:
                    continue
                gBuf.append(self.fileEditObj[growthsIndex + j])
            
            bStr =  f"       {bBuf[0]:<5d}{bBuf[1]:<5d}{bBuf[2]:<5d}{bBuf[3]:<5d}{bBuf[4]:<5d}{bBuf[5]:<5d}{bBuf[6]:<5d}\n"
            gStr =  f"         {gBuf[0]:<4d}{gBuf[1]:<4d}{gBuf[2]:<4d}{gBuf[3]:<4d}\
{gBuf[4]:<4d}{gBuf[5]:<4d}{gBuf[6]:<4d}{gBuf[7]:<4d}{gBuf[8]:<4d}{gBuf[9]:<4d}{gBuf[10]:<4d}\
{gBuf[11]:<5d}{gBuf[12]:<4d}{gBuf[13]:<4d}{gBuf[14]:<4d}\n"
 
            
            f.write("Bases: STR  DEX  AGI  CON  INT  WIL  CHA\n")
            f.write(bStr)

            f.write("Growths: SL  HI  PI  SH  KG  WI  FI  EA  WA  SU  MO  Sup  TP  MP  HP\n")
            f.write(gStr)

            basesIndex += 48
            growthsIndex += 16

            f.write("\n\n\n")

            x += 1

        f.close()


    # ****************************** Main method that calls the others ****************************** #

    def main(self, randoOpt: list):
        random.seed(randoOpt[0])
        # Split the options given into separate lists
        basesRando = []
        growthsRando = []
        
        for i in randoOpt[1:7]:
            basesRando.append(i)

        growthsRando.append(randoOpt[1])
        for j in randoOpt[7:10]:
            growthsRando.append(j)
        
        
            # Call methods that handle the individual options
        bases = BaseRando(self.fileEditObj)
        growths = GrowthsRando(self.fileEditObj)

        # romVer = 0 for JP, romVer = 1 for EN, romVer = 2 for ES

        self.fileEditObj = bases.main(basesRando, randoOpt[0], self.romVer)
        self.fileEditObj = growths.main(growthsRando, randoOpt[0], self.romVer)