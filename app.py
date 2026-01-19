from flask import Flask, request
import os
import subprocess

app = Flask(__name__)

@app.route('/search')
def search():
    # SQL Injection vulnerability
    query = request.args.get('q')
    result = db.execute(f"SELECT * FROM users WHERE name = '{query}'")
    return result

@app.route('/run')
def run_command():
    # Command Injection vulnerability
    cmd = request.args.get('cmd')
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/read')
def read_file():
    # Path Traversal vulnerability
    filename = request.args.get('file')
    with open(f'/data/{filename}', 'r') as f:
        return f.read()

if __name__ == '__main__':
    app.run()
