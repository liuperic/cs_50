import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    cash_row = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash = cash_row[0]["cash"]

    # Total holdings
    holdings = db.execute("SELECT DISTINCT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    quotes = {}

    equity = 0
    for stock in holdings:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        curr_price = quotes[stock["symbol"]]["price"]
        equity += stock["total_shares"] * curr_price

    # Total including cash
    balance = cash + equity

    return render_template("index.html", quotes=quotes, holdings=holdings, cash=cash, balance=balance)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        # Make sure quote input not empty
        if not symbol:
            return apology("missing symbol")

        # Check if valid symbol
        quote = lookup(symbol)
        if quote == None:
            return apology("invalid symbol")

        # Get cash balance
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash_available = rows[0]["cash"]

        share_price = quote["price"]
        num_shares = request.form.get("shares")
        cost = int(num_shares) * share_price

        # Check if there's enough cash remaining for transaction
        if cash_available < cost:
            return apology('not enough cash')
        else:
            # Add transaction info to db
            db.execute("INSERT INTO transactions (symbol, shares, share_price, user_id, stock_name) VALUES(:symbol, :shares, :share_price, :user_id, :stock_name)",
                                                  symbol=symbol, shares=num_shares, share_price=share_price, user_id=session['user_id'], stock_name=quote["name"])
            # Update cash balance
            remaining_cash = cash_available - cost
            db.execute("UPDATE users SET cash = :remaining WHERE id = :user_id", remaining=remaining_cash, user_id=session["user_id"])

            flash(f"{num_shares} share(s) of {symbol} bought!")

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history_rows = db.execute("SELECT symbol, shares, share_price, execution_time FROM transactions WHERE user_id = :user_id ORDER BY execution_time DESC", user_id=session["user_id"])

    # Personal touch feature:
    # Display deposit funds below history of stock transactions
    fund_history = db.execute("SELECT deposit, time FROM funds WHERE user_id = :user_id", user_id=session["user_id"])


    return render_template("history.html", history=history_rows, deposits=fund_history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # Make sure quote symbol not empty
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")

        # Get quote symbol and store quote info in dict

        quote = lookup(symbol)

        # Make sure quote is valid
        if quote == None:
            return apology("invalid symbol")

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Add cash"""
    if request.method == "POST":

        # Cash validation check
        cash = int(request.form.get("cash"))
        if not cash:
            return apology("cash amount invalid")

        # Deposit cash and update database
        db.execute("UPDATE users SET cash = cash + :deposit WHERE id = :user_id", deposit=cash, user_id=session["user_id"])

        db.execute("INSERT INTO funds (deposit, user_id) VALUES(:deposit, :user_id)", deposit=cash, user_id=session["user_id"])

        flash("money deposited!")

        return redirect("/")

    else:
        return render_template("deposit.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Username cannot be blank
        if not request.form.get("username"):
            return apology("must provide username")

        # Password cannot be blank
        elif not request.form.get("password"):
            return apology("must provide password")

        # Password and confirmation password must match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match")

        # Username must be unique
        unique_user = db.execute("SELECT username FROM users where username = :username", username = request.form.get("username"))
        if unique_user:
            return apology("username is taken")

        # Generate password hash
        hash = generate_password_hash(request.form.get("password"))
        # Insert into databse
        user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                    username=request.form.get("username"), hash=hash)

        session["user_id"] = user_id
        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        holdings = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock_name = lookup(symbol)["name"]

        # Number of shares of specified stock owned
        shares_owned = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE symbol = :symbol AND user_id = :user_id",
                          symbol=symbol, user_id=session["user_id"])[0]["shares"]

        # Make sure quote input not empty
        if not symbol:
            return apology("missing symbol")

        # Check if valid symbol
        elif not shares:
            return apology("missing shares")

        # Make sure owns enough shares to sell
        elif shares_owned < shares:
            return apology("too many shares")

        # Current price of stock
        price = lookup(symbol)["price"]
        total_sale = price * shares

        # Add transaction
        db.execute("INSERT INTO transactions (user_id, symbol, shares, share_price, stock_name) VALUES(:user_id, :symbol, :shares, :share_price, :stock_name)",
                    user_id=session["user_id"], symbol=symbol, shares=-shares, share_price=price, stock_name=stock_name)

        # Update cash balance
        db.execute("UPDATE users SET cash = cash + :sale WHERE id = :user_id", sale=total_sale, user_id=session["user_id"])

        flash("Shares sold!")

        return redirect("/")


    else:
        holdings = db.execute("SELECT DISTINCT symbol FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])

        return render_template("sell.html", holdings=holdings)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


