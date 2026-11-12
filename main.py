from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Folder aur File setup
DATA_FOLDER = "saved_accounts"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

ACCOUNTS_FILE = os.path.join(DATA_FOLDER, "accounts.txt")

@app.route('/upload_batch', methods=['POST'])
def upload_batch():
    try:
        data = request.get_json()
        server = data.get('server', 'IND')
        accounts = data.get('accounts', []) # List of "uid:pass"
        
        if not accounts:
            return jsonify({"status": "error", "message": "Koi account nahi mila!"}), 400
        
        # File me save karna
        with open(ACCOUNTS_FILE, "a") as f:
            for acc in accounts:
                f.write(f"{acc}:{server}\n")
                
        # Total counts nikalna
        with open(ACCOUNTS_FILE, "r") as f:
            total_lines = len(f.readlines())
            
        return jsonify({
            "status": "success", 
            "message": f"Successfully added {len(accounts)} accounts!",
            "total_saved": total_lines
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get_stats', methods=['GET'])
def get_stats():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            count = len(f.readlines())
        return jsonify({"status": "success", "total_accounts": count}), 200
    return jsonify({"status": "success", "total_accounts": 0}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
