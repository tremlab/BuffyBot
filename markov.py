from random import choice


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    text_input = open(file_path).read()

    return text_input


def make_chains(text_string, key_word_count=2):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:
        >>>make_chains("Would you could you in", 3)
        {('Would', 'you', 'could'): ['you', 'you', 'you', 'you'],
        ('you', 'could', 'you'): ['in', 'with','in', 'with']
        }


        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}
    words = text_string.split()
    # loop through words to create tuples as keys for chains dictionary

    for index in range(len(words) - key_word_count):
        # if tuple key found append this value
        key_values = []
        for i in range(key_word_count):
            key_values.append(words[index + i])
        key_values = tuple(key_values)

        if key_values in chains:
            chains[key_values].append(words[index + key_word_count])
        # if tuple not found, create key and add value
        else:
            chains[key_values] = [words[index + key_word_count]]

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    #list of key tuples
    key_choices = chains.keys()

    #randomly selects one key tuple
    while True:
        key = choice(key_choices)
        if is_capitalized(key):
            break

    #initializes text list with first key tuple
    text = []

    for index in range(len(key)):
        text.append(key[index])

    while True:
        if key not in chains:
            break
        else:
            #picking a viable next word from value list for given key
            new_word = choice(chains[key])
            if is_ending_punctuation(new_word):
                text.append(new_word)
                break

            # append next word to text list
            text.append(new_word)

            #advance key for next iteration
            key_as_list = list(key)
            del key_as_list[0]
            key_as_list.append(new_word)
            key = tuple(key_as_list)

    buffy_quote = " ".join(text)

    return buffy_quote

# def eval_text(text, chains):
#     """evaluates text for suitability to Twitter, then tweets it.
#     """

#     while len(text) >= 140:
#         text = make_text(chains)

#     return text


def is_capitalized(key):
    if key[0][0].isupper():
        return True
    else:
        return False


def is_ending_punctuation(word):
        if word[-1] in ".!?":
            return True
        else:
            return False


def get_quote(file_name):
    """takes in filename, calls for file to be opened,
    parsed into chains, and then returns a resulting quote.
    """
    text_from_file = open_and_read_file(file_name)
    chains = make_chains(text_from_file, 2)
    markov_text = make_text(chains)

    while len(markov_text) > 139:
        markov_text = make_text(chains)

    return markov_text



################################################################################
if __name__ == "__main__":


    file_name = "buffy_speechify.txt"    

    print get_quote(file_name)
