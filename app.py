import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'task_manage'
app.config["MONGO_URI"] = 'mongodb+srv://root:r00tUser@myfirstcluster-qowfo.mongodb.net/task_manage?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.task.find())

@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
                           categories=mongo.db.category.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.task
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.task.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)