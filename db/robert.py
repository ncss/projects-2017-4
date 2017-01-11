from hashlib import sha512
import sqlite3

conn = sqlite3.connect('db/street.db')
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
    
    def get_posts( self ):
        '''
        Returns a list of all the post objects that the user has made
        '''
        print( 'Post objects.' )
    
    def rate( self, post, rating ):
        '''
        Gets the user to vote on a given post object
        Rating should be -1, 0, or 1
        '''
        print( 'Vote cast!' )
    
    # TODO: Functions for verified status and title management
