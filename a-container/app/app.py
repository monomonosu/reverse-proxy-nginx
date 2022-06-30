# 本体
from datetime import timedelta
from flask import Flask, session,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData

#app = Flask(__name__)

SESSION_LIFE_TIME = 30

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))


app = CustomFlask(__name__)


@app.before_request
def before_request():
    # リクエストのたびにセッションの寿命を更新する
    if "/is-session" == request.path:
        session.permanent = False
        session.modified = False
        return

    if session.get('_id'):
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=SESSION_LIFE_TIME)
        session.modified = True
    else:
        pass

# これが無いとUNIQUE付与できん
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///caddie.db"

app.permanent_session_lifetime = timedelta(minutes=SESSION_LIFE_TIME)

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
ma = Marshmallow(app)
