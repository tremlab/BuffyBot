from flask import Flask, jsonify, render_template, redirect, request, Response, flash, session
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import sms_functions
from jinja2 import StrictUndefined
import os
# twitter too!

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "s0Then!stO0dth34ean9a11iw4n7edto9ow4s8ur$7!ntOfL*me5")
app.jinja_env.endefined = StrictUndefined

AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
CALLER_ID = os.environ.get("TWILIO_CALLER_ID")


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

    sms_string = sms_functions.get_message()

    resp.message(sms_string)

    return str(resp)


@app.route("/message", methods=['POST'])
def awkward_text():
    """sends text to requested number."""
    # TODO need to create a page with form that accepts users phone input
    phone_raw = request.form.get("recipient")

    response = sms_functions.eval_phone(phone_raw)

    return redirect("/send_sms", response=response)


@app.route("/send_sms")
def send_SMS(response):

    if response[0] != "+":
        confirm_string = "not a valid phone number. try again!"
        return render_template("confirm_sms.html", response=confirm_string)
    else:
        sms_string = sms_functions.get_message()
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=recepient_phone,
            from_=CALLER_ID,
            body=sms_string,
            media_url="https://climacons.herokuapp.com/clear.png",
        )
        confirm_string = """confirmed!  sent '%s' to %s """ % (sms_string, response)
        return render_template("confirm_sms.html", response=confirm_string)

    

if __name__ == "__main__":
    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)
