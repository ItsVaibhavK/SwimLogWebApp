from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///swimlog.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """
    Show user's existing swim data and some data analysis.
    """
    data = db.execute(
        "SELECT * FROM swim_data WHERE user_id = :user_id",
        user_id=session["user_id"],
    )

    if not data:
        # First-time users, redirect to Add Data page
        return redirect("/add")
    else:
        # Total distance in meters
        distance_list = db.execute(
            "SELECT SUM(distance) AS d FROM swim_data WHERE user_id = :user_id",
            user_id=session["user_id"],
        )
        total_distance = distance_list[0]["d"]

        # Total time in minutes
        time_list = db.execute(
            "SELECT SUM(duration) AS t FROM swim_data WHERE user_id = :user_id",
            user_id=session["user_id"],
        )
        total_time = time_list[0]["t"]

        # Total number of sessions
        sessions_list = db.execute(
            "SELECT COUNT(*) AS s FROM swim_data WHERE user_id = :user_id",
            user_id=session["user_id"],
        )
        total_sessions = sessions_list[0]["s"]

        user_data = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"]
        )
        user = user_data[0]["username"]

        return render_template(
            "index.html",
            data=data,
            total_distance=total_distance,
            total_time=total_time,
            total_sessions=total_sessions,
            user=user,
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("please provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("please provide password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for username, password, password confirmation
        if not request.form.get("username"):
            return apology("please provide username")
        elif not request.form.get("password"):
            return apology("please provide password")
        elif not request.form.get("confirmation"):
            return apology("please provide password confirmation")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Query db for username and check it doesn't already exist
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            return apology("username already exists")

        # Add new user
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")),
        )

        # Query db for new user
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect to homepage
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for password, password confirmation
        if not request.form.get("password"):
            return apology("please provide password")
        elif not request.form.get("confirmation"):
            return apology("please provide password confirmation")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Update user table in db
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(request.form.get("password")),
            session["user_id"],
        )

        # Redirect to log in with new password
        session.clear()
        return redirect("/login")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for distance, pool length, duration
        if not request.form.get("distance"):
            return apology("please provide distance")
        elif not request.form.get("pool"):
            return apology("please provide pool length")
        elif not request.form.get("duration"):
            return apology("please provide duration")

        # Update swim_data table in db
        db.execute(
            "INSERT INTO swim_data(user_id, distance, pool, duration) VALUES(?, ?, ?, ?)",
            session["user_id"],
            request.form.get("distance"),
            request.form.get("pool"),
            request.form.get("duration"),
        )
        # Redirect user to homepage
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


@app.route("/modify", methods=["GET", "POST"])
@login_required
def modify():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for session number, distance, pool length, duration
        if not request.form.get("session_number"):
            return apology("please provide session number")
        elif not request.form.get("distance"):
            return apology("please provide distance")
        elif not request.form.get("pool"):
            return apology("please provide pool length")
        elif not request.form.get("duration"):
            return apology("please provide duration")
        # Validate session number provided by user
        user_input = int(request.form.get("session_number"))
        session_list = db.execute(
            "SELECT session FROM swim_data WHERE user_id = :user_id",
            user_id=session["user_id"],
        )
        id_list = []
        for number in session_list:
            if not number["session"] in id_list:
                id_list.append(number["session"])
        if not user_input in id_list:
            return apology("please enter a valid session number")
        else:
            # Update swim_data table in db
            db.execute(
                "UPDATE swim_data SET distance = ?, pool = ?, duration = ? WHERE session = ?",
                request.form.get("distance"),
                request.form.get("pool"),
                request.form.get("duration"),
                request.form.get("session_number"),
            )
            # Redirect user to homepage
            return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("modify.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check for session number
        if not request.form.get("session_number"):
            return apology("please provide session number")
        # Validate session number provided by user
        user_input = int(request.form.get("session_number"))
        session_list = db.execute(
            "SELECT session FROM swim_data WHERE user_id = :user_id",
            user_id=session["user_id"],
        )
        id_list = []
        for number in session_list:
            if not number["session"] in id_list:
                id_list.append(number["session"])
        if not user_input in id_list:
            return apology("please enter a valid session number")
        else:
            # Update swim_data table in db
            db.execute(
                "DELETE FROM swim_data WHERE session = ?",
                request.form.get("session_number"),
            )
            # Redirect user to homepage
            return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("delete.html")
