Project Setup Guide

Folder Structure

- Study2Watch.db: the database file that stores user data 
- gui.py: Contains all the graphical user interface which is needed for user interaction
- database.py: stores the database and all the necessary queries
- _pycache_: Contains cached version of the two .py files
- Multiple images: These images are necessary for the overall aesthetic of the UI

Installation

Before attempting to run this application, ensure that you have Python 3 installed

In terminal, run
Python --version

Prerequisites 

- Downloading Visual Studio Code
- Downloading the required Python packages, latest version preferable which is Python 3.12.3 (code was written in Python)
- Install the extension "SQLite Viewer" to see the database (Optional)


Instructions
1. There is two main files, gui.py and database.py which you can run, in which running the gui.py will start the application
2. Running the database file only runs the database and not the desktop application
3. The application opens up on the signup page in which you can create an account, upon doing so, you will be redirected to the homepage
4. If the user already has credentials, they can log in with those details
5. There are 4 buttons shown on the homepage, each leading to its respective pages
6. Create a session allows the user to make a unique revision sessions and once submitted, it is saved to that user in the database and redirects the user to the timer page, where there is a timer to time the session and links to Netflix and Crunchyroll for user viewing.
7. Track your shows displays your show count and the shows you have watched in every made session
8. Similarly, Track your sessions, shows every session in detail
9. Lastly, Create a timetable allows the user to save, display and update revision plans on specific dates
10.The user can log out and log in whenever they would like
