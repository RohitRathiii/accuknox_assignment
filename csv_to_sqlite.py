import csv
import re
import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

inserted = 0
duplicates = 0
invalid = []

with open("users.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = (row["name"] or "").strip()
        email = (row["email"] or "").strip().lower()

        if not name or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            invalid.append(reader.line_num)
            continue

        # using ? so names with quotes or sql in them cant break the query
        cur.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)", (name, email))
        if cur.rowcount == 1:
            inserted += 1
        else:
            duplicates += 1

conn.commit()

print(f"rows in csv: {inserted + duplicates + len(invalid)}")
print(f"inserted: {inserted}")
print(f"duplicate emails skipped: {duplicates}")
print(f"invalid rows skipped: {len(invalid)} (lines {invalid})\n")

for row in cur.execute("SELECT id, name, email FROM users"):
    print(row)

conn.close()
