from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# Configure MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/employee_db'
mongo = PyMongo(app)

# Get MongoDB collection
employees_collection = mongo.db.employees

# Get all employees from MongoDB
@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = list(employees_collection.find())
    
    # Convert ObjectId to string for serialization
    for employee in employees:
        employee['_id'] = str(employee['_id'])
    
    return jsonify({'employees': employees})

# Get a specific employee from MongoDB
@app.route('/api/employees/<string:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = employees_collection.find_one({'_id': ObjectId(employee_id)})
    
    # Convert ObjectId to string for serialization
    if employee:
        employee['_id'] = str(employee['_id'])
        return jsonify({'employee': employee})
    else:
        return jsonify({'message': 'Employee not found'}), 404

# Create a new employee in MongoDB
@app.route('/api/employees', methods=['POST'])
def create_employee():
    new_employee = request.json
    result = employees_collection.insert_one(new_employee)
    new_employee['_id'] = str(result.inserted_id)
    return jsonify({'message': 'Employee created successfully', 'employee': new_employee}), 201

# Update an employee in MongoDB
@app.route('/api/employees/<string:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    filter_criteria = {'_id': ObjectId(employee_id)}
    updated_employee = request.json
    employees_collection.update_one(filter_criteria, {'$set': updated_employee})
    return jsonify({'message': 'Employee updated successfully', 'employee': updated_employee})

# Delete an employee from MongoDB
@app.route('/api/employees/<string:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    result = employees_collection.delete_one({'_id': ObjectId(employee_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'Employee deleted successfully'})
    else:
        return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)