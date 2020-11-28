from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
# Create your models here.

class Category(models.Model):
    created_at = models.DateTimeField(default=timezone.now,verbose_name="date created")
    title = models.CharField(max_length=250, verbose_name="title")
    
    class Meta:
        verbose_name="Category"
        verbose_name_plural = "Categories"
        ordering = ["title"]
        
    def __str__(self):
        return self.title
    
class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name="category", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="title")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="date published")
    last_modified = models.DateTimeField(default=timezone.now, verbose_name="last modified")
    #I did not setup any auth for users so the author will just be a name, this can be a foreign key on the user field
    author = models.CharField(max_length=250, verbose_name="author")
    content = models.TextField(verbose_name="content")
    comment_count = models.IntegerField(default=0,verbose_name="comment count")
    slug = models.SlugField(null=True , blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        #If this was a multiuser blog, would have added arandom string to the 
        #slug to avoid clashing of names i.e same titles will have different slugs
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        
    def get_absolute_url(self):       
        kwargs = {
            "year": "%04d" % self.published_date.year,
            "month": "%02d" % self.published_date.month,
            "day": "%02d" % self.published_date.day,
            "slug": self.slug
        }

        return reverse("post-detail", kwargs=kwargs)
    
    class Meta:
        verbose_name ="Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_date"]
           
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", 
                             verbose_name="post", 
                             on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now,
                                       verbose_name="comment date")
    author  = models.CharField(max_length=250, default="anonymous", verbose_name="author name")
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"