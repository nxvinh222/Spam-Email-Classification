from flask import Flask, jsonify, request # import objects from the Flask model
import joblib
app = Flask(__name__) # define app using Flask

# Load vectorizer and model from file
vectorizer_file = "count_vectorizer.pkl"
classifier_file = "naive_bayes.pkl"
vectorizer = joblib.load(vectorizer_file)
classifier = joblib.load(classifier_file)

def spam_or_not(email):
    doc_term_matrix = vectorizer.transform(email)
    if classifier.predict(doc_term_matrix)[0] == 1:
        return "spam"
    else:
        return "ham"

@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})
    
@app.route('/', methods=['POST'])
def addOne():
	email = [request.json['email']]
	return jsonify({'result' : spam_or_not(email)})


if __name__ == '__main__':
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode
