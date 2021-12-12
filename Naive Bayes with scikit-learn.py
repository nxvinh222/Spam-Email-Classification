import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_score, f1_score, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Prepare data
DATA_JSON_FILE = 'Data/email-text-data-no-html.json'
data = pd.read_json(DATA_JSON_FILE)
data.sort_index(inplace=True)

vectorizer = CountVectorizer(stop_words='english')
all_features = vectorizer.fit_transform(data.MESSAGE)

X_train, X_test, y_train, y_test = train_test_split(all_features, data.CATEGORY, test_size=0.3, random_state=88)

# Prepare and train model
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Evaluate model
print(accuracy_score(y_test, classifier.predict(X_test)))
print(recall_score(y_test, classifier.predict(X_test)))
print(precision_score(y_test, classifier.predict(X_test)))
print(f1_score(y_test, classifier.predict(X_test)))

# Save vectorizer and model to file in the current working directory
vectorizer_file = "count_vectorizer.pkl"
classifier_file = "naive_bayes.pkl"
joblib.dump(vectorizer, vectorizer_file)
joblib.dump(classifier, classifier_file)
