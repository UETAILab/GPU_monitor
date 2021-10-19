from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/sysreport', methods=['POST'])
def add_message():
    content = json.loads(request.data)
    print("REQ", content)
    return content

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)