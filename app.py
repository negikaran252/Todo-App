from flask import Flask, render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(500),nullable=False)


@app.route("/",methods=["GET","POST"])
def hello_world():
    if request.method=="POST":
        todo_title = request.form.get("title")
        todo_desc = request.form.get("desc")
        todo = Todo(title=todo_title, desc=todo_desc)
        db.session.add(todo)
        db.session.commit()
    all_todos=Todo.query.all()
    # print(all_todos)
    return render_template("index.html",all_todos=all_todos)

@app.route("/delete/<int:sno>")
def delete(sno):
    me=Todo.query.filter_by(id=sno).first()
    db.session.delete(me)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>",methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        newtitle=request.form.get("title")
        newdesc = request.form.get("desc")
        me=Todo.query.filter_by(id=sno).first()
        me.title=newtitle
        me.desc=newdesc
        db.session.add(me)
        db.session.commit()
        return redirect("/")

    me=Todo.query.filter_by(id=sno).first()
    return render_template("update.html",todo=me)

if __name__ == '__main__':
    app.run(debug=True,port=8000)