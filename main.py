from flask.helpers import get_flashed_messages
from pymongo import MongoClient
from flask import Flask, render_template, request, flash, jsonify, session, redirect, url_for
from flask_cors import CORS
from bson.json_util import dumps
from bson import ObjectId
import json
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
client = MongoClient('localhost', 27017)
db = client['userblog']
blogs = db['blogs']
users = db['users']
feedback = db['feedback']

app.config['SECRET_KEY'] = "some super secret"


@app.route("/submitblog", methods=['POST'])
def submit():
    print("executing...")
    print(request.get_data())

    try:
        data = json.loads(request.data)
        user_title = data['title']
        user_content = data['content']
        user_name = data['uname']
        print(user_name, user_content, user_title)
        if user_title and user_content and user_name:
            # print('this line is executing')
            status = blogs.insert_one({
                "title": user_title,
                "content": user_content,
                "uname": user_name
            })
        get_flashed_messages("succesfully submitted")

        return dumps({'message': 'SUCCESS'})
    except:
        return dumps({'success': False,
                      'error': 'something went wrong'})




@app.route("/auth/signup", methods=['POST'])
def signup():
    print(request.get_data())

    try:
        data = json.loads(request.data)
        name = data['name']
        email = data['email']
        pw = data['pw']
        if name and email and pw:
            status = users.insert_one({
                "name": name,
                "email": email,
                "pw": pw
            })
            print("user success")
            return dumps({"success": True})
        else:
            print("unable to save data")
            return dumps({
                'success': False,
                'error': 'something went wrong'
            })
    except:
        print("server error")
        return dumps({
            'success': False,
            'error': 'something went wrong'
        })


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.form
        users = db['users']

        if data:
            email = data['email']
            password = data['pw']
            login_user = users.find_one({
                'email': email,
                'pw': password
            })

            if login_user:
                id = login_user['_id']
                id = str(id)
                session['logged_in'] = True
                session['EMAIL'] = login_user["email"]
                session['USERNAME'] = login_user['name']
                session["USERID"] = id
                print('login successful')
                flash("you are successfuly logged in")
                return redirect(url_for('home'))

            else:
                flash("login failed")
                return redirect(url_for('signin'))
        else:
            flash("login failed")
            return redirect(url_for('signin'))

    else:
        flash("login failed")
        return redirect(url_for('signin'))

# @app.route('/feedback', methods=['POST', 'GET'])
# def feedback():
   
     
       



@app.route("/")
def home():
    return render_template("home.html")


@app.route("/blogs")
def blog():
    return render_template("blogs.html")


@app.route("/living")
def blog1():
    return render_template("living.html")


@app.route("/terrace")
def blog2():
    return render_template("terrace.html")


@app.route("/office")
def blog3():
    return render_template("office.html")


@app.route("/bedroom")
def blog4():
    return render_template("bedroom.html")


@app.route("/balcony")
def blog5():
    return render_template("balcony.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


@app.route("/createblog")
def createblog():
    return render_template("createblog.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/contactus" ,methods=['POST', 'GET'])
def contactus():
    if request.method == "POST":
        data1 = request.form
        feedback = db['feedback']
        print(data1)

        if data1:
            fname = data1['fname']
            lname = data1['lname']
            cmnt = data1['cmnt']
            suggestn = data1['suggestn']
            if lname and fname and cmnt and suggestn:
                feed = feedback.insert_one({
                'fname': fname,
                'lname': lname,
                'cmnt': cmnt,
                'suggestn': suggestn,

            })
            
            return render_template("contactus.html")
        else:
            print("unable to save data")
            return dumps({
                'success': False,
                'error': 'something went wrong'
            })
    if request.method=="GET":
        return render_template("contactus.html")


@app.route("/userblogs")
def userblog():
    x = blogs.find()
    lis = []
    for data in x:
        lis.append([data['title'], data['content'], data['uname']])

    return render_template("userblog.html", lis=lis)


@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.max_age = 0
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
