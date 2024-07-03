from flask import render_template, request, Blueprint
from app.models import Task
import calendar
from datetime import datetime, timedelta


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    tasks = Task.query.order_by(Task.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', tasks=tasks)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

  
@main.route("/calendar")
def calendar_view():
    now = datetime.now()
    current_month = now.strftime("%B %Y")
    next_month = (now.replace(day=28) + timedelta(days=4)).strftime("%B %Y")  # Next month approximation
    
    # Generate calendar data for current month
    _, days_in_month = calendar.monthrange(now.year, now.month)
    current_month_data = []
    day_counter = 1
    for _ in range(6):  # 6 weeks to cover all possibilities
        week = []
        for _ in range(7):
            if day_counter <= days_in_month:
                week.append(day_counter)
                day_counter += 1
            else:
                week.append('')
        current_month_data.append(week)
    
    # Generate calendar data for next month
    _, days_in_month = calendar.monthrange(now.year, now.month + 1 if now.month < 12 else 1)
    next_month_data = []
    day_counter = 1
    for _ in range(6):  # 6 weeks to cover all possibilities
        week = []
        for _ in range(7):
            if day_counter <= days_in_month:
                week.append(day_counter)
                day_counter += 1
            else:
                week.append('')
        next_month_data.append(week)

    today = now.day  # Get current day of the month

    return render_template('calendar.html', current_month=current_month, next_month=next_month,
                           current_month_data=current_month_data, next_month_data=next_month_data,
                           today=today)
