import sqlite3

conn = sqlite3.connect('street.db')

cur = conn.cursor()

cur.execute('''

CREATE TABLE user (
    user_id INTEGER NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    levels INTEGER NOT NULL,
    is_verified BOOLEAN NOT NULL,
    profile_picture TEXT NOT NULL,
    PRIMARY KEY (user_id)
    );
''')

cur.execute('''

CREATE TABLE post (

    post_id INTEGER NOT NULL,
    author INTEGER NOT NULL,
    location STRING NOT NULL,
    title STRING NOT NULL,
    description STRING NOT NULL,
    image STRING NOT NULL,
    rating INTEGER NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (author_id) REFERENCES user (user_id)
    );
''')

cur.execute('''

CREATE TABLE comments (
    comment_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    author INTEGER NOT NULL,
    comment STRING NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES post (post_id),
    FOREIGN KEY (author) REFERENCES post (user_id)
    );
''')    

cur.execute('''

CREATE TABLE post_ratings (
    rating_id INTEGER NOT NULL,
    user INTEGER NOT NULL,
    post INTEGER  NOT NULL,
    rating INTEGER NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (user) REFERENCES user (user_id),
    FOREIGN KEY (post) REFERENCES post (post_id)
    );
''')      
    

    
 
while True:
    row = cur.fetchone()
    if not row:
        break
    print(row)
    
conn.commit()
    
conn.close()