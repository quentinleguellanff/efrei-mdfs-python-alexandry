from flask import Flask,jsonify,request
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all_books():
    with open('books.json') as json_file:
        data = json.load(json_file)  
        return jsonify(data)
 
@app.route("/api/v1/resources/books/new", methods=["POST"])
def post_book():
    isOk = True
    data = request.get_json()
    with open('books.json') as json_file:
        localData = json.load(json_file)
        for index in range(len(localData['books'])):  
            if localData['books'][index]['title'] == data['title']:
                return "Error, there is already a book with this name !"
    if(isOk):
        localData['books'].append(data)
    with open('books.json','w') as json_file:
        json.dump(localData,json_file,indent=4)
    
    return jsonify(data)
    
@app.route("/api/v1/resources/books/update", methods=["PUT"])
def update_book():
    data = request.get_json()
    updated = False
    with open('books.json') as json_file:
        localData = json.load(json_file)
        for index in range(len(localData['books'])):  
            if localData['books'][index]['title'] == data['title']:
                localData['books'][index] = data
                updated = True
    if not updated:
        localData['books'].append(data)
    with open('books.json','w') as json_file:
        json.dump(localData,json_file,indent=4)
    
    return jsonify(data)

@app.route("/api/v1/resources/books/delete", methods=["DELETE"])
def delete_books():
    data = request.get_json()
    deleted = False
    with open('books.json') as json_file:
        localData = json.load(json_file)
        for index in range(len(localData['books'])):  
            if localData['books'][index]['title'] == data['title']:
                localData['books'].pop(index)
                with open('books.json','w') as json_file:
                    json.dump(localData,json_file,indent=4)
                return jsonify(localData)
    if not deleted:
        return "the book you want to delete does not exist..."