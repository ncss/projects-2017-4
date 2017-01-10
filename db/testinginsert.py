cur.execute('''

INSERT INTO user VALUES (           0, 'password0', 'test0@email.com', 'username_poster', '0', '1', 'test.jpg');
INSERT INTO user VALUES (           1, 'password1', 'test1@email.com', 'username_commenter', '0', '1', 'test.jpg');


INSERT INTO post VALUES (           0, 'username', 'University of Sydney', 'Test_post', 'Insert a description in here', 'test_post.jpg', '137');
    
INSERT INTO comments VALUES (           0, '0', '1', 'This post is awesome');
    
INSERT INTO post_ratings VALUES (           0, '1', '0', '1');    


SELECT *
FROM user;

''') 