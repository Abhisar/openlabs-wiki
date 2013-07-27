from django.db import models


class Article(models.Model):
    """
    creates a model/table articles
    """
    title = models.CharField(max_length=200)
    user = models.CharField(max_length=25)
    flag = models.CharField(max_length=6)


class history(models.Model):
    """
    Creates a model to track history of files
    """
    page_id = models.ForeignKey(Article)
    content = models.TextField()
    edited = models.DateTimeField(auto_now_add=True)
    edited_by = models.CharField(max_length=25)


class Document(models.Model):
    imagefile = models.ImageField(upload_to='documents/%Y/%m/%d')

    
    def __unicode__(self):
        """
        Will call the __unicode__ method of the User class and  to give
        an object a readable name
        """
        return self.title
