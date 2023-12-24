import statistics
import hfpy_utils
import os

# Get directory relative to this python file
# https://stackoverflow.com/a/5137509
dir_path = os.path.dirname(os.path.realpath(__file__))


CHARTS = "charts/"

#Splitting the file name into variables
FOLDER = "swimdata/"

def read_swim_data(filename):
    swimer, age, distance, stroke = filename.removesuffix(".txt").split("-")

    # Retrieving data from file
    with open(dir_path + "/" + FOLDER + filename) as file:
        lines = file.readlines()
        # Remember, that strip remove the break line
        times = lines[0].strip().split(",")
    
    converts = []
    
    for t in times:
        if ":" in t:
            minutes, rest = t.split(":")
            seconds, hundredths = rest.split(".")
         
        else:
            minutes = 0
            seconds, hundredths = t.split(".")
 
           
        converts.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths))
       
        
    average = statistics.mean(converts)    
    
    round(average/ 100, 2) #86.56, where 86 - seconds, 56 - hundredths
    
    #mins_secs, hundredths = str(round(average / 100, 2)).split(".") # ['86', '58']
    mins_secs, hundredths = f"{(average / 100):.2f}".split(".")
    
    mins_secs = int(mins_secs)
    
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    
    average = f"{minutes}:{seconds:0>2}.{hundredths}"
    
    return swimer, age, distance, stroke, times, average, converts


def produce_bar_chart(filename, location=CHARTS):
    """
    Given the name of a swimmer's file, produce a HTML/SVG-based bar chart.

    Save the chart to the CHARTS folder. Return the path to the bar chart file.
    """
    
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(filename)
    from_max = max(converts)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                        <head>
                        <body>
                            <h3>{title}</h3>"""
    body = f""
    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body + f""" 
                            <svg height="30" width="400">
                                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                            </svg>{t}<br />"""                             
    footer = f"""
                            <p>Average Time: {average}</p>
                        </body>
                    </html>"""
                    
    page = header + body + footer
    save_to = f"{dir_path}/{location}{filename.removesuffix('.txt')}.html"
    
    with open(save_to, "w") as sf:
        print(page, file=sf)
        
    return save_to    
    
                    
                    
                    
                                                