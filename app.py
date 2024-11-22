from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
username = "root"
password = ""
database_name = "flask_db"
host = "localhost"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database_name}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'connect_timeout': 300
    }
}

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Correct usage of datetime.utcnow

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            return f"error adding the task: {str(e)}", 500

    else:
        tasks = Todo.query.order_by(desc(Todo.created_at)).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        db.session.rollback()
        return f"error adding the task: {str(e)}", 500


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            return f"error adding the task: {str(e)}", 500


    return render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
