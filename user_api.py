from flask import Flask, request, jsonify
import pickle
import yaml
import os

app = Flask(__name__)

@app.route('/api/user/<user_id>')
def get_user(user_id):
    # IDOR - No authorization check
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    return jsonify(user)

@app.route('/api/user/update', methods=['POST'])
def update_user():
    # Mass Assignment vulnerability
    data = request.json
    user_id = data.get('id')
    User.query.filter_by(id=user_id).update(data)
    db.commit()
    return jsonify({"status": "updated"})

@app.route('/api/load')
def load_data():
    # Insecure Deserialization
    data = request.args.get('data')
    obj = pickle.loads(data.encode())
    return str(obj)

@app.route('/api/config')
def load_config():
    # YAML Deserialization vulnerability  
    config_data = request.args.get('yaml')
    config = yaml.load(config_data)
    return jsonify(config)

@app.route('/api/eval')
def evaluate():
    # Code Injection
    expr = request.args.get('expr')
    result = eval(expr)
    return str(result)
