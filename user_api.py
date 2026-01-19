from flask import Flask, request, jsonify
import json
import yaml
import os

app = Flask(__name__)

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    # FIXED: Added authentication check and parameterized query
    if not request.headers.get('Authorization'):
        return jsonify({"error": "Unauthorized"}), 401
    
    # Use parameterized query instead of f-string
    user = db.query("SELECT * FROM users WHERE id = %s", (user_id,))
    return jsonify(user)

@app.route('/api/user/update', methods=['POST'])
def update_user():
    # FIXED: Whitelist allowed fields to prevent mass assignment
    if not request.headers.get('Authorization'):
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    user_id = data.get('id')
    
    # Only allow specific fields to be updated
    allowed_fields = ['name', 'email', 'phone']
    safe_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    User.query.filter_by(id=user_id).update(safe_data)
    db.commit()
    return jsonify({"status": "updated"})

@app.route('/api/load')
def load_data():
    # FIXED: Use JSON instead of pickle
    if not request.headers.get('Authorization'):
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.args.get('data')
    obj = json.loads(data)  # Safe JSON parsing
    return jsonify(obj)

@app.route('/api/config')
def load_config():
    # FIXED: Use safe_load instead of load
    if not request.headers.get('Authorization'):
        return jsonify({"error": "Unauthorized"}), 401
        
    config_data = request.args.get('yaml')
    config = yaml.safe_load(config_data)  # Safe YAML parsing
    return jsonify(config)

# REMOVED: Dangerous eval endpoint completely removed
