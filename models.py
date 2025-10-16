from flask_sqlalchemy import SQLAlchemy
content = db.Column(db.Text)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Event(db.Model):
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(256), nullable=False)
description = db.Column(db.Text)
venue = db.Column(db.String(256))
date = db.Column(db.DateTime)
ticket_link = db.Column(db.String(512))
created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(256), nullable=False)
description = db.Column(db.Text)
price = db.Column(db.Float, nullable=False)
sku = db.Column(db.String(64))
image = db.Column(db.String(256))
created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Media(db.Model):
id = db.Column(db.Integer, primary_key=True)
filename = db.Column(db.String(256), nullable=False)
caption = db.Column(db.String(256))
media_type = db.Column(db.String(32)) # 'image' or 'video'
uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class ContactMessage(db.Model):
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(128))
email = db.Column(db.String(128))
message = db.Column(db.Text)
created_at = db.Column(db.DateTime, default=datetime.utcnow)
