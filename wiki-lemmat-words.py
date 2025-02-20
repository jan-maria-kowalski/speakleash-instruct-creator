import os 
from utils.functions import download_file
from speakleash import Speakleash
import random
import json
import spacy

nlp = spacy.load("pl_core_news_md")

source_name = "speakleash_plwiki_lemmat_words"
source_url = "https://speakleash.org/"
source_description = "Instrukcje powstały dzięki ekstrakcji słów z polskiej wersji Wikipedii i przetworzenia ich za pomocą pakietu Spacy."
script_name = os.path.basename(__file__)

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
output_dir = os.path.join(base_dir, "output")
replicate_to = os.path.join(base_dir, "datasets")

sl = Speakleash(replicate_to)
counter = 0
wiki = sl.get("plwiki").data
instructions = []
words = {}

for txt in wiki:
    doc = nlp(txt)
    print("Instructions: " + str(len(instructions)))
    for token in doc:
        if not token.is_stop and not token.is_punct and not token.is_digit and token.is_oov == False:
            word = token.text.strip()
            lemma = token.lemma_.strip()
            if word.upper() != lemma.upper():
                if word not in words:
                    words[word] = lemma
                    counter += 1
                    instructions.append({"instruct": "Podaj formę podstawową (lemat) dla słowa: " + word, "input" : "", "output" : "Forma podstawowa dla słowa " + word + " to: " + lemma, "source_name" : source_name, "source_url" : source_url, "source_description" : source_description, "script_name" : script_name})

    if len(instructions) > 100000:
        break

random.shuffle(instructions)
with open(os.path.join(output_dir, "wiki-lemmat-words.json"), "w", encoding='utf-8') as f:
    json.dump(instructions, f, indent=4, ensure_ascii=False)
print("Instructions: " + str(len(instructions)))


