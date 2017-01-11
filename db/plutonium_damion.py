from hashlib import sha512
import sqlite3

conn = sqlite3.connect('street.db')
cur = conn.cursor()

def database_connect():
    if conn is None:
        conn = sqlite3.connect('street.db')
        cur = conn.cursor()

    return conn

def hash_password( email, password ):
    '''
    This function is used to salt and hash passwords
    Uses strong recent hashing algorithms + salts to ensure
    that our users are secure at all times.

    Email address is used as a salt.
    '''
    string = email + password
    h = sha512()
    h.update( string.encode() )
    return h.hexdigest()

class Post:
    def __init__(self, post_id, author_id, location, title, description, image, rating):
        self.id = post_id
        self.author_id = author_id
        self.location = location
        self.title = title
        self.description = description
        self.image = image

        #self.rating = Rating.post_rating(post_id) #TODO: UNCOMMENT THIS!!!

    def create( user, title, description, image, location ):
        '''
        Creates a new post given the user object, title, description, image, and location.
        '''
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO post (author_id, location, title, description, image, rating)
        VALUES (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
        )""", (
        user,
        location,
        title,
        description,
        image,
        0 #TODO: Calculate from ratings table
        ))
        conn.commit()
        print( '[Post.create]' )
        post_id = cur.lastrowid
        rating = 0 # Initial value of the rating column
        return Post(post_id, user, location, title, description, image, rating)

    def get( postid ):
        '''
        Returns a post object given a postid
        '''
        cur = conn.cursor()
        cur.execute("""
        SELECT *
        FROM post
        WHERE post_id = ?
        """, (
        postid,
        ))
        response = cur.fetchone()
        print( '[Post.get] post_id:', postid ) #self, post_id, author_id, location, title, description, image
        return Post(postid, response[1], response[2], response[3], response[4], response[5], response[6])

    def get_all():
        '''
        Returns a list containing every post object
        NOTE: This can be large - be careful
        '''

        cur = conn.cursor()
        cur.execute("""
        SELECT *
        FROM post
        ORDER BY post_id DESC
        """)

        postsArr = []

        for row in cur:
            postsArr.append(Post(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) #self, post_id, author_id, location, title, description, image

        print( '[Post.get_all]' )

        return postsArr

    def get_by_recent( amount ):
        '''
        Returns some of the most recent posts created
        '''
        print( 'Most recent posts' )

    def get_by_location( location, amount ):
        '''
        Returns some of the nearest posts
        '''
        print( 'Nearby posts' )

    def rating( self ):
        '''
        Returns the rating of a post.
        '''
        print( 'Return ratings.' )

    def comments( self ):
        '''
        Returns a list of all the comments on the post
        '''
        print( 'Return comments.' )

class Comment:
    def __init__(self, comment_id, author, post, content):
        self.comment_id = comment_id
        self.author = author
        self.post = post
        self.content = content
        print( 'Incredible new comment!' )

    def create(user_id, postid, contents ):
        '''
        Given a user object, a post object, and a string
        creates a new comment on the specified post
        '''


        cur = conn.execute('''

        INSERT INTO comments (post_id, author, comment) VALUES (?, ?, ?);

        ''', (postid, user_id, contents))
        print( 'New comment has been created!' )
        return Comment()

class Ratings:
    def __init__(self):
        print('post ratings')


    def create(rating_id, user, post, rating):
        '''
        This area ensures that a used doesn't upvote/downvote more than once,
        and the 'rating' column is a 'boolean' (not really), indicating weather
        is a user has rated
        '''
        pass
