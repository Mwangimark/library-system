from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# all_books = [
#      {
#
#     }
# ]

all_books = []


@app.route('/')
def home():
    return render_template('index.html', all_books=all_books)


@app.route('/add', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        data = request.form

        title = data['book_name']
        author = data['book_author']
        rating = data['rating']
        book = {
            "title": title,
            "author": author,
            "rating": rating
        }

        all_books.append(book)
        print(all_books)
        return redirect(url_for('home'))


    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
