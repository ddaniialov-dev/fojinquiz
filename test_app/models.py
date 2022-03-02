from sqlalchemy import Boolean, Column, ForeignKey, Integer, DateTime, Text, Table
from sqlalchemy.orm import relationship


from quiz_project.behaviours import BaseModel
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
    answers = relationship("Answer")


class Answer(BaseModel):
    __tablename__ = "answers"
    
    question = Column(Integer, ForeignKey("questions.id"))
    text = Column(Text)
    is_true = Column(Boolean, default=True)
    user_answers = relationship("user_answers.id")


class UserAnswer(BaseModel):
    __tablename__ = "user_answers"
    
    answer = Column(Integer, ForeignKey("answers.id"))
    session = Column(Integer, ForeignKey("sessions.id"))


class Session(BaseModel):
    __tablename__ = "sessions"
    
    finished_date = Column(DateTime, nullable=True)
    user = Column(Integer, ForeignKey("users.id"))
    test = Column(Integer, ForeignKey("tests.id"))


association_table = Table('association', BaseModel.metadata,
    Column('question_id', ForeignKey('questions.id')),
    Column('session_id', ForeignKey('sessions.id'))
)