from django.db import models
from django.contrib.auth.models import User  # import User for BlogComment
from django.utils.timezone import now        # import now for timestamp BlogComment

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=15)
    slug = models.CharField(max_length=130)
    timeStamp = models.DateTimeField(blank=True)
    

    # In database if we want to see name or email id of user who has sent message.
    def __str__(self):
        return self.title + ' by ' + self.author

# BlogComment will be associated with 'user' as well as with 'post'.
class BlogComment(models.Model):   
    sno = models.AutoField(primary_key=True)  
    comment = models.TextField()
    # 'models.ForeignKey' <-- will point to the record of the Post, and same goes with post.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''on_delete=models.CASCADE' <-- means if the Post is deleted on which comment is added,
      then comment will also get deleted.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    '''models.ForeignKey' <-- it would be pointing to self only
       ie. 'parent' will point to any post of 'BlogComment' Model and also we are going to allow 'null' values.'''
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + " by " + self.user.username
    