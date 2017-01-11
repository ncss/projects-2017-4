import sqlite3
import plutonium
import unittest
import os
from plutonium import database_connect
from plutonium import terminate_connection
from plutonium import User, Ratings, Post, Comment
from create_db import init_db

plutonium.database_connect


conn = sqlite3.connect('street.db')
cur = conn.cursor()

class Testing_plutonium(unittest.TestCase):
    def setUp(self):
        init_db( 'test.db' )
        self.conn = database_connect( 'test.db' )
        self.cur = self.conn.cursor()

    def register(self):
        self.cur.execute('SELECT 7')
        self.assertEqual( self.cur.fetchone()[0], 7 )

    def test_register(self):
        u = User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        self.assertEqual( u.username, 'James Curran' )

    def get_all(self):
        User.register( 'james.r.curran@sydney.edu.au', 'cranberry', 'James Currant' )
        with self.assertRaises( ValueError ):
            User.register( 'james.r.curran@sydney.edu.au', 'cranberry', 'James Currant' )

    def test_login(self):
        User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        u = User.login( 'james.r.curran@sydney.edu.au', 'tomtom' )
        self.assertEqual( u.username, 'James Curran' )

    def test_displayname(self):
        User.register( 'james.r.curran@sydney.edu.au', 'tomtom', 'James Curran' )
        u = User.get( 'james.r.curran@sydney.edu.au' )
        self.assertEqual( u.username, 'James Curran' )

    def test_create(self):
        u = User.register( '10@ten.com', 'testing', 'James Curran is love' )
        p = Post.create( User.get('10@ten.com').user_id, 'some random location', 'James Currans secret post', 'default.jpg', '50')
        print( p, p.author_id, User.get_by_id(p.author_id).email )
        self.assertEqual( u.username, 'James Curran is love')

    def test_create_comment(self):
        u = User.register( '10@ten.com', 'testing', 'James Curran is love' )
        p = Post.create( User.get('10@ten.com').user_id, 'some random location', 'James Currans secret post', 'default.jpg', '50')
        c = Comment.create( p.author_id, p.id, 'This is a comment.')
        self.assertEqual( c.content, 'This is a comment.')

    def test_rate(self):
        pass

    def tearDown(self):
        terminate_connection()
        os.remove( 'test.db' )

if __name__ == '__main__':
    unittest.main()
