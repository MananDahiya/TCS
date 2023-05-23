from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from app.extensions import db
from app.models.user import User

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, ForeignKey("user.id", ondelete = "CASCADE"), nullable = False)
    updated_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
    published_at = db.Column(db.DateTime(timezone = True), server_default = func.now())
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f'<Post {self.author_id}>'