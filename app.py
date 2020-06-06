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
                           category=mongo.db.category.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.task
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.task.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.category.find()
    return render_template('edittask.html', task=the_task,
                           category=all_categories)

@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.task
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.task.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_categories')
def get_categories():
    return render_template('category.html',
                           category=mongo.db.category.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.category.find_one(
                           {'_id': ObjectId(category_id)}))

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.category.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.category.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

@app.route('/insert_category', methods=['POST'])
def insert_category():
    category=mongo.db.category
    category_doc = {'category_name': request.form.get('category_name')}
    category.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html',
                           category=mongo.db.category.find())
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=(os.environ.get('PORT')),
            debug=True)