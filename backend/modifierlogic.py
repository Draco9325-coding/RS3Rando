import random

class ModRando():

    def __init__(self, fileObj: bytearray):
            self.fileEditObj = fileObj      # Pass on the bytearray object to be edited

    def changeStatMod(self, min, max, ver):
            # Star sign modifiers are stored at 0x3E9649
            # Favorite weapon modifiers are stored at 0x3E9679

            # Stored in order of Str-Dex-Agi-Con-Int-Wil-Cha-HP
        starmodindex = 4101705
        favmodindex = 4101753
        newmod = 0

        if ver == 1:
            starmodindex += 512
            favmodindex += 512

        for x in range(5):
            for i in range(8):
                newmod = random.randrange(min, max)
                
                if i==7:
                    newmod *= 5     # HP Increments by 5. This one can get stupidly silly really fast

                if newmod < 0:
                    newmod = abs(newmod) + 128

                self.fileEditObj[starmodindex+i] = newmod
            starmodindex += 8

        for y in range (9):
            for i in range (8):
                newmod = random.randrange(min, max)
                if i == 7:
                    newmod*=5       # See above

                if newmod < 0:
                    newmod = abs(newmod) + 128

                self.fileEditObj[favmodindex+i] = newmod

            favmodindex += 8
        print()

    def handleModRando(self, modOpt, ver):
            # Options are stored as
            #   Tatyana, Spark Type, Star Sign, Fav Weapon, RandoMod?, Min, Max

        if not modOpt[1] and not modOpt[2] and not modOpt[3] and not modOpt[4]:
            print("No changes requested, skipping...")
            return self.fileEditObj

        print("Modifier options are:")
        for item in modOpt:
            print(item)

            # Spark type is byte 0x16 from the character ID, star sign 0x28, fav weapon 0x2A
        sparkfileindex = 4064790
        if ver == 1:
            sparkfileindex += 512

        charcount = 32
        count = 0
        newval = 0

        if modOpt[0]:
            charcount = 41

        while count < charcount:
            if modOpt[1]:   # Randomize spark type
                newval = random.randrange(0,11)
                self.fileEditObj[sparkfileindex] = newval
                
                if count == 18 and modOpt[0] == False:
                    tatyanaindex = sparkfileindex +720
                    for x in range(8):
                        self.fileEditObj[tatyanaindex] = newval
                        tatyanaindex += 48

            if modOpt[2]:   # Randomize star sign
                newval = random.randrange(0,4)
                self.fileEditObj[sparkfileindex+18] = newval

                if count == 18 and modOpt[0] == False:
                    tatyanaindex = sparkfileindex +720
                    for x in range(8):
                        self.fileEditObj[tatyanaindex + 18] = newval
                        tatyanaindex += 48

            if modOpt[3]:   # Randomize fav weapon
                newval = random.randrange(0,8)
                self.fileEditObj[sparkfileindex+20] = newval

                if count == 18 and modOpt[0] == False:
                    tatyanaindex = sparkfileindex +720
                    for x in range(8):
                        self.fileEditObj[tatyanaindex+20] = newval
                        tatyanaindex += 48

            print("Character",count,"modifiers randomized")

            sparkfileindex += 48
            count += 1

        if modOpt[4]:
            self.changeStatMod(modOpt[5], modOpt[6], ver)

        return self.fileEditObj

    def main(self, optlist: list, romVer):
        return self.handleModRando(optlist, romVer)