# AccuKnox assignment, problem statement 1

Python 3.8 or newer. Install the libraries first:

    pip install -r requirements.txt

Run everything from inside this folder.

## 1. Books API to SQLite

    python books_api.py

Fetches books from the Open Library search API, saves title, author and publication year in books.db and prints them. You can pass your own search term too, eg `python books_api.py "machine learning"`. Running it again wont add the same books twice.

## 2. Student scores, average and bar chart

No API was given for this one so mock_api.py serves students.json with Flask. Start it in one terminal:

    python mock_api.py

and run this in another one:

    python student_scores.py

It prints each student's average, the subject averages and the class average, and saves the bar chart as scores_chart.png.

## 3. CSV to SQLite

    python csv_to_sqlite.py

Reads users.csv and inserts the users into users.db. Invalid rows (no name or bad email) and duplicate emails are skipped and counted.
