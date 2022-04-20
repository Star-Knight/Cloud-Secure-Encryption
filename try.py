from distutils.log import debug
from flask import Flask, url_for,render_template,request,redirect
from cryptography.fernet import Fernet
import pyrebase
import pandas as pd
import numpy as np
from csv import writer
config = {
  "apiKey": "AIzaSyC-90sv52ivkCIl60hIPSovxNWdRgVJIm0",
  "authDomain": "dccdata-7c0f0.firebaseapp.com",
  "databaseURL": "https://dccdata-7c0f0-default-rtdb.firebaseio.com",
  "projectId": "dccdata-7c0f0",
  "storageBucket": "dccdata-7c0f0.appspot.com",
  "messagingSenderId": "921498219196",
  "appId": "1:921498219196:web:38d54cd81324f1c88b96b9",
  "measurementId": "G-3G6WW3BPSK"
}
firebase=pyrebase.initialize_app(config)
db=firebase.database()
app = Flask(__name__)

@app.route('/', methods= ["POST", "GET"])
def home():
   if request.method=="POST":
      user=request.form["nm"]
      key = Fernet.generate_key()
      fernet = Fernet(key)
      encMessage = fernet.encrypt(user.encode())
      encMessage = encMessage.decode()
      data={"pas":str(encMessage)}
      db.child("passes").child("pass").push(data)
      us=db.child("passes").child("pass").get()
      da = pd.DataFrame(us.val())
      df=da.T
      df.insert(0, 's', range(0, 0 + len(df)))
      df.set_index("s")
      df.to_csv('see.csv', index=False)
      new=pd.read_csv("see.csv")
      new.drop('s', inplace=True, axis=1)
      for i in range(len(new)):
          new['pas'][i]=bytes(new['pas'][i], 'utf-8')
      trmp=[]
      for index, row in new.iterrows():
         trmp.append(row['pas'])
      dm=fernet.decrypt(trmp[-1]).decode()
      temp=[]
      temp.append(dm)
      with open('event.csv', 'a') as f_object:
         writer_object = writer(f_object)
         writer_object.writerow(temp)
         f_object.close()
      god=pd.read_csv("event.csv")
      god =god.dropna()
      god.loc[~(god==0).all(axis=1)]
      return redirect(url_for("user", usr=dm))
      #return render_template('table.html',tables=[god.to_html(classes='ram')], titles = ['ram'])
   else:
      return render_template('index.html')

@app.route("/<usr>")
def user(usr):
   return render_template('ret.html',usr=usr)

@app.route("/table")
def disp():
   god=pd.read_csv("event.csv")
   god =god.dropna()
   god.loc[~(god==0).all(axis=1)]
   return render_template('table.html',tables=[god.to_html(classes='ram')], titles = ['ram'])

if __name__ == '__main__':
   app.run(debug=True)