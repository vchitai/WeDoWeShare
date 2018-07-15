from flask import Flask, request
import embedding
import json
from embedding import *

app = Flask(__name__)
wrapper = embedding.EmbeddingWrapper('./data/res.csv', './data/mentor.csv')
wrapper.train_all(1)

@app.route('/')

def hello():
    return 'hello'
@app.route('/api/train_batch', methods = ['POST'])
def train_batch():
    new_batch = request.form['new_batch']
    new_label = request.form['new_label']
    new_batch = json.loads(new_batch)
    new_label = json.loads(new_label)
    new_batch = np.array(new_batch)
    new_label = np.array(new_label)

    wrapper.train_new_batch(new_batch, new_label) 
    return json.dumps('ok')

@app.route('/api/suggest', methods = ['POST'])
def suggest():
    vector = request.json['vector']
    print(vector)
    #vector = json.loads(vector)
    a = np.array(vector)
    a = wrapper.suggest(a)
    print(a)
    res = np.array_str(a)
    res = json.dumps(res)
    return res



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)


