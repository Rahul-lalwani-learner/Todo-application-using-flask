from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
#Flask Minimal app
db.Model
class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.Integer,nullable=False)
    now_asia = timezone("Asia/Kolkata")
    date_created=db.Column(db.DateTime,default=datetime.now(now_asia))

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


#Creating Database
with app.app_context():
    db.create_all()
@app.route('/',methods=['GET','POST'])#This are methods that we are using in a single route
def addTask():
    if request.method=="POST":#accepting post request
        Title=request.form['title']
        Desc=request.form['desc']
        todo = Todo(title=Title,desc=Desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    # print(allTodo)
    return render_template("index.html",allTodo=allTodo)
    # return "Hello, world"
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # allTodo=Todo.query.all()
    # print(allTodo)
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        Title=request.form['title']
        Desc=request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title=Title
        todo.desc=Desc
        now_asia = timezone("Asia/Kolkata")
        todo.date_created=datetime.now(now_asia)
        # db.session.add(todo)
        db.verified=True
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)
    # allTodo=Todo.query.all()
    # print(allTodo)
    # return "This is update page"

#This is rendor products page
@app.route('/show')
def products(): 
    allTodo=Todo.query.all()
    print(allTodo)
    return "This are all my todos"
if __name__=="__main__":
    app.run(debug=True) 


#Any file in static folder that fill will be able to open in server

#templates folder is used for saving templates