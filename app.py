from flask import Flask, render_template, request, jsonify
import json
import DB

db_connect = DB.DBConnect()

app = Flask(__name__)

@app.route('/')
def index():
    return """API"""

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     # print(request.form.get("num1"))
#     num1 = float(request.form.get('num1'))
#     num2 = float(request.form.get('num2'))
#     print(num1)
#
#     return json.dumps({"out":"10"})


@app.route('/register', methods=['POST'])
def register():
    user_name = request.form.get('name')
    print(user_name)
    db_connect.register_user(user_name)
    # return jsonify({'user_id': user_id})
    return json.dumps({"out":True})



if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as ex:
        print(ex)
    finally:
        db_connect.close()
