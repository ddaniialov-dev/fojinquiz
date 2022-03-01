from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship


from quiz_project.behaviours.base_model import BaseModel
from quiz_project.utils import get_current_time

class Test(BaseModel):
    __tablename__ = "tests"
    
    holder = Column(Integer, ForeignKey("users.id"))
    published = Column(Boolean, default=True)
    published_date = Column(DateTime, default=get_current_time)
    questions = relationship("Question")


class Question(BaseModel):
    __tablename__ = "questions"
    
    test = Column(Integer, ForeignKey("tests.id"))
    text = Column(Text)


class Answer(BaseModel):
    __tablename__ = "answers"
    
    question = Column(Integer, ForeignKey("questions"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)


class UserAnswer(BaseModel):
    __tablename__ = "user_answers"
    
    answer = Column(Integer, ForeignKey())