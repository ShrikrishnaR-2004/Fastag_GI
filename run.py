import os
from app import create_app
from app.extensions import db

app = create_app(os.getenv('FLASK_ENV', 'default'))


@app.shell_context_processor
def make_shell_context():
    from app.models import User
    return dict(db=db, User=User)


if __name__ == '__main__':
    app.run(debug=True)
