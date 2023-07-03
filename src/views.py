from flask import jsonify, render_template, redirect, request
from db import Database, convert_to_dict

def configure(app):

    @app.route('/home')
    def api():
        keys = ('id', 'task', 'priority')
        db = Database()
        connection = db.connect()

        if connection:
            data = db.select('SELECT {} FROM {};'.format('*', 'todo'))

            if data:
                tasks = convert_to_dict(data, keys)

            db.disconnect()
        return render_template('home.html', tasks=tasks)

    @app.route('/add', methods=['GET', 'POST'])
    def add_task():
        if request.method == 'GET':
            return render_template('add.html')
        elif request.method == 'POST':
            db = Database()
            connection = db.connect()

            if connection:
                task, priority = request.form['task'], request.form['priority']
                if task and priority:
                    db.insert("INSERT INTO todo (task, priority) VALUES ('{}', '{}')".format(task, priority))

                db.disconnect()

            return redirect('/home')

    @app.route('/del/<id>')
    def delete_id(id):
        db = Database()
        connection = db.connect()

        if connection:
            db.insert("DELETE FROM todo WHERE id = {}".format(id))
            db.disconnect()

        return redirect('/home')
