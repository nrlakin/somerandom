from flask.ext.wtf import Form
from .models import Poster, Post
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class PostForm(Form):
    post = StringField('post', validators = [DataRequired(), Length(min=0, max=140)])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        return True
    
