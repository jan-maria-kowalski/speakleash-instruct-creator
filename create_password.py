import os
import random
import json
import string

source_name = "password_creator"
source_url = "https://speakleash.org/"
source_description = "Instrukcje zostały wygenerowane automatycznie"
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")

def generate_syllable_password(length=8, num_digits=2, num_special_chars=2):

    syllables = ['se', 'a', 'gnie', 'szka', 'ba', 'ra', 'ma', 'ta', 'na', 'la',
                 'ko', 'mu', 'ni', 'te', 'ru', 'so', 'wa', 'pe', 'ci', 'da',
                 'lo', 'mi', 'ne', 'fu', 'gi', 'he', 'je', 'ke', 'le', 'ze',
                 'bi', 'di', 'fi', 'gi', 'hi', 'ki', 'li', 'mi', 'pi', 'ti']
    
    password = ''

    while len(password) < length:
        password += random.choice(syllables)

    password = password[:length]

    for c in password:
        i = random.randint(0, 100)
        if i > 50:
            password = password.replace(c, c.upper(), 1)
        pass      

    password += ''.join(random.choices(string.digits, k=num_digits))
    password += ''.join(random.choices(string.punctuation, k=num_special_chars))

    return password

def random_instruct(mode):

    if mode == "sylabic":
        instruct = [
            "Stwórz hasło łatwe do zapamiętania składające się ",
            "Wygeneruj hasło łatwe do wymówienia składające się ",
            "Stwórz hasło proste do zapamiętania składające się ",
            "Stwórz hasło (łatwe do zapamiętania) składające się z",
            "Stwórz hasło, które jest łatwe do zapamiętania, wygenerowane z "
        ]
        return random.choice(instruct)
    else:
        instruct = [
            "Stwórz hasło składające się ",
            "Wygeneruj hasło składające się ",
            "Twórz hasło składające się ",
            "Wygeneruj losowe hasło składające się z ",
            "Stwórz losowe hasło, które jest wygenerowane z "
        ]
        return random.choice(instruct)
        


instructions = []

chars = [8, 10, 12, 14, 16, 18, 20]
digits = [2, 3, 4, 5]
special_chars = [2, 3, 4, 5]
mode = ["sylabic", "random"]


for i in range(10000):
    
    random.shuffle(chars)
    random.shuffle(digits)
    random.shuffle(special_chars)
    random.shuffle(mode)

    output = ""
    instruct = random_instruct(mode[0]) + str(chars[0]) + " znaków, " + str(digits[0]) + " cyfr i " + str(special_chars[0]) + " znaków specjalnych."
    

    if mode[0] == "sylabic":
        output = generate_syllable_password(chars[0], digits[0], special_chars[0])
    else:
        output = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=chars[0])) + ''.join(random.choices(string.digits, k=digits[0])) + ''.join(random.choices(string.punctuation, k=special_chars[0]))

    instructions.append({"instruct": instruct, "input" : "", "output" : output, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})

random.shuffle(instructions)

random.shuffle(instructions)
with open(os.path.join(output_dir, "create_password.json"), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))
