#importing customtkinter and widgets necessary
import customtkinter
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
import database 
from PIL import Image
import webbrowser
 
#database connections for sign up and login/ remove whitespaces with strip on some functions below
# this checks for id and username to be unique, if so, account can then be made successfully
def checkfields():
    username_entry = username.get().strip()
    password_entry = password.get().strip()
    id_entry = id.get().strip()
    
    if id_entry and username_entry and password_entry:
        #keeps track of user logged in
        global loggedin_id
        loggedin_id = id_entry
        if database.idcheck(id_entry):
            messagebox.showerror("Error", "ID already exists")
        elif database.usernamecheck(username_entry):
            messagebox.showerror("Error", "Username taken")
        else:
            database.insertaccountdata(id_entry, username_entry, password_entry)
            messagebox.showinfo("User created", "Account successfully created.")
            loginbutton()
    else:
        messagebox.showerror("Error", "Please enter ID, username, and password")

#login in function
def logincheckfields2():
     username_entry2 = username2.get().strip()
     password_entry2 = password2.get().strip()
     id2_entry = id2.get().strip()

     if id2_entry and username_entry2 and password_entry2:
          if database.verify_user(id2_entry, username_entry2, password_entry2):
           #keep track of user logged in
           global loggedin_id
           loggedin_id = id2_entry
           loginbutton()
           messagebox.showinfo("User verified", "Successfully Logged in")
          else:
           messagebox.showerror("Error", "Failed to sign in, incorrect credentials")
     else:
          messagebox.showerror("Error", "Incorrect ID, username or password")
 
# database connection for session page
def sessionfunc():
    option1_entry = sessID.get().strip()
    option2_entry = showwatched.get().strip()
    option3_entry = numofcycles.get().strip()
    option4_entry = cyclelength.get().strip()
    option5_entry = topicstudied.get().strip()

    global loggedin_id

    if not (option1_entry and option2_entry and option3_entry and option4_entry and option5_entry):
     messagebox.showinfo("Error", "Enter all fields")
    elif database.verify_sessID(option1_entry):
         messagebox.showinfo("Error", "Session ID already exists")
    else:
        database.insertsessiondata(option1_entry, loggedin_id ,option2_entry, option3_entry, option4_entry, option5_entry)
        confirmsession()
        messagebox.showinfo("Success", "Session saved")

#connection with database to enter all shows in listbox, goes through the list of shows enters end of listbox
def displayshowswatched():
    showswatched = database.getshowdata(loggedin_id)
    if not showswatched:
        messagebox.showinfo("Error", "No shows available.")
    for show in showswatched:
        #displays all shows in database associated to logged in user
        showslist.insert(END, show[0])
#shows all the sessions based off users/ similar to function above/ upacks from "session" into the following variables and displays on listbox
def displaysessions():
    sessionsmade = database.getsessiondata(loggedin_id)
    if not sessionsmade:
        messagebox.showinfo("Error", "No sessions available.")
    for session in sessionsmade:
        sessID, show_watched, num_of_cycles ,cycle_length, topic_studied, id = session
        # concatenation simiar to display total shows watched function
        session_details = ("SessID: " + str(sessID) + ", Show: " + str(show_watched) +", Cycles: " + str(num_of_cycles) + ", Cycle Length: " + str(cycle_length) + ", Topic: " + topic_studied + ", id: " + str(id))
        sessionslist.insert(END, session_details)

#saves date,topic and show for the user for planning
def saveplan():
    selectdate = cal.get_date()
    topicforstudy = topicstorevise.get().strip()
    futureshowwatch = showtowatch.get().strip()
    reset_pages()
    planexists = database.gettimetabledata(loggedin_id,selectdate)
    if planexists is not None:
        messagebox.showerror("Error","Plan already exists")
        return
    if not selectdate:
        messagebox.showinfo("Error","Please select a date")
    if not (selectdate and topicforstudy and futureshowwatch):
       messagebox.showinfo("Error", "Enter all fields")
    else:
        database.inserttimetabledata(loggedin_id,selectdate,topicforstudy,futureshowwatch)
        messagebox.showinfo("Success", "Saved Plan")
#similar to above, this time it updates the plan on a specific data if user wants to change some fields.
def updateplan():
    selectdate = cal.get_date()
    topicforstudy = topicstorevise.get().strip()
    futureshowwatch = showtowatch.get().strip()
    reset_pages()
    planexists = database.gettimetabledata(loggedin_id,selectdate)
    if planexists is None:
        messagebox.showerror("Error","No available plan to update")
        return
    if not selectdate:
        messagebox.showinfo("Error","Please select a date")
    if not (selectdate and topicforstudy and futureshowwatch):
       messagebox.showinfo("Error", "Enter all fields")
    else:
        database.updatetimetabledata(loggedin_id,selectdate,topicforstudy,futureshowwatch)
        messagebox.showinfo("Success", "Updated Plan")

    #displays the plan for the user if there is a plan set for a specific date.
def showplan():
    selectdate = cal.get_date()
    plan = database.gettimetabledata(loggedin_id, selectdate)
    #goes through the tuple
    if plan:
        #in order in table
        topicsplanned = plan[0]
        showlist = plan[1]
        date = plan[2]
        messagebox.showinfo("Saved Plan", f"Date: {date}\nTopics to Revise: {topicsplanned}\nShow to Watch: {showlist}")
    else:
        messagebox.showinfo("No Plan Found", "No topics or shows saved for the selected date.")

#Functions for buttons to go page to page, removes widgets go to diff pages
def loginbutton():
    for widget in window.winfo_children():
        widget.pack_forget()
        signuppage.pack_forget()
        homepage.pack()

def sessionbutton():
    for widget in window.winfo_children():
        widget.pack_forget()
    sessionpage.pack()
    reset_pages()

def confirmsession():
     for widget in window.winfo_children():
        widget.pack_forget()
        timerpage.pack()

def finishsessionbutton():
    for widget in window.winfo_children():
        widget.pack_forget()
        timerpage.pack_forget()
        homepage.pack()
        #reset the timer back to zero, taken from the default state of 00:00:00 at the starttimer section
        global second, minute, hour, stop
        second = 0
        minute = 0
        hour = 0
        stop = True
        stopwatch.configure(text=f"{hour:02}:{minute:02}:{second:02}")

def trackshowsbutton():
    for widget in window.winfo_children():
        widget.pack_forget()
    trackshowspage.pack()
    reset_pages()

def tracksessionsbutton():
    for widget in window.winfo_children():
        widget.pack_forget()
    tracksessionspage.pack()
    reset_pages()

def timetablebutton():
    for widget in window.winfo_children():
        widget.pack_forget()
    timetablepage.pack()
    reset_pages()

def signoutbutton():
    homepage.pack_forget()
    loginpage.pack()
    reset_pages()

def backbuttonlogin():
    loginpage.pack_forget()
    signuppage.pack(expand=True, fill='both')
    signuppagebackground2.place(x=0,y=0,relwidth=0.30, relheight=1)
    reset_pages()

def backbuttonsession():
        sessionpage.pack_forget()
        homepage.pack()
        #stops the flickering of images navigating page to page
        signuppagebackground2.place_forget()
        
def backbuttonshows():
        trackshowspage.pack_forget()
        homepage.pack()
        signuppagebackground2.place_forget()

def backbuttontracksession():
        tracksessionspage.pack_forget()
        homepage.pack()
        signuppagebackground2.place_forget()

def backbuttontimetable():
        timetablepage.pack_forget()
        homepage.pack()
        signuppagebackground2.place_forget()

#fetching the shows from the table after button is clicked
def displayshowbutton():
    displayshowswatched()
    displayshowcount()

#fetching the session data from the table after the button is clicked
def displaysessionbutton():
    displaysessions()
    displaysessioncount()

def signup():
    for widget in window.winfo_children():
        widget.pack_forget()
        homepage.pack_forget()
    loginpage.pack()
    
 
#clears all the fields by deleting all the characters
def reset_pages():
    #login
    id2.delete(0, 'end')
    username2.delete(0, 'end')
    password2.delete(0, 'end')
    #signup
    id.delete(0, 'end')
    username.delete(0, 'end')
    password.delete(0, 'end')
    #sessions
    sessID.delete(0, 'end')
    #getid.delete(0, 'end')
    showwatched.delete(0, 'end')
    cyclelength.set("")
    numofcycles.set("")
    topicstudied.delete(0, 'end')
    
    #trackshows
    showslist.delete(0, 'end')
    #tracksessions
    sessionslist.delete(0, 'end')
    #timetable
    topicstorevise.delete(0, 'end')
    showtowatch.delete(0, 'end')
    cal.selection_clear()

    
    numofshowslabel.configure(text="Total Shows Watched: ")
    numofsessionslabel.configure(text="Total Sessions Made: ")

#shows number of shows watched by the user/ using concatenation
def displayshowcount():
    numofshows = showslist.size()
    numofshowslabel.configure(text="Total Shows Watched: " + str(numofshows))

def displaysessioncount():
    numofsessions = sessionslist.size()
    numofsessionslabel.configure(text="Total Sessions Made: " + str(numofsessions))
# buttons that go to respective websites for users to watch their shows
def opennetflix():
    webbrowser.open("https://www.netflix.com/gb/")

def opencrunchyroll():
    webbrowser.open("https://www.crunchyroll.com")

second = 0
minute = 0
hour = 0
stop = True

def start():
    global second, minute, hour, stop
    if not stop:
        #time.sleep(1)
        #increments to then 60 then resets to 0 after first min,first hour etc.
        second += 1
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1
        stopwatch.configure(text=f"{hour:02}:{minute:02}:{second:02}")
        stopwatch.after(1000, start)

def stoptimer():
    global stop
    stop = True
    startbutton.configure(state="normal")
     
def restartimer():
    global stop
    startbutton.configure(state="disabled")
    stop = False
    start()

img1 = Image.open("netflix icon.png")
img2 = Image.open("crunchyroll")
img3 = Image.open("background3.png")
img4 = Image.open("background4.jpg")
img5 = Image.open("icon1.png")
img6 = Image.open("icon2.png")
img7 = Image.open("icon3.png")
img8 = Image.open("icon4.png")
img3 = customtkinter.CTkImage(dark_image=img3,light_image=img3,size=(1100,700))
img4 = customtkinter.CTkImage(dark_image=img4,light_image=img4,size=(450,700))

#creating window using customtkinter library 
window = customtkinter.CTk(fg_color="#6868ff")
window.geometry("1100x700")
window.resizable(False, False)
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("blue")
background1 = customtkinter.CTkLabel(window,text="",image=img4)
background1.place(x=1100,y=700, relwidth=0.30, relheight=1)

#sign up page design
title = customtkinter.CTkFont(family="Cascadia Code", size=60,weight="bold")
signuppage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0)
signuppage.pack(expand=True, fill='both')
signuppagebackground = customtkinter.CTkLabel(signuppage,text="",image=img3)
signuppagebackground.place(x=0,y=0, relwidth=1, relheight=1)
signuppagebackground2 = customtkinter.CTkLabel(signuppage,text="",image=img4)
signuppagebackground2.place(x=0,y=0, relwidth=0.30, relheight=1)
signuppagetitle = customtkinter.CTkLabel(signuppage, text="Signup to Continue",font=title, bg_color="#6868ff")
signuppagetitle.place(x=400,y=0)
#widgets for sign up page
idtext = customtkinter.CTkLabel(signuppage, text="ID",font=("Serif", 20), bg_color="#6868ff")
idtext.place(x=680,y=120)
id = customtkinter.CTkEntry(signuppage, height=30, width=300, font=("Serif", 20),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
id.place(x=550,y=150)
usernametext = customtkinter.CTkLabel(signuppage, text="Username",font=("Serif", 20), bg_color="#6868ff")
usernametext.place(x=650,y=220)
username = customtkinter.CTkEntry(signuppage, height=30, width=300, font=("Serif", 20),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
username.place(x=550,y=250)
passwordtext = customtkinter.CTkLabel(signuppage, text="Password",font=("Serif", 20), bg_color="#6868ff")
passwordtext.place(x=650,y=320)
password = customtkinter.CTkEntry(signuppage,height=30, width=300, font=("Serif", 20), fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff", show="*")
password.place(x=550,y=350)
buttonlogin = customtkinter.CTkButton(signuppage, text="Register", height=30, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=checkfields)
buttonlogin.place(x=550,y=450)
text1 = customtkinter.CTkLabel(signuppage, text="Already have an account?",font=("Serif", 14), bg_color="#6868ff")
text1.place(x=618,y=520)
signupbutton = customtkinter.CTkButton(signuppage, text="Login", height=20, width=220, font=("Serif", 20), fg_color="#8181ff", text_color="white",bg_color="#6868ff", command=signup)
signupbutton.place(x=590,y=550)


#loginpage design
loginpage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
loginpage.pack_propagate(False)
loginpagebackground = customtkinter.CTkLabel(loginpage,text="",image=img3)
loginpagebackground.place(x=0,y=0, relwidth=1, relheight=1)
loginpagebackground2 = customtkinter.CTkLabel(loginpage,text="",image=img4)
loginpagebackground2.place(x=0,y=0, relwidth=0.30, relheight=1)
loginlabel = customtkinter.CTkLabel(loginpage, text="Login",font=title, bg_color="#6868ff")
loginlabel.place(x=610,y=0)

#widgets for login page
id2text = customtkinter.CTkLabel(loginpage, text="ID",font=("Serif", 20), bg_color="#6868ff")
id2text.place(x=680,y=120)
id2 = customtkinter.CTkEntry(loginpage, height=30, width=300, font=("Serif", 20),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
id2.place(x=550,y=150)
usernametext2 = customtkinter.CTkLabel(loginpage, text="Username",font=("Serif", 20), bg_color="#6868ff")
usernametext2.place(x=650,y=220)
username2 = customtkinter.CTkEntry(loginpage, height=30, width=300, font=("Serif", 20),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
username2.place(x=550,y=250)
passwordtext2 = customtkinter.CTkLabel(loginpage, text="Password",font=("Serif", 20), bg_color="#6868ff")
passwordtext2.place(x=650,y=320)
password2 = customtkinter.CTkEntry(loginpage, height=30, width=300, font=("Serif", 20), fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff", show="*")
password2.place(x=550,y=350)
buttonlogin2 = customtkinter.CTkButton(loginpage, text="Login", height=30, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=logincheckfields2)
buttonlogin2.place(x=550,y=450)
text2 = customtkinter.CTkLabel(loginpage, text="Don't have an account?",font=("Serif", 14), bg_color="#6868ff")
text2.place(x=625,y=520)
backbutton = customtkinter.CTkButton(loginpage, text="Sign up", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=backbuttonlogin)
backbutton.place(x=600,y=550)

# homepage design 
homepage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
homepage.pack_forget()
homepage.pack_propagate(False)
homepagebackground = customtkinter.CTkLabel(homepage,text="",image=img3)
homepagebackground.place(x=0,y=0, relwidth=1, relheight=1)

homepagelabel = customtkinter.CTkLabel(homepage, text="Study2Watch",font=title, bg_color="#6868ff")
homepagelabel.pack(pady=20)

# All homepage buttons to proceed to respective pages
sessionbutton = customtkinter.CTkButton(homepage, text="Create a session", height=45, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#4d4dff",image=customtkinter.CTkImage(dark_image=img7,light_image=img7, size=(30,30)), command=sessionbutton)
sessionbutton.pack(pady=40, padx=60)

trackshowsbutton = customtkinter.CTkButton(homepage, text="Track your shows", height=45, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#4d4dff",image=customtkinter.CTkImage(dark_image=img5,light_image=img5, size=(30,30)),command=trackshowsbutton)
trackshowsbutton.pack(pady=45, padx=60)

tracksessionsbutton = customtkinter.CTkButton(homepage, text="Track your sessions", height=45, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#4d4dff",image=customtkinter.CTkImage(dark_image=img6,light_image=img6, size=(30,30)),command=tracksessionsbutton)
tracksessionsbutton.pack(pady=50, padx=60)

timetablebutton = customtkinter.CTkButton(homepage, text="Create a timetable", height=45, width=300, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#4d4dff",image=customtkinter.CTkImage(dark_image=img8,light_image=img8, size=(30,30)),command=timetablebutton)
timetablebutton.pack(pady=55, padx=60)

signoutbutton = customtkinter.CTkButton(homepage, text="Signout", height=30, width=150, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#4d4dff", command=signoutbutton)
signoutbutton.place(x=10, y=40)

# ensures frames are the same size as the window and not fixed
sessionpage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
sessionpage.pack_propagate(False)
trackshowspage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
trackshowspage.pack_propagate(False)
tracksessionspage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
tracksessionspage.pack_propagate(False)
timetablepage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
timetablepage.pack_propagate(False)
timerpage = customtkinter.CTkFrame(window, bg_color="transparent",border_width=0, width=1100, height=700)
timerpage.pack_propagate(False)

#sessionpage widgets 
sessionpagebackground = customtkinter.CTkLabel(sessionpage,text="",image=img3)
sessionpagebackground.place(x=0,y=0, relwidth=1, relheight=1)
sessionlabel = customtkinter.CTkLabel(sessionpage, text="Study2Watch",font=title, bg_color="#6868ff")
sessionlabel.pack(pady=20)
sessidtext = customtkinter.CTkLabel(sessionpage, text="ID",font=("Serif", 15), bg_color="#6868ff")
sessidtext.place(x=530,y=120) 
sessID = customtkinter.CTkEntry(sessionpage, height=18, width=130, font=("Serif", 15),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
sessID.place(x=470,y=150) 
showwatchedtext = customtkinter.CTkLabel(sessionpage, text="Show",font=("Serif", 15), bg_color="#6868ff")
showwatchedtext.place(x=520,y=200) 
showwatched = customtkinter.CTkEntry(sessionpage, height=20, width=220, font=("Serif", 15),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
showwatched.place(x=430,y=230) 
timeforcyclelabel = customtkinter.CTkLabel(sessionpage, text="Cycle length",font=("Serif", 15), bg_color="#6868ff")
timeforcyclelabel.place(x=500,y=290) 
cycletime = ["40 minutes","1 hour"]
cyclelength = customtkinter.CTkComboBox(sessionpage, values=cycletime,state="readonly", height=20, width=170, border_width=0,bg_color="#6868ff")
cyclelength.place(x=455,y=320) 

numofcyclelabel = customtkinter.CTkLabel(sessionpage, text="Total cycles",font=("Serif", 15), bg_color="#6868ff")
numofcyclelabel.place(x=500,y=390)
cycles = ["1", "2", "3","4"]
numofcycles = customtkinter.CTkComboBox(sessionpage, values=cycles,state="readonly" ,height=20, width=170,border_width=0,bg_color="#6868ff")
numofcycles.place(x=455,y=420) 
topicstudiedtext = customtkinter.CTkLabel(sessionpage, text="Topic studied",font=("Serif", 15), bg_color="#6868ff")
topicstudiedtext.place(x=500,y=490) 
topicstudied = customtkinter.CTkEntry(sessionpage, height=20, width=220, font=("Serif", 15),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
topicstudied.place(x=430,y=520) 
confirmbutton = customtkinter.CTkButton(sessionpage, text="Confirm", height=18, width=130, font=("Serif", 15), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=sessionfunc)
confirmbutton.place(x=470,y=590) 
backbutton1 = customtkinter.CTkButton(sessionpage, text="Go back", height=28, width=200, font=("Serif", 15), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=backbuttonsession)
backbutton1.place(x=10, y=40)

 #trackshows widgets
trackshowspagebackground = customtkinter.CTkLabel(trackshowspage,text="",image=img3)
trackshowspagebackground.place(x=0,y=0, relwidth=1, relheight=1)
showslabel = customtkinter.CTkLabel(trackshowspage, text="Study2Watch",font=title, bg_color="#6868ff")
showslabel.pack(pady=20)
numofshowslabel= customtkinter.CTkLabel(trackshowspage, text="Total Shows Watched: ", font=("Serif", 17), bg_color="#6868ff")
numofshowslabel.pack(pady=40)
addshow = customtkinter.CTkButton(trackshowspage, text="Display Shows", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=displayshowbutton)
addshow.place(y=200, x=440)
showslist = Listbox(trackshowspage, height=30, width=75, font=("Serif", 12))
showslist.place(x=200, y=250)
backbutton2 = customtkinter.CTkButton(trackshowspage, text="Go back", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=backbuttonshows)
backbutton2.place(x=10, y=40)

#tracksessions widgets
tracksessionspagebackground = customtkinter.CTkLabel(tracksessionspage,text="",image=img3)
tracksessionspagebackground.place(x=0,y=0, relwidth=1, relheight=1)
showslabel = customtkinter.CTkLabel(tracksessionspage, text="Study2Watch",font=title, bg_color="#6868ff")
showslabel.pack(pady=20)
numofsessionslabel= customtkinter.CTkLabel(tracksessionspage, text="Total Sessions Made: ", font=("Serif", 17), bg_color="#6868ff")
numofsessionslabel.pack(pady=40)
recapsession = customtkinter.CTkButton(tracksessionspage, text="Click to recap session", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=displaysessionbutton)
recapsession.place(y=200, x=440)
sessionslist = Listbox(tracksessionspage, height=30, width=75, font=("Serif", 12))
sessionslist.place(x=200, y=250)
backbutton3 = customtkinter.CTkButton(tracksessionspage, text="Go back", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=backbuttontracksession)
backbutton3.place(x=10, y=40)

#timetable widgets
timetablepagebackground = customtkinter.CTkLabel(timetablepage,text="",image=img3)
timetablepagebackground.place(x=0,y=0, relwidth=1, relheight=1)
timerlabel = customtkinter.CTkLabel(timetablepage, text="Study2Watch",font=title, bg_color="#6868ff")
timerlabel.pack(pady=20)
cal = Calendar(timetablepage, selectmode='day', locale='en_UK',bordercolor="black",normalbackground="#9A9AFF",weekendbackground="#9A9AFF",headersbackground="white",background="#9A9AFF",foreground="white",selectforeground="black",selectbackground="#5A5AB2")
cal.pack(padx=30, pady=30)
topicstostoretext = customtkinter.CTkLabel(timetablepage, text="Topic for plan",font=("Serif", 15), bg_color="#6868ff")
topicstostoretext.place(x=500,y=350) 
topicstorevise= customtkinter.CTkEntry(timetablepage, height=30, width=300, font=("Serif", 15),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
topicstorevise.pack(pady=20)
showtowatchtext = customtkinter.CTkLabel(timetablepage, text="Show to watch",font=("Serif", 15), bg_color="#6868ff")
showtowatchtext.place(x=500,y=430) 
showtowatch = customtkinter.CTkEntry(timetablepage,height=30, width=300, font=("Serif", 15),fg_color="#8181ff", placeholder_text_color="white", border_width=0, bg_color="#6868ff")
showtowatch.pack(pady=30)
savesession = customtkinter.CTkButton(timetablepage, text="Save Plan", height=30, width=300, font=("Serif", 15),fg_color="#8181ff", border_width=0, bg_color="#6868ff", command=saveplan)
savesession.place(x=400,y=520) 
updatedplan = customtkinter.CTkButton(timetablepage, text="Update Plan", height=30, width=300, font=("Serif", 15),fg_color="#8181ff", border_width=0, bg_color="#6868ff", command=updateplan)
updatedplan.place(x=400,y=580)
displayplan = customtkinter.CTkButton(timetablepage, text="Display Plan", height=30, width=300, font=("Serif", 15),fg_color="#8181ff", border_width=0, bg_color="#6868ff", command=showplan)
displayplan.place(x=400,y=640)
backbutton4 = customtkinter.CTkButton(timetablepage, text="Go back", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=backbuttontimetable)
backbutton4.place(x=10, y=40)

#timer widgets
timerpagebackground = customtkinter.CTkLabel(timerpage,text="",image=img3)
timerpagebackground.place(x=0,y=0, relwidth=1, relheight=1)
timerlabel = customtkinter.CTkLabel(timerpage, text="Study2Watch",font=title, bg_color="#6868ff")
timerlabel.pack(pady=20)
instructionlabel = customtkinter.CTkLabel(timerpage, text="Time yourself based on selected time slots allocated. Once you are done with all cycles, press finish.",font=(title,14),bg_color="#6868ff")
instructionlabel.pack(pady=30)
stopwatch = customtkinter.CTkLabel(timerpage, text=f"{hour:02}:{minute:02}:{second:02}", font=("title", 50),bg_color="#6868ff")
stopwatch.place(x=450, y=200)
startbutton = customtkinter.CTkButton(timerpage, text="Start", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=restartimer)
startbutton.place(x=340, y=270)
stopbutton = customtkinter.CTkButton(timerpage, text="Stop", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", command=stoptimer)
stopbutton.place(x=560, y=270)
netflixbutton = customtkinter.CTkButton(timerpage, text="Open Netflix", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff", image=customtkinter.CTkImage(dark_image=img1,light_image=img1) ,command=opennetflix)
netflixbutton.place(x=450, y=350)
crunchyrollbutton = customtkinter.CTkButton(timerpage, text="Open Crunchyroll", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",image=customtkinter.CTkImage(dark_image=img2,light_image=img2),command=opencrunchyroll)
crunchyrollbutton.place(x=450, y=450)
finishbutton = customtkinter.CTkButton(timerpage, text="Finish", height=30, width=200, font=("Serif", 20), fg_color="#8181ff", text_color="white", border_width=0, bg_color="#6868ff",command=finishsessionbutton)
finishbutton.place(x=450, y=550)

window.mainloop()