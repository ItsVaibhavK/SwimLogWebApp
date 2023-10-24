# SWIM LOG WEB APP

#### Description:
## IDEA BEHIND SWIMLOG AS A WEB APP
The basic command-line version of this program was originally written for my final project for [CS50P (2023)](https://cs50.harvard.edu/python/2022/).<br>I decided to take that basic Python program, and elevate it to a web app using the various tools and technologies I learnt in [CS50X (2023)](https://cs50.harvard.edu/x/2023/).

_Note:_ This README file contains common sections borrowed from the original [Swim Log](https://github.com/ItsVaibhavK/SwimLog.git) project as some of the explanation remains the same,<br>like the inspiration behind it, thought process, etc.


As a person who swims fairly regularly for exercise, I wanted to track my basic swimming data, like:
- Distance swam in a session
- Pool length
- Duration of a session

And to be able to analyze the data, with parameters such as:
- Total distance swam
- Total time spent swimming
- Average distance swam per session
- Average duration of a session

Before I decided to turn this idea into my final project for [CS50P (2023)](https://cs50.harvard.edu/python/2022/) and [CS50X (2023)](https://cs50.harvard.edu/x/2023/), I was trying out various swim-tracking apps on my phone,<br>but they were all invariably too cluttered for my taste. More often than not, it was about pushing the user to sign up for swimming lessons,<br>or to connect a smart watch that would share your swimming session data to the app for you.

Most of the apps had the option to manually update your swimming session data, but it was almost always without fail locked behind a paywall.<br>This is what ultimately led me to utilize what I have been learning through [CS50P (2023)](https://cs50.harvard.edu/python/2022/) and [CS50X (2023)](https://cs50.harvard.edu/x/2023/) and create a Python program<br>to allow me to log/track the data from my swimming sessions.

From the initial command-line Python program version of [Swim Log](https://github.com/ItsVaibhavK/SwimLog.git), I decided to turn it into a web app utilizing Flask, Python, SQL, Bootstrap, and more.

## HOW SWIM LOG WORKS
### Libraries used:
- **cs50** - Using `from cs50 import SQL` enables the program to talk to the SQLite3 database, so that SQL queries can be executed within Python code.

- **flask** - Light web framework written in Python that enables Python code to run within HTML using Jinja, a templating langauge.

- **werkzeug.security** - Library that helps keep user passwords encrypted.

- **flask_session** - To keep track of user's session data.

### Files in this project:
- **app.py** - Contains the main code that makes this project run.

- **swimlog.db** - The SQLite3 database that stores user data in two tables, `users` and `swim_data`.

- **helpers.py** - Helper functions for **app.py**.

- **requirements.txt** - Lists all the pip-installable modules used.

- **README.md** - The current file.

- **add.html** - HTML file for the page that allows the user to add new data.

- **apology.html** - HTML file for the page that displays an error code and message.

- **change.html** - HTML file for the page that allows the user to change their password.

- **delete.html** - HTML file for the page that allows th user to delete data from `swim_data`.

- **index.html** - HTML file for the home page.

- **layout.html** - HTML file for the base template page.

- **login.html** - HTML file for the page that allows the user to log in.

- **modify.html** - HTML file for the page that allows the user to modify existing data.

- **register.html** - HTML file for the page that allows a new user to register.

- **styles.css** - CSS file/stylesheet.

- **favicon.ico** - Branding image for the web app.

- **logo.png** - Branding image for the web app.

### Schema for data tables:
These were the **SQL commands** run to create the data tables:

CREATE TABLE users (<br>id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,<br>username TEXT NOT NULL,<br>hash TEXT NOT NULL<br>);

CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE swim_data (<br>session INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,<br>user_id INTEGER NOT NULL,<br>date DATETIME DEFAULT CURRENT_TIMESTAMP,<br>distance INTEGER NOT NULL,<br>pool INTEGER NOT NULL,<br>duration INTEGER NOT NULL,<br>FOREIGN KEY (user_id) REFERENCES users(id)<br>);

### Operations:

The web app takes the user to the `login` page by default. No other page can be accessed without logging in, thanks to the decorator `@login_required`.<br>While logged out, the only navbar options are `Register` and `Log in`.

Once logged in, the web app goes to the `home` page. The user is greeted with a welcome message.<br>Here, the user's existing swim data is displayed as a table, with the following analytics under it:
- Total distance swam: in meters if under a kilometer, in kilometers otherwise.
- Average distance swam per session: in meters if under a kilometer, in kilometers otherwise.
- Total time spent swimming: in minutes if under an hour, in hour(s) and minute(s) otherwise.
- Average time spent swimming per session: in minutes if under an hour, in hour(s) and minute(s) otherwise.

Since a first-time user would not have any existing swimming data to display, they are taken to the `Add New Data` page by default.<br>Once data is added, they are taken to the `home` page.

The `home` page navbar presents the user with the options to `Change Password` and `Log Out`.

Under all this info, the user is presented with three buttons:
- **Add New Data** - Add new data to their `swim_data` table.
- **Modify Existing Data** - Modify existing data from their `swim_data` table using `session` number.
- **Delete Data** - Delete data from their `swim_data` table using `session` number.




## DESIGN THOUGHTS AND FUTURE IDEAS:
1. [Bootstrap](https://getbootstrap.com/) is utilized quite heavily throughout this project to beautify the web app.

2. [CS50X (2023)](https://cs50.harvard.edu/x/2023/)'s Week 9 problem, [C$50 Finance](https://cs50.harvard.edu/x/2023/psets/9/finance/), was used as a base to build this web app, especially to figure out user-related data<br>and features such as logging in, logging out, helper functions, etc.

3. Distance covered in a session, pool length, and the duration of a session are the current parameters that are the focus of Swim Log<br>since these are the main parameters I care about for my personal data. I would, however, like to also consider adding parameters<br>such as number of laps and swim pace.

4. The program currently only stores/calculates distance data under the metric system. An idea for a future version of Swim Log could be to<br>provide the option of selecting what system of measurement the user would like to implement.

5. Currently, the date/timestamp data is not used in any way apart from a form of record-keeping.<br>Utilizing the date/timestamp data to see milestones like start date, year, etc. can also be considered.

## CREDITS, CONCLUSION:
I cannot express my gratitude and admiration of the staff and team at CS50 enough for sharing their knowledge with students like me,<br>and for their time, effort and dedication behind the plethora of courses offered by Harvard's CS50 on [edX.](https://www.edx.org/) I went from not knowing anything about programming at all<br>to writing my own programs and web apps in these last few months.<br>Thank you from the bottom of my heart for instilling in me the love of all things programming!

_To quote [Professor Malan](https://cs.harvard.edu/malan/):_
> This was CS50!
