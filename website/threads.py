from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import User, School, Thread, Message
from . import db
from sqlalchemy.sql import func



thread = Blueprint('thread', __name__)




def time_ago(timestamp):
    """Helper function to calculate how long ago a timestamp occurred."""
    now = datetime.utcnow()
    delta = now - timestamp

    if delta.days > 1:
        return f"{delta.days} days ago"
    elif delta.days == 1:
        return "1 day ago"
    elif delta.seconds >= 3600:
        hours = delta.seconds // 3600
        return f"{hours} hours ago"
    elif delta.seconds >= 60:
        minutes = delta.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

@thread.route('/', methods=['GET', 'POST'])
@login_required
def view_threads():
    # Get the user's school
    school = School.query.get(current_user.schoolId)

    # Fetch threads associated with the user's school
    threads = (Thread.query
               .filter_by(schoolId=current_user.schoolId)
               .order_by(Thread.time_stamp.desc())
               .all())
    for thread in threads:
        user = User.query.get(thread.created_by)
        thread.user = user


    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')

        # Validate thread title and description
        if not title or len(title.strip()) < 3:
            flash('Thread title must be at least 3 characters.', category='error')
        elif not description or len(description.strip()) < 10:
            flash('Thread description must be at least 10 characters.', category='error')
        elif any(thread.title.strip().lower() == title.strip().lower() for thread in threads):
            flash('A thread with this title already exists.', category='error')
        else:
            # Create and save the new thread
            new_thread = Thread(
                title=title.strip(),
                description=description.strip(),
                schoolId=current_user.schoolId,
                created_by=current_user.id,
                time_stamp=func.now()
            )

            db.session.add(new_thread)
            db.session.commit()

            flash('Thread created successfully!', category='success')
            return redirect(url_for('thread.view_threads'))

    return render_template('view_threads.html', user=current_user, threads=threads, school=school)

@thread.route('/threads/<int:thread_id>', methods=['GET', 'POST'])
@login_required
def thread_messages(thread_id):
    # Fetch the thread and its associated messages
    thread = Thread.query.get_or_404(thread_id)
    messages = (Message.query
                .filter_by(thread_id=thread_id)
                .order_by(Message.time_stamp.asc())
                .all())

    # Attach user information and "time ago" to messages
    for message in messages:
        message.user = User.query.get(message.user_id)
        message.time_ago = time_ago(message.time_stamp)

    if request.method == 'POST':
        content = request.form.get('content')

        # Validate message content
        if not content or len(content.strip()) == 0:
            flash('Message cannot be empty.', category='error')
        else:
            # Create and save the new message
            new_message = Message(
                thread_id=thread_id,
                user_id=current_user.id,
                content=content.strip(),
                time_stamp=func.now()
            )

            db.session.add(new_message)

        # Update the user's XP and level
            user = User.query.get(current_user.id)
            if not user:
                flash("User not found.", "error")
                return redirect(request.referrer)

            user.xp += 18
            if user.xp >= 100*user.level:
                user.level += 1
                user.xp = 1

            # Commit the changes to the database
            try:
                db.session.commit()
                flash("Message sent and XP updated successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred: {str(e)}", "error")

                return redirect(request.referrer)

            db.session.commit()



            flash('Message posted successfully!', category='success')
            return redirect(url_for('thread.thread_messages', thread_id=thread_id))

    return render_template('thread_messages.html', thread=thread, messages=messages, user=current_user)

