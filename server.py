from flask import Flask, jsonify, render_template, redirect, request, Response, flash, session
import twitter
import sys
import os
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from jinja2 import StrictUndefined
import markov
import twilio_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "s0Then!stO0dth34ean9a11iw4n7edto9ow4s8ur$7!ntOfL*me5")
app.jinja_env.endefined = StrictUndefined

AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")
TWILIO_APP_SID = os.environ.get("TWILIO_TWIML_APP_SID")

# api = twitter.Api(
#     consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
#     consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
#     access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
#     access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# print api.VerifyCredentials()


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
    # TODO need to create a page with form that accepts users phone input
    phone_raw = request.form.get("mobile")
    response = phone_raw

    # response = sms_functions.eval_phone(phone_raw)
    sms_string = markov.get_quote("buffy_speechify.txt")
    confirm_string = twilio_functions.send_sms

    return render_template("confirm_sms.html", confirm_string=confirm_string)

    

if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
