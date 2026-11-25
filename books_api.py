import sqlite3
import sys
import time

import requests

query = sys.argv[1] if len(sys.argv) > 1 else "python programming"

# open library search api, its free and doesnt need a key
url = "https://openlibrary.org/search.json"
params = {"q": query, "limit": 15, "fields": "title,author_name,first_publish_year"}

# open library is slow and resets the connection sometimes, so 30 sec timeout and 3 tries
for attempt in range(3):
    try:
        res = requests.get(url, params=params, timeout=30)
        res.raise_for_status()
        break
    except requests.RequestException as e:
        print(f"try {attempt + 1} failed: {e}")
        time.sleep(2)
else:
    sys.exit("could not reach open library, try again in a bit")

docs = res.json()["docs"]

conn = sqlite3.connect("books.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    publication_year INTEGER,
    UNIQUE(title, author)
)
""")

added = 0
for doc in docs:
    title = doc.get("title")
    if not title:
        continue
    author = ", ".join(doc.get("author_name", [])[:2]) or "Unknown"
    year = doc.get("first_publish_year")

    cur.execute("INSERT OR IGNORE INTO books (title, author, publication_year) VALUES (?, ?, ?)",
                (title.strip(), author, year))
    added += cur.rowcount

conn.commit()
print(f"got {len(docs)} books from the api, {added} new ones saved in books.db\n")

for book_id, title, author, year in cur.execute("SELECT * FROM books ORDER BY publication_year DESC"):
    print(f"{year} | {title} | {author}")

conn.close()
