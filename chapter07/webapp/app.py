from flask import Flask, session, render_template, request
import swimclub
import os

app = Flask(__name__)
app.secret_key = "You will never guess..."


@app.get("/")
def index():
    return render_template(
        "index.html",
        title="Welcome to the Swimclub",
    )
    
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

#The "/swimmers" URL responds to a HTTP GET Request.
@app.get("/swimmers")
#The function's signature.
def display_swimmers():
    populate_data()
    return render_template(
        "select.html",
        title="Select a swimmer",
        url="/showfiles",
        select_id="swimmer",
        data=sorted(session["swimmers"]),   
    )

@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])
   
@app.post("/showfiles")
def display_swimmer_files():
    populate_data()
    name = request.form["swimmer"]
    return render_template (
        "select.html",
        title ="Select an event",
        url="/showbarchart",
        select_id="file",
        data=session["swimmers"][name],
    )   

@app.post("/showbarchart")
def show_bar_chart():
    file_id = request.form["file"]
    location = swimclub.produce_bar_chart(file_id, "templates/")
    return render_template(location.split("/")[-1])   
           
if __name__ == "__main__":
    app.run(debug=True)
    
