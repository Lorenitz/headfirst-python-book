from flask import Flask, session, render_template
import swimclub
import os

app = Flask(__name__)
app.secret_key = "You will never guess..."


#This function doesn't return anything
def populate_data():
    #The if statements ensures the session is populated only when necessary
    if "swimmers" not in session:
        swim_files = os.listdir(swimclub.FOLDER)
        swim_files.remove(".DS_Store")
        
        session["swimmers"] = {}
        
        for file in swim_files:
            name, *_ = swimclub.read_swim_data(file)
            if name not in session["swimmers"]:
                session["swimmers"][name] = []
            session["swimmers"][name].append(file)
            

#The "/swimmers"URL responds to a HTTP GET Request.
@app.get("/swimmers")
#The function's signature.
def display_swimmers():
    populate_data()
    return str(sorted(session["swimmers"]))


@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])
   
app.run(debug=True)


@app.get("/")
def index():
    return render_template("index.txt")
        
if __name__ == "__main__":
    app.run()
    
