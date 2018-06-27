from flask import Flask, render_template, request
import MySQLdb
import socket

app = Flask(__name__)

@app.route('/add', methods=['POST','GET'])
def addpage():
  if request.method == 'POST':
     post_data =  [request.form.get('sig'), request.form.get('name'), request.form.get('type'), request.form.get('description')]
     db = MySQLdb.connect(host="***",
                     user="***",
                     passwd="***",
                     db="***")
     cur = db.cursor()
     print(post_data)
     command = "INSERT INTO signals(sig,name,type,description) VALUES ('%s','%s','%s','%s')" % (post_data[0],post_data[1],post_data[2],post_da$
     try:
       cur.execute(command)
       db.commit()
     except:
       db.rollback()
     db.close
  return render_template('add.html')

@app.route('/', methods = ['POST', 'GET'])
def index():
  port = ***
  ip = '***'
  items = getRemoteButtons()
  if request.method == 'POST':
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((ip,port))
     form = request.form
     for key, val in form.items():
       sendsignal = val
       s.send(val.encode('utf-8'))
  return render_template('index.html', marks=items)

def getRemoteButtons():
   db = MySQLdb.connect(host="***",
                     user="***",
                     passwd="***",
                     db="***")
   cur = db.cursor()
   cur.execute("SELECT * FROM signals")
   items = cur.fetchall()
   db.close
   for item in items:
     print(item)
   return items

if __name__=='__main__':
  app.run(debug=True,host='0.0.0.0')



