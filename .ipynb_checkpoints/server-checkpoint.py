from flask import Flask,request
from get_and_predURL import init,chk_is_elsagate

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello Word</h1>"

@app.route("/api", methods=['POST'])
def api():
    if 'url' in request.form.keys():
        url = request.form['url']
        print(url)
        if chk_is_elsagate(url):
            print('is elsa gate')
            return '1'
        else:
            print('not elsa gate')
            return '0'
    else:
        return 'err'

if __name__ == "__main__":
    init()
    app.run(debug=True)

