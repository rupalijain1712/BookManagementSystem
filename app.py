from flask import (
    Flask,
    render_template,
    request
)

from database import *
from gemini_service import *

app = Flask(__name__)

create_tables()


@app.route("/")
def home():
    return render_template(
        "home.html"
    )


@app.route("/add", methods=[
    "GET",
    "POST"
])
def add():

    if request.method == "POST":

        add_book(
            request.form["title"],
            request.form["author"],
            request.form["category"],
            request.form["price"]
        )

        return render_template(
            "success.html",
            message="Book Added Successfully"
        )

    return render_template(
        "add_book.html"
    )


@app.route("/view")
def view():

    books = get_all_books()

    return render_template(
        "view_books.html",
        books=books
    )


@app.route("/search",
           methods=["GET",
                    "POST"])
def search():

    book = None

    if request.method == "POST":

        book = search_book(
            request.form["id"]
        )

    return render_template(
        "search_book.html",
        book=book
    )


@app.route("/update",
           methods=["GET",
                    "POST"])
def update():

    if request.method == "POST":

        update_book(
            request.form["id"],
            request.form["title"],
            request.form["author"],
            request.form["category"],
            request.form["price"]
        )

        return render_template(
            "success.html",
            message="Book Updated Successfully"
        )

    return render_template(
        "update_book.html"
    )


@app.route("/delete",
           methods=["GET",
                    "POST"])
def delete():

    if request.method == "POST":

        delete_book(
            request.form["id"]
        )

        return render_template(
            "success.html",
            message="Book Deleted Successfully"
        )

    return render_template(
        "delete_book.html"
    )


@app.route("/recommend",
           methods=["GET",
                    "POST"])
def recommend():

    recommendation = ""

    if request.method == "POST":

        interest = request.form[
            "interest"
        ]

        recommendation = \
            get_book_recommendation(
                interest
            )

        save_recommendation(
            interest,
            recommendation
        )

    return render_template(
        "recommend.html",
        recommendation=recommendation
    )


if __name__ == "__main__":
    app.run(
        debug=True
    )