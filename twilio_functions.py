

def eval_phone(phone_raw):

    phone_digits = []
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

    for char in phone_raw:
        if char in numbers:
            phone_digits.append(char)
    if phone_digits[0] != 1:
        phone_digits.insert(0, "1")

    if len(phone_digits) == 11:
        phone_digits.insert(0, "+")
        recepient_phone = phone_digits.join()
        response = recepient_phone
    else:
        response = "not a valid phone number.  try again!"

def send_sms(response):
    """sends text to requested number."""

    if response[0] != "+":
        confirm_string = "not a valid phone number. try again!"
        return render_template("confirm_sms.html", response=confirm_string)
    else:
        sms_string = markov.get_quote("buffy_speechify.txt")
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            to=recepient_phone,
            from_=CALLER_ID,
            body=sms_string,
            # media_url="https://climacons.herokuapp.com/clear.png",
        )
        confirm_string = """confirmed!  sent '%s' to %s """ % (sms_string, response)

        return confirm_string