from flask import Flask,request,jsonify

import mysql.connector


app=Flask(__name__)


try:
    connect=mysql.connector.connect(host='localhost',username='root',passwd='123wer')
    if connect.is_connected():
        print("MYSQL DB Connected")
except  Exception as e:
    print(e)

cursor=connect.cursor()

cursor.execute("create Database if not exists learnone")

cursor.execute("create table if not exists learnone.employee(name varchar(30),number int)")

@app.route('/insert',methods=['POST','GET'])
def insert():
    if request.method == 'POST':
        name=request.json['name']
        number=request.json['number']
        cursor.execute("insert into learnone.employee values(%s,%s)",(name,number))
        connect.commit()
        return jsonify({'status':'successfully inserted'})
@app.route('/update',methods=['POST'])
def update():
    if request.method == 'POST':
        get_name=request.json['name']
        cursor.execute("update learnone.employee set name='kri' where name=%s",(get_name,))
        connect.commit()
        return jsonify({'status':'successfully updated'})
@app.route('/delete',methods=['POST'])
def delete():
    if request.method=='POST':
        get_name=request.json['name']
        cursor.execute("delete from learnone.employee where name=%s",(get_name,))
        connect.commit()
        return jsonify({'status':'successfully deleted'})
@app.route('/fetch',methods=['POST'])
def fetch():
    if request.method=="POST":
        cursor.execute("select * from learnone.employee")
        l=[]
        for i in cursor.fetchall():
            l.append({'name':i[0],'number':i[1]})
        return jsonify(l)
if __name__=='__main__':
    app.run(debug=True)