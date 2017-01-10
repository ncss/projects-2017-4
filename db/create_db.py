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
    
CREATE TABLE comments (
    comment_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    author INTEGER NOT NULL,
    comment STRING NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES post (post_id),
    FOREIGN KEY (author) REFERENCES post (user_id)
    );
    
CREATE TABLE post_ratings (
    rating_id INTEGER NOT NULL,
    user INTEGER NOT NULL,
    post INTEGER  NOT NULL,
    rating INTEGER NOT NULL,
    PRIMARY KEY (rating_id),
    FOREIGN KEY (user) REFERENCES user (user_id),
    FOREIGN KEY (post) REFERENCES post (post_id)
    );

    
INSERT INTO user VALUES (           0, 'password0', 'test0@email.com', 'username_poster', '0', '1', 'test.jpg');
INSERT INTO user VALUES (           1, 'password1', 'test1@email.com', 'username_commenter', '0', '1', 'test.jpg');


INSERT INTO post VALUES (           0, 'username', 'University of Sydney', 'Test_post', 'Insert a description in here', 'test_post.jpg', '137');
    
INSERT INTO comments VALUES (           0, '0', '1', 'This post is awesome');
    
INSERT INTO post_ratings VALUES (           0, '1', '0', '1');    


SELECT *
FROM user;


''')

'''
while True:
    row = cur.fetchone()
    if not row:
        break
    print(row)
'''
    
conn.close()