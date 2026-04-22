from flask import Flask, render_template, url_for, g, request
import sqlite3
DATABASE = "database.db"
app = Flask(__name__)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html" )

@app.route("/categories")
def view_categories():
    sql = "SELECT * FROM category"
    categories = query_db(sql)
    return render_template("categories.html", categories = categories)

@app.route ("/add_category", methods = ["POST"])
def add_category():
    category_name = request.form ['name']
    sql = "INSERT INTO categories (name, spending_limit) VALUES (?, ?)"
    query_db(sql,(category_name,))
    get_db().commit()
    return render_template (url_for ("view_categories"))
    return categories

@app.route ("/delete_category")
def delete_category():
    return 


@app.route

@app.route("/expenses")
def view_expenses():
    sql = """SELECT e.id, e.category_id, SUM (e.amount_spent), c.name, c.id FROM expenses 
          JOIN categories c ON e.category_id = c.id""" 
    expenses = query_db(sql)
    sql = "SELECT * FROM categories"
    categories = query_db(sql)
    return render_template("expenses.html", expenses=expenses, categories=categories)

if __name__ == "__main__":
    app.run(debug= True)
