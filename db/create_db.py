import sqlite3

def init_db( filename ):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        levels INTEGER NOT NULL,
        is_verified BOOLEAN NOT NULL,
        profile_picture TEXT NOT NULL,
        description TEXT NOT NULL
        );
    ''')

    cur.execute('''

    CREATE TABLE post (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_id INTEGER NOT NULL,
        location STRING NOT NULL,
        title STRING NOT NULL,
        description STRING NOT NULL,
        image STRING NOT NULL,
        rating INTEGER NOT NULL,
        FOREIGN KEY (author_id) REFERENCES user (user_id)
        );
    ''')

    cur.execute('''

    CREATE TABLE comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author INTEGER NOT NULL,
        comment STRING NOT NULL,
        FOREIGN KEY (post_id) REFERENCES post (post_id),
        FOREIGN KEY (author) REFERENCES post (user_id)
        );
    ''')

    cur.execute('''

    CREATE TABLE post_ratings (
        rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user INTEGER NOT NULL,
        post INTEGER  NOT NULL,
        rating INTEGER NOT NULL,
        FOREIGN KEY (user) REFERENCES user (user_id),
        FOREIGN KEY (post) REFERENCES post (post_id)
        );
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db( 'street.db' )
