from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app import db
from app.models import Task
from app.tasks.forms import TaskForm, LoginForm


tasks = Blueprint('tasks', __name__)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_task.html', title='New Task',
                           form=form, legend='New Task')

@tasks.route("/task/<int:task_id>")
def task(task_id):
    task = Task.query.get_or_404(task_id)
    form = LoginForm()  # Assuming you are using LoginForm for the login section
    return render_template('task.html', title=task.title, task=task, form=form)

@tasks.route("/all_tasks", methods=['GET'])
def all_tasks():
    all_tasks = Task.query.order_by(Task.date_posted.desc()).all()
    return render_template('all_tasks.html', title='All Tasks', all_tasks=all_tasks)


@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content
    return render_template('create_task.html', title='Update Task',
                           form=form, legend='Update Task')


@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('main.home'))