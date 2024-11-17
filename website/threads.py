from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, School, Thread, Message
from .import db
from sqlalchemy.sql import func

thread = Blueprint('thread', __name__)


@thread.route('/threads', methods=['GET', 'POST'])
@login_required
def view_threads():
    # Get threads associated with the user's school
    school = School.query.get(current_user.schoolId)
    threads = Thread.query.filter_by(school_id=current_user.schoolId).order_by(Thread.time_stamp.desc()).all()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Validate thread title and description
        if not title or len(title) < 3:
            flash('Thread title must be at least 3 characters.', category='error')
        elif not description or len(description) < 10:
            flash('Thread description must be at least 10 characters.', category='error')
        elif any(thread.title == title for thread in threads):
            return redirect(url_for('thread.view_threads'))  # Do not flash for existing database threads
        else:
            # Create new thread
            new_thread = Thread(
                title=title,
                description=description,
                school_id=current_user.school_id,  # Associate with the user's school
                created_by=current_user.id,  # Save creator's user ID
                time_stamp=func.now()
            )

            db.session.add(new_thread)
            db.session.commit()
            flash('Thread created successfully THROUGH DATABASE!', category='success')
            return redirect(url_for('thread.view_threads'))

    return render_template('view_threads.html', user=current_user, threads=threads, school=school)

@thread.route('/threads/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def thread_messages(thread_id):
    # Fetch the thread and its messages
    thread = Thread.query.get_or_404(thread_id)
    messages = Message.query.filter_by(thread_id=thread_id).order_by(Message.time_stamp.asc()).all()

    for i in messages:
        print(i)


    if request.method == 'POST':
        content = request.form.get('content')



        # Validate message content
        if not content or len(content.strip()) == 0:
            flash('Message cannot be empty.', category='error')
        else:
            # Create new message
            new_message = Message(
                thread_id=thread_id,
                user_id=current_user.first_name,
                content=content.strip(),
                time_stamp=func.now()
            )
            db.session.add(new_message)
            db.session.commit()

            return redirect(url_for('thread.thread_messages', thread_id=thread_id))
            
           
    return render_template('thread_messages.html', thread=thread, messages=messages, user=current_user)
