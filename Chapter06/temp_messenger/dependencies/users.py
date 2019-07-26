import bcrypt

from nameko_sqlalchemy import DatabaseSession
from sqlalchemy import Column, Integer, LargeBinary, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import runtime

HASH_WORK_FACTOR = 15
Base = declarative_base()


class CreateUserError(Exception):
    pass


class UserAlreadyExists(CreateUserError):
    pass


class UserNotFound(Exception):
    pass


class AuthenticationError(Exception):
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=128))
    last_name = Column(Unicode(length=128))
    email = Column(Unicode(length=256), unique=True, index=True)
    # password = Column(LargeBinary())
    password = Column(Unicode(length=255))


class UserWrapper:

    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        plain_text_password = kwargs['password']
        hashed_password = hash_password(plain_text_password)
        kwargs.update(password=hashed_password)

        user = User(**kwargs)
        self.session.add(user)

        try:
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            error_message = err.args[0]

            if 'already exists' in error_message:
                email = kwargs['email']
                message = 'User already exists - {}'.format(email)
                raise UserAlreadyExists(message)
            else:
                raise CreateUserError(error_message)

    def get(self, email):
        query = self.session.query(User)

        try:
            user = query.filter_by(email=email).one()
        except NoResultFound:
            message = 'User not found - {}'.format(email)
            raise UserNotFound(message)

        return user

    @runtime
    def authenticate(self, email, password):
        """这个函数耗费时间比较久"""
        user = self.get(email)

        # 这个密码验证机制效率太慢
        # if not bcrypt.checkpw(password.encode(), user.password):
        #     message = 'Incorrect password for {}'.format(email)
        #     raise AuthenticationError(message)

        if not check_password_hash(user.password, password):
            message = 'Incorrect password for {}'.format(email)
            raise AuthenticationError(message)

        return user


class UserStore(DatabaseSession):

    def __init__(self):
        super().__init__(Base)

    def get_dependency(self, worker_ctx):
        """override"""
        database_session = super().get_dependency(worker_ctx)
        return UserWrapper(session=database_session)


def hash_password(plain_text_password):
    # 这个密码验证机制效率太慢
    # salt = bcrypt.gensalt(rounds=HASH_WORK_FACTOR)
    # encoded_password = plain_text_password.encode()
    # return bcrypt.hashpw(encoded_password, salt)

    return generate_password_hash(plain_text_password)
