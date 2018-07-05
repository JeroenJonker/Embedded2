from flask import Flask,redirect,url_for, render_template, request
import MySQLdb
import socket

app = Flask(__name__)

@app.route('/add', methods=['POST','GET'])
def addpage():
  if request.method == 'POST':
     command = "INSERT INTO signals(sig,description,name,type) VALUES ('%s','%s','%s','%s')" % (request.form.get('sig'),request.form.get('description'),request.form.get('name'),request.form.get('type'))
     updateDatabaseWithCommand(command)
     return redirect('/')
  return render_template('add.html',header="Voeg knop toe", readonly="")

@app.route('/remove',methods=['POST','GET'])
def removepage():
  if request.method == 'POST':
    for key, val in request.form.items():
      return redirect(url_for('remove', sig=key))
  return render_template('index.html',header="Verwijder een knop",marks=getRemoteButtons())

@app.route('/edit', methods=['POST','GET'])
def editpage():
  if request.method == 'POST':
    for key, val in request.form.items():
      return redirect(url_for('edit', sig=key))
  return render_template('index.html', header="Wijzig een knop", marks=getRemoteButtons())

@app.route('/edit/<sig>',methods=['POST','GET'])
def edit(sig):
  if request.method == 'POST':
    command = "UPDATE signals SET sig='%s', name='%s', description='%s', type='%s' WHERE sig='%s'" % (request.form.get('sig'),request.form.get('name'),request.form.get('description'),request.form.get('type'),sig)
    updateDatabaseWithCommand(command) 
    return redirect('/')
  db, cur = getDatabaseAndCursor()
  command = "SELECT sig, description, name, type FROM signals WHERE sig='%s'" % (sig)
  cur.execute(command)
  db.close
  item = cur.fetchall()
  print(item)
  return render_template('add.html',header="Wijzigen knop", readonly="",obj=item[0])

@app.route('/remove/<sig>',methods=['POST','GET'])
def remove(sig):
  if request.method == 'POST':
    command = "DELETE FROM signals WHERE sig='%s' AND name='%s' AND description='%s' AND type='%s'" % (request.form.get('sig'),request.form.get('name'),request.form.get('description'),request.form.get('type'))
    updateDatabaseWithCommand(command) 
    return redirect('/')
  db, cur = getDatabaseAndCursor()
  command = "SELECT sig, description, name, type FROM signals WHERE sig='%s'" % (sig)
  cur.execute(command)
  db.close
  item = cur.fetchall()
  print(item)
  return render_template('add.html',header="Verwijder knop", readonly='readonly', obj=item[0])

@app.route('/', methods = ['POST', 'GET'])
def index():
  port = **** #set port
  ip = '***'  #set IP adress
  items = getRemoteButtons()
  if request.method == 'POST':
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.connect((ip,port))
     form = request.form
     for key, val in form.items():
       sendsignal = val
       s.send(val.encode('utf-8'))
  return render_template('index.html',header="Kies een knop", marks=items)

def getRemoteButtons():
   db = MySQLdb.connect(host="localhost",
                     user="aap",
                     passwd="aap",
                     db="remotebuttons")
   cur = db.cursor()
   cur.execute("SELECT * FROM signals")
   items = cur.fetchall()
   db.close
   return items

def updateDatabaseWithCommand(command):
   db, cur = getDatabaseAndCursor()
   try:
     cur.execute(command)
     db.commit()
   except:
     db.rollback()
   db.close 

def getDatabaseAndCursor():
  db = MySQLdb.connect(host="localhost",
                       user="aap",
                       passwd="aap",
                       db="remotebuttons")
  return db, db.cursor()

if __name__=='__main__':
  app.run(debug=True,host='0.0.0.0')

