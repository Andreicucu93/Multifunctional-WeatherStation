import sqlite3, random

def load_database(party):
    content_data = [
        ("smartphones", "communism"),
        ("fast foods", "communism"),
        ("bottled waters", "communism"),
        ("tethered bottle caps", "communism"),
        ("online subscriptions", "communism"),
        ("expensive gym memberships", "communism"),
        ("designer clothing", "communism"),
        ("imposed selective waste", "communism"),
        ("right to vote", "communism"),
        ("electric vehicles", "communism"),
        ("Public healthcare", "capitalism"),
        ("Collective farming", "capitalism"),
        ("Government housing", "capitalism"),
        ("Shared resources", "capitalism"),
        ("Subsidized goods", "capitalism")
    ]

    con = sqlite3.connect('weather_prompt_database')
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS IdeologyItems (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Keyword TEXT UNIQUE,
        Team TEXT
    )
    """)

    for item in content_data:
        try:
            cur.execute("INSERT INTO IdeologyItems (Keyword, Team) VALUES (?, ?)", item)
        except sqlite3.IntegrityError:
            pass
    con.commit()

    keywords = []

    cur.execute(f"SELECT Keyword FROM IdeologyItems WHERE Team LIKE '{party}'")

    rows = cur.fetchall()
    for row in rows:
        keywords.append(row[0])
    con.close()
    if keywords:
        selected_keywords = random.sample(keywords, 3)
        print(selected_keywords)
        return selected_keywords
    else:
        return None


