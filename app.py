from flask import Flask, request, render_template
import flask_sqlalchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # SQLite database in templates folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
    test_duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Test {self.id} {self.test_name}>'

def create_tables():
    with app.app_context():
        db.create_all()

create_tables()  # Call the function to create the database tables in templates folder

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        test_name = request.form['name']
        test_duration = request.form['duration']
        new_test = Test(test_name=test_name, test_duration=test_duration)

        try:
            db.session.add(new_test)
            db.session.commit()
            return 'Test added successfully!'
        except:
            return 'There was an issue adding your test.'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
