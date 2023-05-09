import re
import json
import math
from flask_cors import CORS
from flask import request, Flask, jsonify, render_template

input_data = "test_data.json"

with open(input_data, "r") as file:
    content = json.loads(file.read())

def clean_str(text):
    text = (text.encode('ascii', 'ignore')).decode("utf-8")
    text = re.sub("&.*?;", "", text)
    text = re.sub(">", "", text)
    text = re.sub("[\]\|\[\@\,\$\%\*\&\\\(\)\":]", "", text)
    text = re.sub("-", " ", text)
    text = re.sub("\.+", "", text)
    text = re.sub("^\s+", "", text)
    text = text.lower()
    return text

df_data = {}
tf_data = {}
idf_data = {}

for data in content:
    tf = {}
    clean_content = clean_str(data['content'])
    list_word = clean_content.split(" ")

    for word in list_word:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1

        if word in df_data:
            df_data[word] += 1
        else:
            df_data[word] = 1

    tf_data[data['id']] = tf

for x in df_data:
    idf_data[x] = 1 + math.log10(len(tf_data) / df_data[x])

idf = {}

for x in df_data:
    idf[x] = 1 + math.log10(len(tf_data) / df_data[x])

tf_idf = {}

for word in df_data:
    list_doc = []
    for data in content:
        tf_value = 0

        if word in tf_data[data['id']]:
            tf_value = tf_data[data['id']][word]

        weight = tf_value * idf[word]

        doc = {
            'id': data['id'],
            'username': data['username'],
            'content': data['content'],
            'score': weight
        }

        if doc['score'] != 0:
            if doc not in list_doc:
                list_doc.append(doc)

    tf_idf[word] = list_doc

def search(query):
    if not query:
        return []

    query = clean_str(query)
    query_words = query.split(" ")
    search_results = {}

    for word in query_words:
        if word in tf_idf:
            for doc in tf_idf[word]:
                if doc['id'] not in search_results:
                    search_results[doc['id']] = doc
                else:
                    search_results[doc['id']]['score'] += doc['score']

    ranked_results = sorted(search_results.values(), key=lambda x: x['score'], reverse=True)
    print(ranked_results)
    return ranked_results

app = Flask(__name__)
CORS(app)  # This line enables CORS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_query():
    query = request.args.get('query', '')
    results = search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=8000, debug=True)

