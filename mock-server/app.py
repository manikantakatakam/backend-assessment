from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'customers.json')

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

@app.route('/api/customers', methods=['GET'])
def get_customers():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    data = load_data()
    total = len(data)
    
    start = (page - 1) * limit
    end = start + limit
    
    paginated_data = data[start:end]
    
    return jsonify({
        "data": paginated_data,
        "total": total,
        "page": page,
        "limit": limit
    })

@app.route('/api/customers/<id>', methods=['GET'])
def get_customer(id):
    data = load_data()
    customer = next((c for c in data if c['customer_id'] == id), None)
    
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
