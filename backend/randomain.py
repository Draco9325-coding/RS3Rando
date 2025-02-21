import random
from backend.baseslogic import BaseRando
from backend.growthslogic import GrowthsRando
from backend.proficiencylogic import ProfRando
from backend.modifierlogic import ModRando

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
            self.starArr = ['Hunter/Artemis', 'Scholar/Athena', 'Royal/Zeus', 'Fighter/Ares', 'Merchant/Hermes']
            self.wepArr = ['Sword', 'Big Sword', 'Axe', 'Mace', 'Epee', 'Spear', 'Bow', 'Kung Fu', 'None']

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

        pBuf = []
        pgBuf = []
        pmBuf = []
        proficiencyIndex = 4064781

        stmBuf = []
        wmBuf = []
        starmodIndex = 4101705
        wepmodIndex = 4101753

        spBuf = []
        starBuf = []
        wepBuf = []
        sparkIndex = 4064790

        if writeList[1] == True:
            charCount = 41
        
        if self.romVer == 1:
            basesIndex += 512
            growthsIndex += 512
            proficiencyIndex += 512
            sparkIndex += 512
            starmodIndex += 512
            wepmodIndex += 512
        
        
        headStr1 = "Seed: " + str(writeList[0]) + "\n"
        if writeList[2] == 0:
            headStr2 = "No Personal Stat Randomization\n"
        elif writeList[2] == 1:
            headStr2 = "Personal Stats: Shuffle\n"
        else:
            headStr2 = "Personal Stats: Randomized\n"

        if writeList[3] == 0:
            headStr3 = "No Growth Randomization\n"
        else:
            headStr3 = "Weapon Level Growths: Randomized\n"

        if writeList[4] == 0:
            headStr4 = "No Weapon Level Randomization\n\n"
        elif writeList[4] == 1:
            headStr4 = "Weapon Level Bases: Shuffled\n\n"
        else:
            headStr4 = "Weapon Level Bases: Randomized\n\n"

        if writeList[5] == True:
            headStr5 = "Spark Types: Randomized\n"
        else:
            headStr5 = "Spark Types: Unchanged\n"

        if writeList[6] == True:
            headStr6 = "Star Signs: Randomized\n"
        else:
            headStr6 = "Star Signs: Unchanged\n"

        if writeList[7] == True:
            headStr7 = "Favorite Weapons: Randomized\n"
        else:
            headStr7 = "Favorite Weapons: Unchanged\n"

        if writeList[8] == True:
            headStr8 = "Stat Modifiers: Randomized\n\n\n"
        else:
            headStr8 = "Stat Modifiers: Unchanged\n\n\n"


        f.write("RS3 Randomized Changelog\n\n")
        f.write(headStr1)
        f.write(headStr2)
        f.write(headStr3)
        f.write(headStr4)
        f.write(headStr5)
        f.write(headStr6)
        f.write(headStr7)
        f.write(headStr8)

        f.write("SL = Slash (Swords)\tHI = Hit (Axe/Mace)\tPI = Pierce (Epee/Lance)\tSH = Shot (Bow)\tKG = Kung Fu\tSup = Support\n\
WI = Wind\tFI = Fire\tEA = Earth\tWA = Water\tSU = Sun\tMO = Moon\n\n\n")
        
        if writeList[8]:
            f.write("\tNew Star Sign Modifers:\n")
            for y in range (5):
                stmBuf.clear()  # Clear the buffer of star sign modifiers

                f.write(str(self.starArr[y])+':\n')
                f.write("   Str   Dex   Agi   Con   Int   Wil   Cha   HP\n")
                for z in range(8):

                    buf = self.fileEditObj[starmodIndex + z]
                    # print(buf)
                    if buf >= 128:
                        buf -= 128
                        buf *= -1

                    stmBuf.append(buf)

                starmodIndex += 8

                stmStr = f"{stmBuf[0]:>6d}{stmBuf[1]:>6d}{stmBuf[2]:>6d}{stmBuf[3]:>6d}\
{stmBuf[4]:>6d}{stmBuf[5]:>6d}{stmBuf[6]:>6d}{stmBuf[7]:>6d}\n\n"
                f.write(stmStr)

            f.write("\n\tNew Favorite Weapon Modifiers:\n")

            for y in range (9):
                wmBuf.clear()

                f.write(str(self.wepArr[y])+':\n')
                f.write("   Str   Dex   Agi   Con   Int   Wil   Cha   HP\n")
                for z in range(8):

                    buf = self.fileEditObj[wepmodIndex + z]
                    # print(buf)
                    if buf >= 128:
                        buf -= 128
                        buf *= -1
                    wmBuf.append(buf)
                wepmodIndex += 8
                

                wmStr = f"{wmBuf[0]:>6d}{wmBuf[1]:>6d}{wmBuf[2]:>6d}{wmBuf[3]:>6d}\
{wmBuf[4]:>6d}{wmBuf[5]:>6d}{wmBuf[6]:>6d}{wmBuf[7]:>6d}\n\n"
                f.write(wmStr)

        f.write("\nStats listed here are BEFORE Star Sign/Weapon Specialty stat modifiers.\n\
\t\tTHEY WILL DIFFER SLIGHTLY IN GAME\n\n\n")
        while x < charCount:

            bBuf.clear()
            gBuf.clear()
            pgBuf.clear()
            pBuf.clear()
            pmBuf.clear()

            if x == 27 or x == 32:
                x += 1
                continue

            indexStr = "Character Index " + str(x) + ": " + self.charArr[x] + "\n\n"

            f.write(indexStr)

                # Read personal stats (Except HP)
            for i in range(7):
                bBuf.append(self.fileEditObj[basesIndex + i])

                # Read growths
            for j in range(16):
                if j == 11:
                    continue
                gBuf.append(self.fileEditObj[growthsIndex + j])

                # Read proficiency values and calculate what they mean
            for k in range(8):
                pbufRead = self.fileEditObj[proficiencyIndex + k]
                if pbufRead >=128:
                    pgBuf.append("Yes")
                    pbufRead -=128          # We already have if it grows out of party, okay to remove
                else:
                    pgBuf.append("No")

                if k == 5:              # For the earthly magicks

                    magCheck = int(pbufRead / 32)    # Determine which magic type
                    if magCheck == 3:
                        pmBuf.append("WA")      # 0x60 is Water
                        pbufRead -= 96
                    elif magCheck == 2:
                        pmBuf.append("EA")      # 0x40 is Earth
                        pbufRead -= 64
                    elif magCheck == 1:
                        pmBuf.append("FI")      # 0x20 is Fire
                        pbufRead -= 32
                    else:
                        pmBuf.append("WI")      # 0x00 is Wind

                elif k == 6:              # For the two celestial magics
                                # Only two magic types for this, so this should be fine
                    if pbufRead >= 32:
                        pmBuf.append("MO")      # 0x20 is Moon
                        pbufRead -= 32
                    else:
                        pmBuf.append("SU")      # 0x00 is Sun

                pBuf.append(pbufRead)
            
            
            bStr =  f"       {bBuf[0]:<5d}{bBuf[1]:<5d}{bBuf[2]:<5d}{bBuf[3]:<5d}{bBuf[4]:<5d}{bBuf[5]:<5d}{bBuf[6]:<5d}\n\n"
            gStr =  f"         {gBuf[0]:<4d}{gBuf[1]:<4d}{gBuf[2]:<4d}{gBuf[3]:<4d}\
{gBuf[4]:<4d}{gBuf[5]:<4d}{gBuf[6]:<4d}{gBuf[7]:<4d}{gBuf[8]:<4d}{gBuf[9]:<4d}{gBuf[10]:<4d}\
{gBuf[11]:<5d}{gBuf[12]:<4d}{gBuf[13]:<4d}{gBuf[14]:<4d}\n\n"
            pStr =  f"               {pBuf[0]:<5d}{pBuf[1]:<5d}{pBuf[2]:<5d}{pBuf[3]:<5d}{pBuf[4]:<5d}{pBuf[5]:<5d}{pBuf[6]:<5d}{pBuf[7]:<5d}\n"
            pgStr = f"   OoP Growth: {pgBuf[0]:<5s}{pgBuf[1]:<5s}{pgBuf[2]:<5s}{pgBuf[3]:<5s}{pgBuf[4]:<5s}{pgBuf[5]:<5s}{pgBuf[6]:<5s}{pgBuf[7]:<5s}\n\n"


            f.write("Bases: STR  DEX  AGI  CON  INT  WIL  CHA\n")
            f.write(bStr)

            f.write("Growths: SL  HI  PI  SH  KG  WI  FI  EA  WA  SU  MO  Sup  TP  MP  HP\n")
            f.write(gStr)

            f.write(f"Proficiencies: SL   HI   PI   SH   KG   {pmBuf[0]:<5s}{pmBuf[1]:<5s}Sup\n")
            f.write(pStr)
            f.write(pgStr)

            basesIndex += 48
            growthsIndex += 16
            proficiencyIndex += 48

            f.write("\n\n\n")

            x += 1

        f.close()


    # ****************************** Main method that calls the others ****************************** #

    def main(self, randoOpt: list):
        random.seed(randoOpt[0])
        # Split the options given into separate lists
        basesRando = []
        growthsRando = []
        profsRando = []
        modsRando = []
        
        for i in randoOpt[1:7]:
            basesRando.append(i)

        growthsRando.append(randoOpt[1])    # Append whether or not to split Tatyana
        for j in randoOpt[7:10]:
            growthsRando.append(j)
        
        profsRando.append(randoOpt[1])      # See above
        for k in randoOpt[10:17]:
            profsRando.append(k)

        modsRando.append(randoOpt[1])      # Numero tres
        for l in randoOpt[17:23]:
            modsRando.append(l)
        
            # Call methods that handle the individual options
        bases = BaseRando(self.fileEditObj)
        growths = GrowthsRando(self.fileEditObj)
        proficiencies = ProfRando(self.fileEditObj)
        modifiers = ModRando(self.fileEditObj)

        # romVer = 0 for JP, romVer = 1 for EN, romVer = 2 for ES
        print("\t\t~~~~ \t  Base Randomization...    ~~~~")
        self.fileEditObj = bases.main(basesRando, self.romVer)
        print("\t\t~~~~ \tGrowth Randomization...    ~~~~")
        self.fileEditObj = growths.main(growthsRando, self.romVer)
        print("\t\t~~~~ Weapon Level Randomization... ~~~~")
        self.fileEditObj = proficiencies.main(profsRando, self.romVer)
        print("\t\t~~~~ Stat Modifier Randomization...~~~~")
        self.fileEditObj = modifiers.main(modsRando, self.romVer)