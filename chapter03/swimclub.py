import statistics
#Splitting the file name into variables
FOLDER = "../swimdata/"

def read_swim_data(filename):
    swimer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    # Retrieving data from file
    with open(FOLDER + filename) as file:
        lines = file.readlines()
        # Remember, that strip remove the break line
        times = lines[0].strip().split(",")
    
    converts = []
    
    for t in times:
        minutes, rest = t.split(":")
        seconds, hundredths = rest.split(".")
        
        converts.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths))
        
    average = statistics.mean(converts)    
    
    round(average/ 100, 2) #86.56, where 86 - seconds, 56 - hundredths
    
    min_secs, hundredths = str(round(average / 100, 2)).split(".") # ['86', '58']
    
    mins_secs = int(mins_secs)
    
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    
    average = str(minutes) + ":" + str(seconds) + "." + hundredths
    
    #print(average)
    
    return average, swimer, age, distance, stroke