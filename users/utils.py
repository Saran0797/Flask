from flask import url_for, current_app
import secrets
import os
from package import mail
from flask_mail import Message


def save_picture(pic_file):
    random_hex = secrets.token_hex(8)
    _, f_exe = os.path.splitext(pic_file.filename)
    file_name = random_hex + f_exe
    file_path = os.path.join(current_app.root_path, "static/profile_pic", file_name)
    pic_file.save(file_path)
    return file_name


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", recipients=[user.email], sender="noreply@gmail.com")
    msg.body = f''' To Reset Your Password visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.'''
    mail.send(msg)
