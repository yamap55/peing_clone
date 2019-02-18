from flask_login import UserMixin
from sqlalchemy import Column, Integer, Sequence, DATETIME, VARCHAR

from datetime import datetime, timezone, timedelta

# from . import BaseModel
from database import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # ユーザーが一意となるIDを取得できるメソッドが必要
    def get_id(self):
        return self.id

    get_datetime_now = lambda: datetime.now(timezone(timedelta(hours=+9), 'JST'))
    id = Column(Integer, Sequence('seq_user_id'), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME, nullable=False, default=get_datetime_now)
    updated_at = Column(DATETIME, nullable=False, default=get_datetime_now, onupdate=get_datetime_now)
