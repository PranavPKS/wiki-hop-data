from flask import Flask,request
from allen import coref, ner


app = Flask(__name__)
p1 = coref()
p2 = ner()

@app.route("/", methods=['GET','POST'])
def hello():
    para = request.json['para']
    return p2.wikify(p1.resolve(para))

if __name__ == '__main__':
    app.run(debug=True)
