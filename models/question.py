from sqlalchemy import Column, Integer, Sequence, DATETIME, VARCHAR, ForeignKey
from sqlalchemy.orm import relation, backref

from datetime import datetime, timezone, timedelta

from database import db


class Question(db.Model):
    __tablename__ = 'questions'

    get_datetime_now = lambda: datetime.now(timezone(timedelta(hours=+9), 'JST'))
    id = Column(Integer, Sequence('seq_question_id'), primary_key=True)
    detail = Column(VARCHAR(255), nullable=False)
    answer = Column(VARCHAR(255), nullable=True, default='')
    user_id = Column(Integer, ForeignKey('users.id'))

    # UserとQuestionテーブルの関連を定義
    user = relation("User", backref=backref('questions', order_by=id))

    created_at = Column(DATETIME, nullable=False, default=get_datetime_now)
    updated_at = Column(DATETIME, nullable=False, default=get_datetime_now, onupdate=get_datetime_now)
