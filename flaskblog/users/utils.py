import os

from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message

from flaskblog import mail


def delete_old_profile_picture():
    old_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file)
    # os.remove(old_picture_path)


def save_picture(form_picture):
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    hash_hex = str(hex(hash(i.tobytes()))).replace("0x", "")  # Remove '0x', even if '-0x'
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = hash_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply.flaskblog@webcoder49.dev',
                  recipients=[user.email])
    msg.html = f'''<p>To reset your password, visit the following link:<br/>
<a href="{url_for("users.reset_token", token=token, _external=True)}">Reset Password</a></p>
<p>If you did not make this request then simply ignore this email and no changes will be made.</p>
    '''
    mail.send(msg)
