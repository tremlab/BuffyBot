# import markov


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


def get_message():
    """TODO  build dynamic message generation here
    """
    return "   ... .. .  ...  :|          ......."