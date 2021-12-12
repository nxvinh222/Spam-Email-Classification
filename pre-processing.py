from os import walk
from os.path import join

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from bs4 import BeautifulSoup

EXAMPLE_FILE = 'Data/SpamData/01_Processing/practice_email.txt'

SPAM_1_PATH = 'Data/SpamData/01_Processing/spam_assassin_corpus/spam_1'
SPAM_2_PATH = 'Data/SpamData/01_Processing/spam_assassin_corpus/spam_2'
EASY_NONSPAM_1_PATH = 'Data/SpamData/01_Processing/spam_assassin_corpus/easy_ham_1'
EASY_NONSPAM_2_PATH = 'Data/SpamData/01_Processing/spam_assassin_corpus/easy_ham_2'

SPAM_CAT = 1
HAM_CAT = 0
VOCAB_SIZE = 2500

# DATA_JSON_FILE = 'Data/SpamData/01_Processing/email-text-data2.json'
DATA_JSON_FILE = 'Data/email-text-data.json'
DATA_JSON_NO_HTML_FILE = 'Data/email-text-data-no-html.json'
WORD_ID_FILE = 'Data/SpamData/01_Processing/word-by-id.csv'

TRAINING_DATA_FILE = 'Data/SpamData/02_Training/train-data.txt'
TEST_DATA_FILE = 'Data/SpamData/02_Training/test-data.txt'

# EMAIL BODY EXTRACTOR


def email_body_generator(path):
    for root, dirnames, filenames in walk(path):
        for filename in filenames:

            filepath = join(root, filename)
            stream = open(filepath, encoding='latin-1')

            is_body = False
            lines = []

            for line in stream:
                if is_body:
                    lines.append(line)
                elif line == '\n':
                    is_body = True

            stream.close()

            email_body = '\n'.join(lines)
            # Remove html
            soup = BeautifulSoup(email_body, 'html.parser')
            email_body = soup.get_text()
            yield filename, email_body


def df_from_directory(path, classification):
    rows = []
    row_names = []

    for filename, email_body in email_body_generator(path):
        rows.append({'MESSAGE': email_body, 'CATEGORY': classification})
        row_names.append(filename)

    return pd.DataFrame(rows, index=row_names)


spam_emails = df_from_directory(SPAM_1_PATH, SPAM_CAT)
spam_emails = spam_emails.append(df_from_directory(SPAM_2_PATH, SPAM_CAT))
ham_emails = df_from_directory(EASY_NONSPAM_1_PATH, HAM_CAT)
ham_emails = ham_emails.append(df_from_directory(EASY_NONSPAM_2_PATH, HAM_CAT))

data = pd.concat([spam_emails, ham_emails])
print('Shape of data is:', data.shape)

# DATA CLEANING
data.drop(['cmds'], inplace=True)

# ADD DOCUMENT IDS TO TRACK EMAILS IN DATASET
document_ids = range(0, len(data.index))
data['DOC_ID'] = document_ids
data['FILE_NAME'] = data.index
data.set_index('DOC_ID', inplace=True)

# SAVE TO JSON
# data.to_json(DATA_JSON_FILE)
data.to_json(DATA_JSON_NO_HTML_FILE)
print('Pre-Processing completed!')
