from specialRolls import iRoll, sRoll
from encounterDictionaries import dayEncounters, nightEncounters

class timePeriod:
    def  __init__(self, vistGuide = False, isNight = False, areTravel = True, onRoad = True, recentEnc = 0, travelPace = "normal"):
        self.vistGuide = vistGuide # Are the players being guided by Vistani?
        self.isNight = isNight # Is it night time? 
        self.areTravel = areTravel # Are the players travelling, or camping?
        self.onRoad = onRoad # Are the players on/near the road, or in the wilderness?
        self.recentEnc = recentEnc # How many encounters have the players had in the last 12 hours?
        self.startEnc = recentEnc # How many encounters the players had before this time interval
        travelPace = travelPace # How quickly are the players travelling? 

    def noEncounter(self):
        print("The time passes uneventfully.")

    def encounterRoll(self): # Rolls to determine which encounter occurs
        if self.vistGuide == True: # Players traveling with Vistani guides
            encRoll = sRoll('1d12')
        else: # Players traveling alone
            encRoll = int(iRoll('1d12') + iRoll('1d8'))
        if self.areTravel == False: # Players are resting/camping
            if self.isNight == False: # Stationary during the day
                if encRoll != 4 or 5 or 6 or 9 or 10 or 15: # Not a travelling encounter
                    encRoll = str(encRoll)
                    self.recentEnc += 1 # Increases recent encounters
                    encounter = dayEncounters.get(encRoll) # Daytime Encounter
                    print("The players encounter " + encounter + ".") # Says what the players face
            else: # Stationary during the night
                if encRoll != 3 or 4 or 5 or 6 or 7: # Not a travelling encounter
                    encRoll = str(encRoll)
                    self.recentEnc += 1 # Increases recent encounters
                    encounter = nightEncounters.get(encRoll) # Nighttime Encounter
                    print("The players encounter " + encounter + ".") # Says what the players face
        else: # Players are travelling;  don't need to worry about specific encounters
            if self.isNight == False: # Travelling during day
                encRoll = str(encRoll)
                self.recentEnc += 1            
                encounter = dayEncounters.get(encRoll) # Daytime Encounter
                print("The players encounter " + encounter + ".") # Says what the players face
            else: # Travelling at night
                encRoll = str(encRoll)
                self.recentEnc += 1            
                encounter = nightEncounters.get(encRoll) # Nighttime Encounter
                print("The players encounter " + encounter + ".") # Says what the players face

    def encounterCheck(self): # Checks to see if players have a random encounter
        if self.recentEnc < 2: # Checks to see if players have already had many recent random encounters
            procRoll = iRoll('1d20')
            if self.onRoad == True: # Players are travelling on, or resting by, the road
                if procRoll >= 18: 
                    self.encounterRoll()
            else: # Players are travelling or resting in the wilderness
                if procRoll >= 15:                              
                    self.encounterRoll()

    def timeCheck(self): # Gauges how long the players are in the forest
        if self.isNight == False:
            time = "day"
        else:
            time = "night"
        if self.areTravel == True:
            self.forestTime = int(input("Distance travelled during the " + time + " (in miles): "))
            travelPace = input("How fast are the players travelling (s/n/f): ")
            if travelPace == "fast" or "Fast" or "f" or "F":
                travelPace = 2
                travelCap = int(30)
                travelRate = int(4)
                travelDay = float(7.5)
            elif travelPace == "normal" or "Normal" or "n" or "N":
                travelPace = 1
                travelCap = int(24)
                travelRate = int(3)
                travelDay = int(8)
            elif travelPace == "slow" or "Slow" or "s" or "S":
                travelPace = 0
                travelCap = int(18)
                travelRate = int(2)
                travelDay = int(9)
            if self.forestTime > travelCap:
                marchHours = int(float(self.forestTime - travelCap) / travelRate)
                print("The players won't be able to travel that far in a normal day.")
                print("They'd need to travel " + str(marchHours) + " hours beyond the normal " + str(travelDay) + " to travel that far.")
                marchCheck = input("Do the players choose to continue travelling, even though they might suffer exhaustion? (y/n)")
                if marchCheck == "True" or "true" or "y" or "Y" or "yes" or "Yes" or True:
                    exhaustDC = int(11)
                    for change in range(int(marchHours)):
                        print("The players make a DC + " + str(exhaustDC) + " CON save.")
                        exhaustDC += 1
                    self.forestTime = self.forestTime / int(travelDay + marchHours)
                else:
                    self.forestTime = int(travelDay)
            else: 
                self.forestTime = self.forestTime / travelRate
                        
        else:
            self.forestTime = int(input("Time spent resting during the " + time + " (in hours): ")) * 2
        for change in range(int(self.forestTime)):
            self.encounterCheck()
        if self.recentEnc == self.startEnc:
            self.noEncounter()

