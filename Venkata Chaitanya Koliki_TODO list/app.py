from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser as dparser


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///task.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
app.app_context().push()

class Task(db.Model):
    __tablename__ = "task"

    id=db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Text)
    date_added = db.Column(db.Date)
    done = db.Column(db.Boolean)

    def __init__(self, task, date_added,done):
        self.task = task
        self.date_added = date_added
        self.done = done

    def __repr__(self):
        return "{} - {} - {}".format(self.task,self.date_added, self.done)

db.create_all()

@app.route('/')
def index():
    # todos=Task.query.all()
    undone = Task.query.filter_by(done=False).all()
    done = Task.query.filter_by(done=True).all()


    return render_template('index.html',done=done,undone=undone)


@app.route('/add',methods=['POST'])
def add():
    tasks=Task(task=request.form['task_name'],date_added=dparser.parse(request.form['date_added'], fuzzy=True).date(),done=False)
    db.session.add(tasks)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/done/<id>')
def done(id):
    todo=Task.query.filter_by(id=int(id)).first()
    todo.done=True
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update/<id>',methods=['GET','POST'])
def update(id):
    undone = Task.query.filter_by(done=False).all()

    return render_template('update.html',undone=undone)

@app.route('/update_task',methods=['GET','POST'])
def update_task():
    if request.method == 'POST':
        t_id=Task.query.get(request.form.get('id'))

        t_id.task = request.form['task_name']
        t_id.date_added = dparser.parse(request.form['date_added'], fuzzy=True).date()
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/delete/<id>')
def delete(id):
    tasks=Task.query.filter_by(id=int(id)).first()
    print(tasks)
    db.session.delete(tasks)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        search = request.form['search_name']
        search_tasks = Task.query.filter(Task.task.like('%' + search + '%'))

        return render_template('index.html', search_tasks=search_tasks,search=search)


@app.route('/sortedAsc')
def sortedAsc():
    asc = Task.query.order_by(Task.date_added).filter_by(done=False).all()
    done = Task.query.filter_by(done=True).all()

    return render_template('index.html',done=done,asc=asc)

@app.route('/sortedDesc')
def sortedDesc():
    desc = Task.query.order_by(Task.date_added.desc()).filter_by(done=False).all()
    done = Task.query.filter_by(done=True).all()

    return render_template('index.html',done=done,desc=desc)



if __name__=='__main__':
    app.run(host="localhost", port=9566,debug=True)
