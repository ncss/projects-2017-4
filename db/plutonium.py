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
        print('User has been logged in.')
        return User()
    
    def register( email, password, displayname ):
        '''
        Registers a new user given an email address, password, and display name.
        '''
        print('New user registered.')
        return User()
        
    def get( email ):
        '''
        Gets a user object given an email.
        '''
        print('Obtained user.')
        return User()
        
    def edit_displayname( self, newname ):
        '''
        Changes the displayname of a user class.
        '''
        self.displayname = newname
        
    # TODO: Functions for verified status and title management
        
class Post:
    def __init__(self):
        self.title = 'James Curran Is The Best'
        self.content = 'James Curran is an Associate Professor and ARC Australian Research Fellow at the University of Sydney and the Research Leader in Language Technology at the Capital Markets Cooperative Research Centre.'
        self.author = 'james.r.curran@sydney.edu.au'
        self.image = 'jamescurran.png'
        self.location = 'James\' Secret Headquarters'
        
    def create( user, title, description, image, location ):
        print('New post created!')
        return Post()
        
    def get( postid ):
        print('Obtained post!')
        return Post()
    
    def rating( self ):
        print('Return ratings.')
        
    def comments( self ):
        print('Return comments.')

class Comment:
    def __init__(self):
        self.author = 'james.r.curran@sydney.edu.au'
        self.post = '2'
        self.content = 'I agree, James Curran IS the best!'
        print('Incredible new comment!')
        
    def create(user, postid, contents ):
        print('New comment has been created!')
        return Comment()