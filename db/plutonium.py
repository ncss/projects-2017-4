class User:
    '''
    User Object
    '''
    def __init__(self):
        self.email = 'james.r.curran@sydney.edu.au'
        self.displayname = 'James Curran'
        
    def login( email, password ):
        '''
        Given a email address and a password, will return the user class or False depending
        on whether or not the login was successful.
        '''
        print( 'User has been logged in.' )
        return User()
    
    def register( email, password, displayname ):
        '''
        Registers a new user given an email address, password, and display name.
        '''
        print( 'New user registered.' )
        return User()
        
    def get( email ):
        '''
        Gets a user object given an email.
        '''
        print( 'Obtained user.' )
        return User()
        
    def get_all():
        '''
        Returns a list of all the users
        NOTE: This can be large - be careful
        '''
        print( 'All users.' )
        
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
        
class Post:
    def __init__(self):
        self.title = 'James Curran Is The Best'
        self.content = 'James Curran is an Associate Professor and ARC Australian Research Fellow at the University of Sydney and the Research Leader in Language Technology at the Capital Markets Cooperative Research Centre.'
        self.author = 'james.r.curran@sydney.edu.au'
        self.image = 'jamescurran.png'
        self.location = 'James\' Secret Headquarters'
        
    def create( user, title, description, image, location ):
        '''
        Creates a new post given the user object, title, description, image, and location.
        '''
        print( 'New post created!' )
        return Post()
        
    def get( postid ):
        '''
        Returns a post object given a postid
        '''
        print( 'Obtained post!' )
        return Post()
    
    def get_all():
        '''
        Returns a list containing every post object
        NOTE: This can be large - be careful
        '''
        print( 'All the posts!' )
        
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
    def __init__(self):
        self.author = 'james.r.curran@sydney.edu.au'
        self.post = '2'
        self.content = 'I agree, James Curran IS the best!'
        print( 'Incredible new comment!' )
        
    def create(user, postid, contents ):
        '''
        Given a user object, a post object, and a string
        creates a new comment on the specified post
        '''
        print( 'New comment has been created!' )
        return Comment()