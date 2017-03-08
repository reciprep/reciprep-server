from flask import Flask
app = Flask(__name__)

@app.route('/api')
def hello_world():
    return 'Hello World ReciPrep'

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    app.run(debug=True)
