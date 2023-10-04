from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    img_url = StringField("Image URL", [DataRequired()])
    caption = StringField("Caption")
    submit = SubmitField()

class PokeForm(FlaskForm):
    name = StringField(label='Look Up a Pokemon', validators=[DataRequired()])
    submit = SubmitField()