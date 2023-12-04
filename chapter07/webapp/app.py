from flask import Flask
import swimclub
import os

app = Flask(__name__)

#The "/swimmers"URL responds to a HTTP GET Request.
@app.get("/swimmers")

#The function's signature.
def display_swimmers():
    swim_files = os.listdir(swimclub.FOLDER)
    swim_files.remove(".DS_Store")
    swimmers = {}
    
    for file in swim_files:
        name, *_  = swimclub.read_swim_data(file)
        if name not in swimmers:
            swimmers[name] = []
        swimmers[name].append(file)
    #The result of this function are converted to a string 
    #before they are returned (just in case)    
    return str(sorted(swimmers))      
        
if __name__ == "__main__":
    app.run()