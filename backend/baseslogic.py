import random

class BaseRando():

    def __init__(self, fileObj: bytearray):
        self.fileEditObj = fileObj          # Give the method access to the ROM data



    def basesShuffle(self, fileIndex, splitTatyana):
        statBuffer = []     # Hold the stats that will get shuffled
        charCount = 32      # Default amount of characters to randomize
        x = 0               # The loop counter

        if splitTatyana:
            charCount = 41      # Tatyana you devil chilf

        while x < charCount:    # Used to be a static 32, now a variable to account for Tatyana
        
            statBuffer.clear()      # Make sure we have a fresh list each time
        
            for y in range(7):      # Grab the stats
                statBuffer.append(self.fileEditObj[fileIndex+y])

            random.shuffle(statBuffer)      # Shuffle the stats

            for z in range(7):      # Put the stats back in
                self.fileEditObj[fileIndex+z] = statBuffer[z]

                if x == 18 and not splitTatyana:
                    tatyanaIndex = fileIndex + 720      # Demon child
                    for i in range(8):
                        self.fileEditObj[tatyanaIndex + z] = statBuffer[z]
                        tatyanaIndex += 48

            fileIndex += 48     # Advance to the next character
            x += 1              # Don't loop infintely

        return self.fileEditObj


    # Personal Bases Randomization; Uses indexes 1~6 of the options list
    def handlePersonalBasesRando(self, basesOpt, romVer):

        fileIndex = 4064774     #* Hardcoding with int literals because I can't be bothered to use bytes atm
                            # This is the index for Julian's personal stat's stored at 0x3E0602, 48 bytes long per character
                            # Uhh, I don't think I can change to refer to the ROMs pointers? It's weird, look at 0x5E92E, it reads the stats

        if romVer == 1: 
            fileIndex += 512    # Move the index 0x200 bytes forward because of the header if Mana Sword EN

            # Get the random personal bases
        if basesOpt[1] == 0:
            print("No changes necessary, skipping...")
            return self.fileEditObj

        if basesOpt[1] == 1:
            print("Shuffling bases...")
            return self.basesShuffle(fileIndex, basesOpt[0])      # Call to other method to shuffle bases instead
        
        k = 0               # Why did I choose k when I made this?
        totalcheck = 0
        charCount = 32

        splitTatyana = basesOpt[0]      # Getting the options into a variable. I could just refer to the list, but eh.
        randMin = basesOpt[2]
        randMax = basesOpt[3]

        statMax = basesOpt[4] + basesOpt[5] + 1
        statMin = basesOpt[4] - basesOpt[5] + 1


        if splitTatyana == True:
            charCount = 41

        print("The bases options are:")     # I will leave this here for debugging if necessary
        for thing in basesOpt:
            print(thing)



        try:
            while k  < charCount:       # Used to be a static 32, now a variable to account for Tatyana

                totalcheck = 0              # Reset BST value
                
                #print("Buffer cleared")
                for j in range(7):      # Really? j?
                
                    newStat = random.randint(randMin, randMax)    # Seems a bit odd to do this, but you'll see why
                    
                    totalcheck += newStat                           # Get a BST to compare

                    self.fileEditObj[fileIndex + j] = newStat       # Write the new stat


                    if k == 18 and splitTatyana == False:                                 # It's because of Tatyana
                        tatyanaIndex = fileIndex + 720                        #* I did not have this tatyanaIndex variable here before
                        for x in range (8):                                   #* This child has forced my hand
                            self.fileEditObj[tatyanaIndex + j] = newStat      #* I also don't know why this works but I will take it
                            tatyanaIndex += 48
                        
                print("Char",k,"randomized\nChecking stat total...")

                if totalcheck < statMin or totalcheck > statMax:    # If the BST does not fall within the range, reroll
                    k -= 1
                    fileIndex -= 48
                    print("Check failed, rerolling...")

                k += 1      # Do not loop infinitely
                fileIndex += 48     # Move to the next character
            # Again, hardcoding because I'm lazy atm #!TODO Convert from ints to use bytes from the file
                        #* Disregard the TODO for now, address 0x5E92E has the code that reads the stats, not sure what to do from there

            return self.fileEditObj

        except Exception as e: 
            print("Error in Bases Randomization: ",e)
            raise



    def main(self, optlist: list, romVer):
        #random.seed(seed)
        return self.handlePersonalBasesRando(optlist, romVer)
