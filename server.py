from flask import Flask, render_template,request, redirect
from mysqlconn import connectToMySQL 

app = Flask(__name__)

@app.route("/users")
def index():
    mysql = connectToMySQL('users')
    users = mysql.query_db('SELECT * FROM users;')
    userData = users
    print(users)
    return render_template("index.html", all_users = users, userData = userData[0] )

@app.route("/users/<id>/destroy")
def delete (id):
    db = connectToMySQL("users")
    num= int(id)
    query = f"DELETE FROM users WHERE id = {num} ;"
    data = {
        "num": int(id)
    }
    db.query_db(query, data)
    print(query)
    return redirect("/users")


@app.route("/users/new")
def new():
    return render_template("new.html")


# def redirect_db():
#     mysql = connectToMySQL('users') 
#     users = mysql.query_db('SELECT * FROM users;')
#     return redirect("/users")


@app.route("/users/create", methods=["POST"])
def create():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(email)s, NOW(), NOW());"

    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "email": request.form["email"]
    }
    db = connectToMySQL('users')
    id = db.query_db(query,data)

    print(id)
    return redirect("/users/"+ str(id))


@app.route("/users/<id>")
def show(id):
    print(id)
    db = connectToMySQL("users")
    query = "SELECT * FROM users WHERE id=%(id_num)s;"

    data = {
        "id_num": id
    }
    userData = db.query_db(query, data)
    

    # print (type(userData[0]))
    return render_template("show.html", userData=userData[0])


@app.route("/users/<id>/edit")
def edit_id (id):
    db = connectToMySQL("users")
    query = "SELECT * FROM users WHERE id=%(id_num)s;"
    data = {
        "id_num": id
    }
    userData = db.query_db(query, data)
    return render_template("edit.html",userData=userData[0])

@app.route("/users/<id>/update", methods=["POST"])
def update(id):
    db = connectToMySQL("users")
    query = "UPDATE users SET `first_name` = %(fn)s, `last_name` = %(ln)s, `email` = %(email)s WHERE (`id` = int %(id_num)s);"
    data = {
        "fn" : request.form["first_name"],
        "ln" : request.form["last_name"],
        "email" : request.form["email"],
        "id_num": id
    }
    db.query_db(query,data)
    return redirect ("/users/"+ str(id))

@app.route("/users/<id>/destroy")
def destroy(id):
    db = connectToMySQL("users")
    num= int(id)
    # query = "DELETE FROM users WHERE id = %(num)d ;"
    query = f"DELETE FROM users WHERE id = {num} ;"
    print(query)
    data = {
        "num": int(id)
    }
    db.query_db(query,data)
    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True) 
