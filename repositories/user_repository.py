from extensions import db
from models.user import User

class UserRepository:

    @staticmethod
    def get_all():
        return User.query.order_by(User.created_at.desc()).all()

    @staticmethod
    def get_by_id(user_id: int):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email: str):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(name: str, email: str, password: str):

        user = User(name=name, email=email,password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update(user: User, name: str = None, email: str = None, password: str = None):
        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.password = password

        db.session.commit()
        return user

    @staticmethod
    def delete(user: User):

        db.session.delete(user)
        db.session.commit()