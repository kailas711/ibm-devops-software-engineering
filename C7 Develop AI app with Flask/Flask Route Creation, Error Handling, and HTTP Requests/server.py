import uuid
from flask import Flask, make_response, request

# Create the Flask application instance
app = Flask(__name__)

# Sample data structure with UUIDs
data = [
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "first_name": "John",
        "last_name": "Doe",
        "age": 30
    },
    {
        "id": "98765432-b12c-34d5-e678-901234567890",
        "first_name": "Jane",
        "last_name": "Smith",
        "age": 25
    }
]

# Define global 404 error handler for undefined endpoints
@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"}, 404

# Define the root route
@app.route("/")
def hello_world():
    return {"message": "Hello World"}

# Define the no_content route
@app.route("/no_content")
def no_content():
    return {"message": "No content found"}, 404

# Define the index_explicit route using make_response
@app.route("/exp")
def index_explicit():
    res = make_response({"message": "Hello World"})
    res.status_code = 200
    return res

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    if "q" not in request.args:
        return {"message": "Invalid input parameter"}, 400

    q = request.args.get("q")

    if not q or q.strip() == "" or q.isdigit():
        return {"message": "Invalid input parameter"}, 422

    for person in data:
        if person.get("first_name").lower() == q.lower():
            return person, 200

    return {"message": "Person not found"}, 404

@app.route("/count")
def count():
    try:
        return {"count": len(data)}, 200
    except NameError:
        return {"message": "Data not found"}, 500

# Define the find_by_uuid GET route
@app.route("/person/<uuid:id>", methods=["GET"])
def find_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            return person, 200

    return {"message": "person not found"}, 404

# Define the delete_by_uuid DELETE route
@app.route("/person/<uuid:id>", methods=["DELETE"])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message": f"Person with ID {id} deleted successfully"}, 200

    return {"message": "person not found"}, 404

# Define the add_by_uuid POST route
@app.route("/person", methods=["POST"])
def add_by_uuid():
    person_data = request.get_json(silent=True)

    if not person_data:
        return {"message": "Invalid input parameter"}, 422

    if "id" not in person_data:
        person_data["id"] = str(uuid.uuid4())

    data.append(person_data)

    return {"id": person_data["id"]}, 200

# Run the server when the script is executed
if __name__ == "__main__":
    app.run(debug=True)