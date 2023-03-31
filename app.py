from flask import Flask, render_template, request
import json
app = Flask(__name__)

@app.route('/')
def index():
    return """API"""

@app.route('/calculate', methods=['POST'])
def calculate():
    # print(request.form.get("num1"))
    num1 = float(request.form.get('num1'))
    num2 = float(request.form.get('num2'))


    return json.dumps({"out":"10"})

if __name__ == '__main__':
    app.run(debug=True)
