from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, FloatField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed


class LoginForm(FlaskForm):
username = StringField('Username', validators=[DataRequired()])
password = PasswordField('Password', validators=[DataRequired()])
submit = SubmitField('Login')


class PageForm(FlaskForm):
title = StringField('Title', validators=[DataRequired()])
slug = StringField('Slug', validators=[DataRequired()])
content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
submit = SubmitField('Save')


class EventForm(FlaskForm):
title = StringField('Title', validators=[DataRequired()])
venue = StringField('Venue')
date = DateTimeField('Date (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M')
ticket_link = StringField('Ticket Link')
description = TextAreaField('Description')
submit = SubmitField('Save')


class ProductForm(FlaskForm):
name = StringField('Name', validators=[DataRequired()])
price = FloatField('Price', validators=[DataRequired()])
description = TextAreaField('Description')
image = FileField('Image', validators=[FileAllowed(['jpg','jpeg','png','gif'])])
submit = SubmitField('Save')


class MediaForm(FlaskForm):
file = FileField('Image/Video', validators=[FileAllowed(['jpg','jpeg','png','gif','mp4','webm'])])
caption = StringField('Caption')
submit = SubmitField('Upload')


class ContactForm(FlaskForm):
name = StringField('Name', validators=[DataRequired()])
email = StringField('Email', validators=[DataRequired(), Email()])
message = TextAreaField('Message', validators=[DataRequired()])
submit = SubmitField('Send')
