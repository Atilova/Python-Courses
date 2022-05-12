from lessons.sixth.static import (
    GameType,
    AnswerType,
    GameLevel
)
from sqlalchemy.orm import (
    backref, 
    relationship
)
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Interval,
    Enum    
)


def initialize(Base):
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
        gamename = Column(String(25))
        username = Column(String(20), unique=True)
        password = Column(String(72))        


    class Game(Base):
        __tablename__ = 'games'
        id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
        game_type = Column(Enum(GameType))
        user = relationship('User', backref=backref('games', cascade='all,delete'))
        user_id = Column(Integer, ForeignKey('users.id'))
        points = Column(Integer, nullable=True)
        guessed_in = Column(Interval, nullable=True)
        bits_mask = Column(String, nullable=True)
        total_fine = Column(Integer, nullable=True)
        level = Column(Enum(GameLevel))


    class GameAttempt(Base):
        __tablename__ = 'attempts'
        id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
        game = relationship('Game', backref=backref('attempts', cascade='all,delete'))
        game_id = Column(Integer, ForeignKey('games.id'))
        penalty = Column(Boolean, default=False)
        suppose = Column(Integer)
        response = Column(Enum(AnswerType))


    return (
        User,
        Game,
        GameAttempt
    )