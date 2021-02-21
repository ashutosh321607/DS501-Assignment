from flask import Flask,render_template,request
import requests

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    return render_template('Home.html')
@app.route('/pipe',methods=['GET','POST'])
def pipe():
    data=request.form.get("data")
    payload={}
    headers={}
    print("Recieved Data in Pipe/app")
    url='http://127.0.0.1:5000/autocomplete?query='+str(data)
    response=requests.request("GET",url,headers=headers,data=payload)
    return response.json()



if __name__ == '__main__':
    app.run(debug=True)
