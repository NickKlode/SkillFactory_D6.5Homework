from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField(default=0)
    
    def update_rating(self):
        postRat = self.post_set.all().aggregate(postSumRat=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postSumRat')
        
        commentRat = self.authorUser.comment_set.all().aggregate(comSumRat=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('comSumRat')
        
        self.authorRating = pRat * 3 + cRat
        self.save()
    
    def __str__(self):
        return f'{self.authorUser.username}({self.authorUser.first_name})'

class Category(models.Model):
    nameCategory = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User)
    
    
    def __str__(self):
        return self.nameCategory

class Post(models.Model):
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    choiceCategory = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postTitle = models.CharField(max_length=64)
    postText = models.TextField()
    postRating = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return self.postTitle
    
    def like(self):
        self.postRating += 1
        self.save()
        
    def dislike(self):
        self.postRating -= 1
        self.save()
    
    def preview(self):
        return self.postText[0:124] + '...'
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'Post-{self.pk}')
    
    

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categotyThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.postThrough.postTitle}({self.categotyThrough.nameCategory})'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return f'{self.commentUser.username}({self.commentUser.first_name})'
    
    def like(self):
        self.commentRating += 1
        self.save()
        
    def dislike(self):
        self.commentRating -= 1
        self.save()