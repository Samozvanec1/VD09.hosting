from app import db
from app import login_manager
from flask_login import UserMixin #для работы с базой данных

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(220), nullable=False)
    clicks = db.Column(db.Integer, default=1)# Column - столбец в базе данных

    def __repr__(self): # для отображения в консоли
        return f"User('{self.username}', '{self.clicks}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #загрузка пользователя из базы данных