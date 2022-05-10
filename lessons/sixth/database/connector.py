from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .models import initialize
from lessons.sixth import DATABASE
from lessons.sixth.static import (
    AnswerType, 
    GameType
)
from bcrypt import (
    checkpw,
    hashpw,
    gensalt
)
from typing import (
    List,
    Any,
    Tuple,
    Dict,
    Type
)


class Database():
    @staticmethod
    def session_required(expire_on_commit=False, auto_commit=True):
        def wrapper(function):
            def make_request(args, kwargs):
                session = kwargs.get('session')                
                session.expire_on_commit = expire_on_commit
                result = function(*args, **kwargs)
                if auto_commit:
                    session.commit()
                return result  

            def inner(*args, **kwargs):
                _self= args[0]  # args[0] -> returns self                
                if kwargs.get('session') is not None:
                    return make_request(args, kwargs)
                
                with _self.engine.connect() as connection:
                    with _self.Session(bind=connection) as session:
                        kwargs['session'] = session
                        return make_request(args, kwargs)
            return inner  
        return wrapper

    def __init__(self) -> None:
        db_uri = f'{DATABASE["ENGINE"]}:///{DATABASE["NAME"]}'
        self.engine = create_engine(db_uri)        
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()
        for model in initialize(self.Base):
            setattr(self, f'md_{model.__name__}', model)

    def migrate(self) -> None:
        print('Migrating Started...')
        self.Base.metadata.create_all(self.engine)
        print('Migrating Finished...')

# Database methods 
    @session_required()
    def check_for_user(self, username: str, session):
        return session.query(self.md_User).filter_by(username=username).first()
        
    @session_required()
    def create_new_user(self, gamename: str, username: str, password: str, session):
        if self.check_for_user(username, session=session) is not None:
            return -1
        hashed_password = hashpw(password.encode(), gensalt())
        new_user = self.md_User(
            gamename=gamename, 
            username=username,
            password=hashed_password
        )
        session.add(new_user)
        return new_user

    @session_required()
    def authenticate_user(self, username, password, session):
        if (user := self.check_for_user(username, session=session)) is not None:            
            if checkpw(password.encode(), user.password):
                return user
        return -1        

    @session_required()
    def get_game(self, game_id, session):
        return session.query(self.md_Game).filter_by(id=game_id).first()

    @session_required()
    def get_all_games(self, username, session):
        user = self.check_for_user(username, session=session)
        return user.games

    @session_required()
    def get_game_attempts(self, game_id, session):
        game = self.get_game(game_id, session=session)
        return game.attempts
        
    @session_required()
    def start_game(self, game_type, user_id, session):
        game_object = {
            'game_type': game_type, 
            'user_id': user_id,
        }
        new_game = self.md_Game(**game_object)
        session.add(new_game)
        return new_game

    @session_required()
    def finish_game(self, game_id, points, guessed_in, session):
        game = self.get_game(game_id, session=session)
        mask = 0b0
        if game.game_type is GameType.USER_GUESSES:
            attempts = self.get_game_attempts(game_id, session=session)            
            for index, attempt in enumerate(attempts):
                write = 0
                if attempt.response == AnswerType.BIGGER:
                    write = 1
                mask = mask | (write << index)  # Writing 0 if SMALLER else 1 (BIGGER)
        update_with = {
            'points': points,
            'guessed_in': guessed_in,
            'bits_mask': format(mask, f'0{len(attempts)}b') if mask else ''  # Not to lose leading zeros
        }

        for update in update_with.items():
            setattr(game, *update)
        return game

    @session_required()
    def add_attempt(self, game_id, penalty_point, suppose, response, session):        
        attempt_object = {
            'game_id': game_id,
            'penalty': penalty_point,
            'suppose': suppose,
            'response': response
        }
        new_attempt = self.md_GameAttempt(**attempt_object)
        session.add(new_attempt)
        return new_attempt