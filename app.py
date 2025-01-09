from flask import Flask, render_template, request , url_for,redirect,jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://shyam:shyam123@localhost:3306/todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    todos = db.relationship('Todo',backref="category")

class Employee(db.Model):
    eid = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String(200), nullable=False)
    lname = db.Column(db.String(200), nullable=False)
    job_role = db.Column(db.String(200), nullable=False)
    salary = db.Column(db.Float)


#for desplay category in dropdown menu
# @app.route('/')
# def show_category():
#     categories = Category.query.all()
#     return render_template('index.html', categories=categories)

@app.route("/todo/<int:sno>", methods=["PUT"])
def update_todo_put(sno):

    print(f"Updating Todo with sno: {sno}")  # Debugging log

    todo = Todo.query.get_or_404(sno)   
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    print(f"Found Todo: {todo.title}")  # Log the found todo

    data = request.get_json()
    todo.title = data.get("title", todo.title)  
    todo.desc = data.get("desc", todo.desc)
    todo.category_id = data.get("category_id", todo.category_id)  
  

    db.session.commit()
    # return "success"  ,200
    return jsonify({"message": "Todo updated successfully!", "todo": todo.title, "desc": todo.desc}), 200  

@app.route("/patchdata/<int:sno>",methods=["PATCH"])
def update_todo_title(sno):
    todo = Todo.query.get_or_404(sno)
    data = request.get_json()

    todo.title = data.get("title",todo.title)
    todo.desc = data.get("desc", todo.desc)  
    todo.category_id = data.get("category_id",todo.category_id)
    db.session.commit()
    return "success",200

@app.route("/post_todo_data", methods=["POST"])
def post_method():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Check each item in the data for required fields
    for item in data:
        if "title" not in item or "desc" not in item:
            return jsonify({"error": "Title or description is missing in one of the items"}), 400
        if "category_id" not in item:
            return jsonify({"error": "Category ID is required for each todo"}), 400

    new_todo_list = []
    for item in data:
        category_id = item['category_id']
        
        # Check if the category exists
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": f"Invalid category ID: {category_id}"}), 400
        
        # Create a new Todo for each item
        new_todo = Todo(
            title=item["title"],
            desc=item["desc"],
            date_created=datetime.now(),
            category_id=category_id
        )
        new_todo_list.append(new_todo)
    
    db.session.add_all(new_todo_list)
    db.session.commit()

    return jsonify({"message": "Todos added successfully!"}), 201

@app.route("/get_all_todo",methods=["GET"])
def get_all_todos():
    todos = Todo.query.all()

    todos_list = []
    for todo in todos:
        todos_list.append({
            "sno" :todo.sno,
            "title":todo.title,
            "description":todo.desc,
            "date created":todo.date_created
        }
        )
    return jsonify({"Todos":todos_list}),200

@app.route("/upload", methods = ['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(f'uploads/{secure_filename(file.filename)}')
    return redirect('/')

@app.route("/submit",methods = ['POST','GET'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        category_id = request.form['category_id']

        if not category_id:
            return "category is required", 400
        
        category = Category.query.get(category_id)
        if not category:
            return "Invalid category", 400
        
        new_todo = Todo(
            title=title,
            desc=desc,
            category_id=category.id
            )
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for("home_page"))
 
    return render_template("index.html")


@app.route("/")
def home_page():
    # Query all Todo items
    allTodo = Todo.query.all()
    categories = Category.query.all()

    # Convert the list of Todo objects into a list of dictionaries
    todo_list = []
    for todo in allTodo:
        todo_list.append({
            'sno': todo.sno,
            'title': todo.title,
            'desc': todo.desc,
            'date_created': todo.date_created.strftime("%Y-%m-%d %H:%M:%S")  # Formatting the date
        })
    # Return the list of todos as a JSON response
    # return jsonify(todo_list)
    return render_template('index.html', allTodo=allTodo,categories=categories)

# @app.route("/")
# def home_page():
    
#     allTodo =  Todo.query.all()
#     print(allTodo)

#     return render_template('index.html', allTodo=allTodo)
    # return "<p>Hello, World!</p>"
@app.route("/admin")
def hello_admin():
    return "Welcome to the admin page"

@app.route("/client/<name>")
def hello_guest(name):
    category = Category.query.get(2)
    todos_in_category = category.todos
    for todo in todos_in_category:
        return f'Title :{todo.title},Description:{todo.desc}'
    
    return "Welcome to the user page %s"%name


@app.route("/user/<username>")
def user(username):
    if username =='admin':
       return redirect(url_for('hello_admin'))
    else:
       return redirect(url_for('hello_guest',name = username))
    
    # return f"this is a product of user {username}"

if __name__ == "__main__":
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
