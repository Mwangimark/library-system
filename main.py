from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my_books.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    author = db.Column(db.String(255), unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():
    all_books = db.session.query(Books).all()
    return render_template('index.html', all_books=all_books)


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        data = request.form

        title = data['book_name']
        author = data['book_author']
        rating = data['rating']

        book_record = Books(title=title, author=author, rating=rating)
        db.session.add(book_record)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit_book():
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = Books.query.get(book_id)
        print(book_to_update.rating)
        book_to_update.rating = request.form['rate_update']
        db.session.commit()

        return redirect(url_for('home'))

    book_id = request.args.get("id")
    selected_book = Books.query.get(book_id)
    return render_template('edit.html', book=selected_book)


@app.route('/delete')
def delete():
    book_id = request.args.get('id')
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
