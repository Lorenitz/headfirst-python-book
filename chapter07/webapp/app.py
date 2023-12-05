from flask import Flask, session
import swimclub
import os

app = Flask(__name__)
app.secret_key = "You will never guess..."

#The "/swimmers"URL responds to a HTTP GET Request.
@app.get("/swimmers")

#The function's signature.
def display_swimmers():
    swim_files = os.listdir(swimclub.FOLDER)
    swim_files.remove(".DS_Store")
    
    session["swimmers"] = {}
    
    for file in swim_files:
        name, *_  = swimclub.read_swim_data(file)
        #To remove the duplicated ones
        if name not in session["swimmers"]:
            session["swimmers"][name] = []
        session["swimmers"][name].append(file)
    #The result of this function are converted to a string 
    #before they are returned (just in case)    
    return str(sorted(session["swimmers"]))


@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    return str(session["swimmers"][swimmer])
   
app.run(debug=True)
        
if __name__ == "__main__":
    app.run()
    
