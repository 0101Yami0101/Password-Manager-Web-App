import json
import random
# Generate random key for suggestion 
# Opening JSON file
f = open('website/static/words.json')
data = json.load(f)
f.close()
  


def Generate_key():
    list_of_words = []
    SECRET = ""
    for _ in range(12):
        word = random.choice(data)
        if word in list_of_words:
            sub_word = random.choice(data)
            list_of_words.append(sub_word)
            SECRET += word + ""
        else:
            list_of_words.append(word)
            SECRET += word + " "

    return SECRET





