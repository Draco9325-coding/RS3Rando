import random
import traceback
    # Oh man this one is MESSY
    # The amount of mental visualization on how to do this was insane. Send help. I'm losing my mind.

    #!TODO Implement way to prevent shuffling from heavily biasing wind magic, preferably reading inherent magic byte

class ProfRando():

    def __init__(self, fileObj: bytearray):
        self.fileEditObj = fileObj

    def handleSpellLists(self, splitTatyana, romVer):
            # Default routine to run if randomizing weapon levels in any form
            # Mostly done to prevent weird game breaking shenanigans I.e. Sharl having Fire and Wind magic
            #
            # This won't give magic spells to those who normally do not have any, but it will
            # remove the spell list if the character does not roll a magic level

        spellIndex = 4064795    # Index of Julian's spell list
        magIndex = 4064786      # Index of magic level (Earthly, +1 for Celestial)

        SPELL_ID = 170           # The first magic ID

        if romVer == 1:
            spellIndex += 512   # Move indices depending on ROM version
            magIndex += 512

        spellBuffer = []        # Initialize buffer to hold the spell IDs

        count = 0           # Set up the loop
        charCount = 32
        if splitTatyana:
            charCount = 41
        
        while count < charCount:
            spellBuffer.clear()     
            hasEarthly = False      # See which major type of magic is had
            hasCelestial = False
            spellNum = 0

            for x in range(4):
                spellBuffer.append(self.fileEditObj[spellIndex + x])
                if spellBuffer[x] != 255:
                    spellNum += 1       # Count each spell, empty slots are nulled to 255
            
            if spellNum == 0:
                count += 1      # Don't add spells if the character has no spells
                magIndex += 48
                spellIndex += 48
                continue

            if(self.fileEditObj[magIndex] % 32) > 0:
                hasEarthly = True           # If has Wind/Fire/Earth/Water
            if(self.fileEditObj[magIndex+1]%32) > 0:
                hasCelestial = True         # If has Sun/Moon

            #!TODO check for which type of magic, which school, and then change the spells
                # Time for very verbose nested 'if' conditionals with long functions within them
            magType1 = self.fileEditObj[magIndex]
            magType2 = self.fileEditObj[magIndex+1]

            if magType1 >= 128:
                magType1 -= 128

            if magType2 >= 128:
                magType2 -= 128
            
            magType1 = int(magType1 / 32) # Get the current magic the character has
            magType2 = int(magType2/32)
            
            magType2 += 4       # Sun
            
                # Now that I have all the necessary information, we first check which of the two types of magic (Earthly
                # or Celestial) are present, if at all.
            if not hasEarthly and not hasCelestial:
                for i in range(spellNum):
                    spellBuffer[i] = 255    # Remove spells if the character has no magic level

                    #*The idea is to take the spell's ID, subtract 170 (0xAA), modulo by 7, add (7 * magic type), then add back 0xAA
                # If both Earthly and Celestial
            elif hasEarthly and hasCelestial:
                splitcount = int(spellNum/2)        # Split the list half and half
                for i in range(spellNum):
                    idBuf = spellBuffer[i]
                    idBuf = idBuf - SPELL_ID
                    idBuf = idBuf % 7       # Doing this one at a time because i do not trust it to compute it properly otherwise
                    if i < splitcount:
                        idBuf = (7 * magType1) + idBuf + SPELL_ID   # As I then don't follow my own words. should give one of 4 earthly magicks
                    else:
                        idBuf = (7 * magType2) + idBuf + SPELL_ID   # Oh this, i dont trust this. but its math, computers are good at math, right?
                                                                # But this gives either sun or moon magic
                    spellBuffer[i] = idBuf
            
            elif hasEarthly:
                for i in range(spellNum):
                    idBuf = spellBuffer[i]
                    idBuf = idBuf - SPELL_ID
                    idBuf = idBuf % 7
                    idBuf = (7 * magType1) + idBuf + SPELL_ID
                    spellBuffer[i] = idBuf

            elif hasCelestial:
                for i in range(spellNum):
                    idBuf = spellBuffer[i]
                    idBuf = idBuf - SPELL_ID
                    idBuf = idBuf % 7
                    idBuf = (7 * magType2) + idBuf + SPELL_ID
                    spellBuffer[i] = idBuf

                # There's probably a better way to do this, oh well, time to see if this works

            for y in range(4):
                self.fileEditObj[spellIndex + y] = spellBuffer[y]

                #* Tatyana does not start with magic, for now that won't be handled

            count += 1
            magIndex += 48
            spellIndex += 48    # Don't loop infinitely and move to the next character


    def profShuffle(self, fileIndex, splitTatyana, romVer):
        buffer = []
        charcount = 32
        count = 0

        if splitTatyana:
            charcount = 41

        while count < charcount:
            buffer.clear()      # Clear the buffer of held proficiencies

            for x in range(8):
                buffer.append(self.fileEditObj[fileIndex + x])  # Grab proficiencies

            random.shuffle(buffer)      # Get jiggy with it

            for y in range(8):
                doesGrow = buffer[y] >=128      # Remember if it should have out of party scaling
                
                if doesGrow:
                    buffer[y] = buffer[y] - 128     # Remove scaling flag

                if (y != 5 and y !=6) and (buffer[y] >= 32):    # Execute if the current index is not magic and is too high
                    buffer[y] = buffer[y] % 32  # If it's not magic, bring the level back down
                
                    #!TODO Read inherent magic byte to use for out of party magic scaling

                if doesGrow:                    # Place back the scaling flag
                    buffer[y] = buffer[y] + 128

                self.fileEditObj[fileIndex + y] = buffer[y]

                if count == 18 and not splitTatyana:
                    tatyanaIndex = fileIndex + 720      # Tatyana Time (the thrilling trilogy finale)
                    for i in range(8):
                        self.fileEditObj[tatyanaIndex + y] = buffer[y]
                        tatyanaIndex += 48

                # Remove magic lock
            exIndex = fileIndex + 32
            self.fileEditObj[exIndex] = 0

            fileIndex += 48
            count += 1

        self.handleSpellLists(splitTatyana, romVer)     # Change spell lists to match weapon levels

    def handleProfRando(self, profOpt, romVer):
        # Options in order of
        # Tatyana/Choice/Max/Grow?/Chance/Mag/Chance
            # Set where the proficiency bases are, and check if we need to adjust
        
        fileIndex = 4064781
        
        if romVer == 1:
            fileIndex += 512

        if profOpt[1] == 0:
            print("No changes necessary, skipping...")
            return self.fileEditObj
        elif profOpt[1] == 1:
            print("Shuffling weapon levels...")
            self.profShuffle(fileIndex, profOpt[0], romVer)
            return self.fileEditObj
        
        for item in profOpt:
            print(item)

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
                    if count != 8:      # Exclude Leonid, he starts with 666 base HP
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
                if count == 18 and not profOpt[0]:
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

                    roll = random.randrange(0, 100)     # Roll if magic gets a base
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
                    
                    self.fileEditObj[fileIndex + i] = newProf   # Finally, assign the value

                        # Tatyana time (the trilogy pt 2)
                    if count == 18 and not profOpt[0]:
                        tatyanaIndex = fileIndex + 720
                        for y in range(8):
                            self.fileEditObj[tatyanaIndex + i] = newProf
                            tatyanaIndex += 48

                    i += 1

                # Remove the magic lock from characters; Possibly here temporarily while I consider a magic lock ranomizer
            exIndex = fileIndex + 32
            self.fileEditObj[exIndex] = 0

            print("Character",count,"weapon levels randomized")
            count += 1      # Don't loop infinitely
            fileIndex += 48     # Advance to the next character

        self.handleSpellLists(profOpt[0], romVer)   # Change spell lists depending on weapon levels
        return self.fileEditObj     # Return the file object


    def main(self, optlist: list, romVer):
        #random.seed(seed)
        try:
            return self.handleProfRando(optlist, romVer)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            raise