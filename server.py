from flask import Flask, jsonify, render_template, redirect, request, Response, flash, session
import sys
import os
from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse
from jinja2 import StrictUndefined
import markov
import twilio_functions
import twitter_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "s0Then!stO0dth34ean9a11iw4n7edto9ow4s8ur$7!ntOfL*me5")
app.jinja_env.endefined = StrictUndefined

AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")
TWILIO_APP_SID = os.environ.get("TWILIO_TWIML_APP_SID")


@app.route("/", methods=['GET', 'POST'])
def homepage():
    """display homepage.
    """
    # build homepage, fomr to submit phone #
    return render_template("index.html")


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """this route responds to incoming texts.
    """
    resp = MessagingResponse()

    # buffy_text = markov.get_quote("buffy_speechify.txt")
    buffy_text = "that'll put marzipan in your pie plate, bingo!"

    resp.message(buffy_text)

    return str(resp)


@app.route("/message", methods=['POST'])
def ask_for_msg():
    phone_raw = request.form.get("mobile")

    mobile = twilio_functions.eval_phone(phone_raw)

    buffy_txt = twilio_functions.send_sms(mobile)

    twitter_functions.tweet_text(buffy_txt)

    confirm_string = """Marzipan! '%s' was texted to %s
    """ % (buffy_txt, mobile)

    return render_template("confirm_sms.html", confirm_string=confirm_string)


if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
