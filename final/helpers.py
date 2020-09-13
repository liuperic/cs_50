import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, message=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def interest(p, r, n, t, additional=0):
    """Calculates compounding interest.

    Arguments:
        p - (integer) Starting principal balance
        r - (float) Annual interest rate in decimal form.
        n - (integer) Number of compounding periods in a year.
        t - (integer) Number of years.
        additional - (float) Optional addition deposit at end of each compounding period

    Returns:
        Future value of principal with compounding interest
    """
    FV = p * pow((1 + r/n), t*n)

    # No zero-division
    if r > 0:
        deposit = additional*(pow((1+r), t) -1)/r

        return FV + deposit
    else:
        raise("Invalid interest rate")
