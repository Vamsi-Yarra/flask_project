from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='secret',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello Flask!'


# with Query Strings
@app.route('/new/')
def get_request(greeting='hello'):
    query_val = request.args.get('greeting', greeting)
    return f'<h1>Greeting from user is {query_val}</h1>'


# without using query string format
@app.route('/user')
@app.route('/user/<name>')
def get_request_without_query_string(name='Rama'):
    return f'<h1> hello there! {name} </h1>'


# Working with Numbers
# Working with Types
@app.route('/text/<string:name>')
def get_string(name='Seetha'):
    return f'the name is {name}'


# Working with Integers
@app.route('/add/<int:num1>/<int:num2>')
def get_int_numbers(num1=0, num2 =0):
    return 'Sum of given numbers is {}'.format(num1 + num2)

# Working with Floats
@app.route('/product/<float:num1>/<float:num2>')
def get_float_numbers(num1=0, num2 =0):
    return 'Sum of given numbers is {}'.format(num1 * num2)

@app.route('/temp')
def using_template():
    return render_template('hello.html')


# Using Jinja2 Templates
@app.route('/watch')
def top_movies():
    movies_list = ['RRR', 'Pushpa 1', 'Bheemla Nayak', 'Radhe Shyam', 'Skylab']

    return render_template('movies.html', movies=movies_list, name='Vamsi')


# using Jinja2 templates with tables and conditions
@app.route('/tables')
def movies_plus():
    movies_dict = {
        'RRR': 3.2,
        'Puspha 1': 2.40,
        'Bheemla Nayak': 1.2,
        'Radhe Shyam': 4.2,
        'Skylab': 4.1
    }

    return render_template('tables.html', movies = movies_dict, name='Raki')


# using Jinja2 templates for filters
@app.route('/filters')
def filter_data():
    movies_dict = {
        'RRR': 3.2,
        'Puspha 1': 2.40,
        'Bheemla Nayak': 1.2,
        'Radhe Shyam': 4.2,
        'Skylab': 4.1
    }

    return render_template('filter_data.html', movies=movies_dict, name=None, film='Vakeel Saab')


# using Jinja2 macros
@app.route('/macros')
def macros():
    movies_dict = {
        'RRR': 3.2,
        'Puspha 1': 2.40,
        'Bheemla Nayak': 1.2,
        'Radhe Shyam': 4.2,
        'Skylab': 4.1
    }

    return render_template('using_macros.html', movies=movies_dict)


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The publisher is {}'.format(self.name)

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # Foreign Key relationship
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)