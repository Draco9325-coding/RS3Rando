import random

    # Oh man this one is MESSY
    # The amount of mental visualization on how to do this was insane. Send help. I'm losing my mind.

class ProfRando():

    def __init__(self, fileObj: bytearray):
        self.fileEditObj = fileObj

    def profShuffle(self, fileIndex, splitTatyana):
        return self.fileEditObj

    def handleProfRando(self, profOpt, romVer):
        # Options in order of
        # Tatyana/Choice/Max/Grow?/Chance/Mag/Chance
            # Set where the proficiency bases are, and check if we need to adjust
        fileIndex = 4064781
        
        if romVer == 1:
            fileIndex += 512

        if profOpt[1] == 0:
            return self.fileEditObj
        elif profOpt[1] == 1:
            return self.profShuffle(fileIndex, profOpt[0])
        
            # Holds if the proficiency grows out of party
        doesGrow = False

        charCount = 32  # Tatyana's aliases have tormented me
        count = 0
        i = 0
        if profOpt[0]:
            charCount = 41

        profMax = profOpt[3]
        profChance = profOpt[2]
        growChance = profOpt[5]
        magChance = profOpt[7]

        while count < charCount:
            i = 0

            while i < 8:
                    # Skip magic for now
                if i == 5:
                    i += 2
                
                valCheck = self.fileEditObj[fileIndex + i]

                    # If the value has the flag for out of party growth AND no randomizing it, remember it
                if valCheck >= 128 and not profOpt[4]:
                    doesGrow = True  # Remember what normally grew when out of party
                elif profOpt[4]:
                    doesGrow = (random.randrange(0,100) <= growChance)  # If randomizing it, make the roll
                else:
                    doesGrow = False        # Otherwise it does not grow out of party if no flag and no randomizing it
            
                roll = random.randrange(0, 100)
                if roll > profChance:       # Make the roll
                    newProf = 0     # If roll fails, set 0
                else:
                    if profMax == 1:
                        newProf = 1   # Prevent the bounding numbers for randrange from breaking
                    else:
                        newProf = random.randrange(1, profMax)  # If roll succeeds, get a new base
                    
                if doesGrow:
                    newProf += 128    # I could use bitmasks and such, but for a randomizer this should be fine
                
                self.fileEditObj[fileIndex + i] = newProf   # Finally, assign the value

                    # Tatyana time (the trilogy pt 1)
                if i == 18 and not profOpt[0]:
                    tatyanaIndex = fileIndex + 720
                    for x in range(8):
                        self.fileEditObj[tatyanaIndex + i] = newProf
                        tatyanaIndex += 48
                i += 1

            if profOpt[6]:
                    # If magic is a thing to work with, start at magic index
                i = 5

                while i < 7:
                    valCheck = self.fileEditObj[fileIndex + i]
                    if valCheck >= 128 and not profOpt[4]:
                        doesGrow = True
                    elif profOpt[4]:
                        doesGrow = (random.randrange(0,100) <= growChance)
                    else:
                        doesGrow = False

                    roll = random.randrange(0, 100)
                    if roll > magChance:
                        newProf = 0
                    else:
                        if profMax == 1:
                            newProf = 1
                        else:
                            newProf = random.randrange(1, profMax)

                    if doesGrow:
                        newProf += 128

                        # Pick a magic. If no proficiency base and no out-of-party growth, it shouldn't matter
                    if i == 5:
                        roll = random.randrange(0, 97, 32)  # 0x00 = Wind  0x20 = Fire  0x40 = Earth  0x60 = Water
                    elif i == 6:
                        roll = random.randrange(0, 33, 32)  # 0x00 = Sun   0x20 = Moon

                    newProf += roll
                    print(newProf)
                    self.fileEditObj[fileIndex + i] = newProf   # Finally, assign the value

                        # Tatyana time (the trilogy pt 2)
                    if i == 18 and not profOpt[0]:
                        tatyanaIndex = fileIndex + 720
                        for y in range(8):
                            self.fileEditObj[tatyanaIndex + i] = newProf
                            tatyanaIndex += 48

                    i += 1

            count += 1      # Don't loop infinitely
            fileIndex += 48     # Advance to the next character

        return self.fileEditObj


    def main(self, optlist: list, romVer):
        #random.seed(seed)
        return self.handleProfRando(optlist, romVer)