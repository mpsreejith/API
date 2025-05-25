from flask import Flask,request,jsonify
import pymongo

app=Flask(__name__)

connection = (
    pymongo.MongoClient("mongodb+srv://sreejithmp007:anandam007@cluster0.x9rrkbe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"))

database=connection['APItask']

collection=database['APIcollections']

@app.route('/insert/mongoAPI',methods=['POST'])
def insert():
    if request.method=="POST":
        name=request.json['name']
        number=request.json['number']
        collection.insert_one({'name':name,'number':number})
        return jsonify({'name':name,'number':number})

if __name__=='__main__':
    app.run(debug=True)