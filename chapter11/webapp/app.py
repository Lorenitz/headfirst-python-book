from flask import Flask, session, render_template, request
import swimclub
import os
import data_utils
import convert_utils

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

#This @app line needs to use post as opposed to get, as the URL has data posted to id
@app.post("/swimmers")
def display_swimmers():
    #The line below does double-duty. It grabs the data sent from the HTML form, then saves it to Flask's session variable
    session["chosen_date"] = request.form["chosen_date"]
    data = data_utils.get_session_swimmers(session["chosen_date"])
    swimmers = [f"{swimmer[0]}-{swimmer[1]}" for swimmer in data]
    return render_template(
        "select.html",
        title = "Select a swimmer",
        url="/showevents",
        select_id="swimmer",
        data=sorted(swimmers),        
    )



@app.get("/swims")
def display_swim_sessions():
    data = data_utils.get_swim_sessions()
    dates = [session[0].split(" ")[0] for session in data]
    return render_template(
        "select.html",
        title="Select a swim session",
        url="/swimmers",
        select_id="chosen_date",
        data=dates,
    )    






@app.get("/files/<swimmer>")
def get_swimmers_files(swimmer):
    populate_data()
    return str(session["swimmers"][swimmer])


   
@app.post("/showevents")
def display_swimmer_events():
   session["swimmer"], session["age"] = request.form["swimmer"].split("-")
    #grab the data you need from your database engine 
    #The values of the placeholder variables are taken from Flask's "session" variable.
   data = data_utils.get_swimmers_events(session["swimmer"], session["age"], session["chosen_date"])
   
   #Perform the necessary transformation
   events = [f"{event[0]}{event[1]}" for event in data]
   
   #There are a few minor changes here to ensure the code refers to event and events instead of files
   return render_template(
       "select.html",
       title="Select an event",
       url="/showbarchart",
       select_id="event",
       data=events,
   )
   
   
   

@app.post("/showbarchart")
def show_bar_chart():
    distance, stroke = request.form["event"].split("-")
    data = data_utils.get_swimmers_times(
        session["swimmer"],
        session["age"],
        distance,
        stroke,
        session["chosen_data"]
    )
    times = [time[0] for time in data]
    
    #perform the conversions
    average_str, times_reversed, scaled = convert_utils.perform_conversions(times)
    
    #Grab the four world record times
    world_records = convert_utils.get_wolrds(distance, stroke)
    
    #using a fstring to create a page header
    header = f"{session['swimmer']}(Under {session['age']}) {distance} {stroke} - {session['chosen_date']}"
    
    return render_template(
        "chart.html",
        title=header,
        data=list(zip(times_reversed, scaled)),
        average=average_str,
        worlds=world_records,
        
    )
    
    file_id = request.form["file"]
    location = swimclub.produce_bar_chart(file_id, "templates/")
    return render_template(location.split("/")[-1])   













           
if __name__ == "__main__":
    app.run(debug=True)
    
