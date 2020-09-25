from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    body = models.TextField()
    who_created = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_created")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.body} by {self.who_created}"

class Like(models.Model): 
    who_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_liked")
    what_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="what_post")

    def __str__(self):
        return f"{self.who_liked} liked {self.what_post}"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    is_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="is_following")

    def __str__(self):
        return f"{self.follower} is following {self.is_following}"
