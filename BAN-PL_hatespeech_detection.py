import os
import pandas as pd
import json
import random

from utils.functions import download_file
from zipfile import ZipFile


SOURCE_NAME = os.path.basename(__file__).replace(".py", "") + "BAN-PL.csv"
SOURCE_URL = "https://github.com/ZILiAT-NASK/BAN-PL/tree/main/data"
SOURCE_DESCRIPTION = "Instrukcje zawierające tekst z potencjalnie szkodliwymi treściami \
                    oraz klasyfikację tego tekstu: zawiera/nie zawiera szkodliwych treści"
SCRIPT_NAME = os.path.basename(__file__)
FILE = "BAN-PL_1.zip"
DATA_DIR = "data"
OUTPUT_DIR = "output"
PASSWORD = "BAN-PL_1"
MEMBER_FILE = 'BAN-PL.csv'


def create_dirs() -> tuple:
    """
    Create storage directories for both downloaded dataset and created JSON instructions file.
    """
    # Get the path to the currently executing python script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define directories name for downloaded and output files
    data_dir = os.path.join(base_dir, DATA_DIR)
    output_dir = os.path.join(base_dir, OUTPUT_DIR)

    # Create directory for downloading data from server / link
    os.makedirs(data_dir, exist_ok=True)

    # Create directory (if it does not exist yet) for created instructions json files
    os.makedirs(output_dir, exist_ok=True)
    return data_dir, output_dir


def _convert_github_url(git_url: str) -> str:
    """
    Converts provided GitHub url to downloadable url for raw format files. If is not from GitHub or already
    represents raw file, it returns unchanged link.

    :param git_url: Link to the GitHub repository file
    :return: Link to the GitHub repository in raw format, if conditions are met.
    """
    if 'github' in git_url and '/tree/' in git_url and 'raw' not in git_url:
        return git_url.replace('/tree/', '/raw/', 1)
    return git_url


def download_and_extract(download_url: str, file: str, password: str) -> tuple:
    """
    Download dataset file, return its file path and corresponding JSON file path.

    :param download_url: Url address of the dataset file.
    :param file: The name of the dataset file to be downloaded.
    :param password: The password for the encrypted file.
    :return: A tuple containing path to downloaded file and output JSON file.
    """
    download_url = _convert_github_url(download_url)
    file_path = download_file(f"{download_url}/{file}", DATA_DIR, file)
    with ZipFile(file_path, mode='r') as zf:
        zf.extract(path=DATA_DIR, member=MEMBER_FILE, pwd=bytes(password, 'utf-8'))
    updated_file_path = f'{DATA_DIR}/{MEMBER_FILE}'
    json_path = os.path.join(OUTPUT_DIR, 'BAN-PL.json')
    return updated_file_path, json_path


def create_instruction(file_path, json_path):
    instr_list = [
        "Oceń, czy te treści są szkodliwe",
        "Określ, czy ten tekst jest nieodpowiedni",
        "Czy dostęp do tego tekstu powinien być w jakiś sposób ograniczony?",
        "Czy ten tekst zawiera drastyczne lub nieodpowiednie treści?",
        "Czy ten tekst może zawierać szkodliwe treści?",
        "Czy ten tekst jest nieodpowiedni dla dzieci i osób wrażliwych?"
    ]
    instruction = f"{random.choice(instr_list)}"
    instructions = []
    data = pd.read_csv(file_path, usecols=['Text', 'Class'])

    for index, row in data.iterrows():
        source = row['Text']
        if row['Class'] == 1:
            target = "Tak"
        else:
            target = "Nie"
        instructions.append({"instruct": instruction, "input": source, "output": target})
    random.shuffle(instructions)
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(instructions, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    _data_dir, _output_dir = create_dirs()
    _file_path, _json_path = download_and_extract(SOURCE_URL, FILE, PASSWORD)
    create_instruction(_file_path, _json_path)
