from hashlib import sha512
import sqlite3

conn = sqlite3.connect('street.db')
cur = conn.cursor()

def database_connect():
    if conn is None:
        conn = sqlite3.connect('db/street.db')
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

class User:
    '''
    User Object
    '''
    def __init__(self, email, username, level, is_verified, profile_picture ):
        self.email = email
        self.username = username
        self.level = level
        self.is_verifed = is_verified
        self.profile_picture = profile_picture

    @staticmethod
    def login( email, password ):
        '''
        Given an email address and an unhashed password
        Will return a User object if valid login
        Will throw error if invalid login
        '''
        c = conn.cursor()
        password = hash_password( email, password )
        # Ensure that the user is in the database
        c.execute('SELECT * FROM user WHERE email = ?;', (email,) )
        data = c.fetchone()
        if data is None:
            raise ValueError("User is not in database")
        else:
            storedhash = data[1]
            # Hash the given password and compare it to the storedhash
            if password == storedhash:
                return User( data[2], data[3], data[4], data[5], data[6] )
            else:
                raise ValueError("Passwords do not match")

    @staticmethod
    def register( email, password, username ):
        '''
        Given the required data, registers an account in the database
        Will return False if the account does not meet registration requirements
        '''
        c = conn.cursor()
        # Check that the email is not currently in the database
        c.execute('SELECT email FROM user WHERE email = ?;', (email,) )
        if len( c.fetchall() ) > 0:
            return ValueError("User is already in database")
        else:
            password = hash_password( email, password )
            c.execute('INSERT INTO user (password, email, username, levels, is_verified, profile_picture) VALUES(?, ?, ?, ?, ?, ?);', (password, email, username, 0, 0, 'default.png') )
            conn.commit()
            return User( email, username, 0, 0, 'default.png' )

    @staticmethod
    def get( email ):
        '''
        Gets a user object given an email.
        '''
        c = conn.cursor()
        c.execute('SELECT * FROM user WHERE email = ?;', (email,) )
        data = c.fetchone()
        if data is None:
            raise ValueError("User is not in database")
        else:
            return User( data[2], data[3], data[4], data[5], data[6] )

    @staticmethod
    def get_all():
        '''
        Returns a list of all the users
        NOTE: This can be large - be careful
        '''
        users = []
        c = conn.cursor()
        c.execute('SELECT * FROM user')
        for each in c.fetchall():
            users.append( each )
        return users

    def edit_displayname( self, newname ):
        '''
        Changes the displayname of a user class.
        '''
        self.displayname = newname
        print( 'Display name updated.' )

    def get_posts( user_id ):
        '''
        Returns a list of all the post objects that the user has made
        '''
        posts = []

        cur = conn.cursor()
        cur.execute("""
        SELECT *
        FROM post
        WHERE author_id = ?
        """, (
        user_id,
        ))

        print( 'Post objects.' )
        for post in cur:
            posts.append(Post(post[0], post[1], post[2], post[3], post[4], post[5], post[6]))

        return posts

    def rate( self, post, rating ):
        '''
        Gets the user to vote on a given post object
        Rating should be -1, 0, or 1
        '''
        print( 'Vote cast!' )

    # TODO: Functions for verified status and title management

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

        posts = []

        for row in cur:
            posts.append(Post(row[0], row[1], row[2], row[3], row[4], row[5], row[6])) #self, post_id, author_id, location, title, description, image

        print( '[Post.get_all]' )

        return posts

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
