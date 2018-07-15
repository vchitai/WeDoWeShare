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
@app.route('/api/suggest', methods = ['POST'])
def suggest():
    vector = request.form['vector']
    vector = json.loads(vector)
    a = np.array(vector)
    a = wrapper.suggest(a)
    print(a)
    res = np.array_str(a)
    res = json.dumps(res)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
