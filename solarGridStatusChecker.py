import EPB0 # Epaper 2.13 landscape mode library
import random

if __name__=='__main__':
    epd = EPB0.EPD_2in13()
    epd.Clear(0xff)
    # COORDINATES ARE MAPPED TO 1ST QUADRANT!
    # origin is BOTTOM LEFT in landscape mode
    
    # some variables for checking status:
    hourlyOutput = 0 # hourly energy output of all panels (in Watts); changes each hour
    dailyOutput = 0 # sum of all hourly energy outputs thru out day (in Watts)
    totalOutput = 0 # sum of all hourly energy outputs (in Watts)
    panelCount = 3 # how many panels are in this grid?
    hour = 0 # what hour of the day is it? (0-23)
    #hourlyMultiplier = 1; # how the hour of the day affects output - day vs. night
    
    weather = ["clear", "cloudy", "stormy"] # weather has impact on UV index, can either be clear, cloudy, or stormy
    currentWeather = "clear" # displays current weather conditions
    uvMultiplier = 1 # depending on what the UV index and weather is, this will impact the hourly energy output

    temperature = random.randint(60, 95) # temperature in fahrenheit
    tempMultiplier = 1 # temperature has impact on tempMultiplier, which affects hourly energy output (temp sweetspot is 60-95 F)
    
    graphHour = 3 # x value at start of graph
    EPB0.DLineH(graphHour, 10, graphHour + (5 * 24)) # bold horizantal line on bottom for graph base
    EPB0.PrtLtxt("Hourly", 5, 13, 0)
    EPB0.PrtLtxt("Output:", 5, 11, 0)
    EPB0.PrtStxt("panels: " + str(panelCount), 130, 2, 0)
    
    
    
    # loop for entire day
    while hour < 24:
        estHourlyOutput = 400 # estimated amount of power (in Watts) that a panel will produce in 1 hour (perfect conditions)
        uvIndex = 12 # Ultraviolet index rating; the higher, the more energy it gets
        
        # no numpy in micropython so I'll hafta make the bell curve myself
        if hour <= 4 or hour >= 19:
            uvMultiplier = .1
        elif hour <= 5 or hour >= 18:
            uvMultiplier = .15
        elif hour <= 6 or hour >= 17:
            uvMultiplier = .2
        elif hour <= 7 or hour >= 16:
            uvMultiplier = .45
        elif hour <= 8 or hour >= 15:
            uvMultiplier = .75
        elif hour <= 9 or hour >= 14:
            uvMultiplier = .9
        elif hour <= 10 or hour >= 13:
            uvMultiplier = .95
        else:
            uvMultiplier = 1
        
        
        # temperature climbs or declines depending on time of day
        if hour < 12:
            temperature += random.randint(-3, int(hour * .5))
        elif hour >= 12:
            temperature += random.randint(int((12-hour) * .5), 3)
        
        # weather determines UV level    
        if (hour+1) % 4 == 0:
            currentWeather = random.choice(weather)
            
        if currentWeather == "clear":
            uvMultiplier *= 1.2
            temperature += random.randint(2, 5)
        elif currentWeather == "cloudy":
            uvMultiplier *= .7
            temperature -= random.randint(2, 5)
        elif currentWeather == "stormy":
            uvMultiplier *= .4
            temperature -= random.randint(4, 7)
        
        # temperature impact
        if temperature < 32:
            temperature += random.randint(0, 8)
        elif temperature > 123:
            temperature -= random.randint(0, 8)    
        
        if temperature >= 60 and temperature <= 95:
            tempMultiplier = 1
        elif temperature > 95:
            tempMultiplier = 1 - (.01 * (temperature - 95))
        elif temperature < 60:
            tempMultiplier = 1 - (.01 * (60 - temperature))
            
        # putting environmental multipliers into effect
        estHourlyOutput *= uvMultiplier
        estHourlyOutput *= tempMultiplier
        estHourlyOutput *= panelCount
        uvIndex = int(uvIndex * uvMultiplier)
        hourlyOutput = int(estHourlyOutput)
        outHr = "hourly output = " + str(hourlyOutput) # python concatenation is weird :/
        print(outHr)
        print(currentWeather)
        print("temperature: ",temperature)
        dailyOutput += hourlyOutput
        
        # display updates to show status of grid:
        EPB0.PrtStxt("hour: " + str(hour), 130, 14, 0)
        EPB0.PrtStxt("output: " + str(hourlyOutput) + " W ", 130, 12, 0) # the two spaces at the end are important because it prevents the 3rd digit from staying when there are 2 digit outputs near later hours
        EPB0.PrtStxt("daily: " + str(dailyOutput) + " W ", 130, 10, 0)
        EPB0.PrtStxt("weather:" + str(currentWeather) + " ", 130, 8, 0)
        EPB0.PrtStxt("temp (F): " + str(temperature) + " ", 130, 6, 0)
        EPB0.PrtStxt("UV index: " + str(uvIndex) + " ", 130, 4, 0)
        EPB0.PrtStxt("Avg out: " + str(int(hourlyOutput / panelCount)) + " W ", 130, 0, 0)
        EPB0.Rect(graphHour, 10, 5, int((hourlyOutput * .1)/ panelCount)) # grphs hourly power output in graph on left side each hour
        epd.display(EPB0.Beeld) # updates display with full refresh
        
        # for example purposes, the delay time below is set to 4000 milliseconds, or 4 second(s)
        # change number below to 3600000 for an actual hour
        epd.delay_ms(1000) # time between loops, shuts off power to display, meaning it can't be updated yet it maintains the image
        
        graphHour += 5
        hour += 1 #last operation in this while loop
    
    
    print(graphHour)
    #epd.display(EPB0.Beeld) # Beeld is being called as an image: THIS IS WHAT MAKES STUFF APPEAR
    #epd.delay_ms(2000) # shuts off power to display, meaning it can't be updated yet it maintains the image
    epd.Clear(0xff) # clears the display
    epd.delay_ms(2000)
    epd.sleep()
