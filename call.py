import main

dayRest = timePeriod(areTravel = False, isNight = False)
dayTravel = timePeriod(areTravel = True, isNight = False)
nightRest = timePeriod(areTravel = False, isNight = True)
nightTravel = timePeriod(areTravel = True, isNight = True)

dayTravel.timeCheck()
