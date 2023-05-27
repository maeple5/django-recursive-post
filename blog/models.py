from django.conf import settings
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField('タイトル', max_length=255)
    content = models.TextField('説明', blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField("投稿日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    is_updated = models.BooleanField(help_text='編集済みならTrue', default=False)
    
    class Meta:
        db_table = 'posts'
    def __str__(self):
        return f'{self.pk} {self.title}'
    
    
# class Comment(models.Model):
#     text = models.TextField('本文', blank=False)
#     commented_at = models.DateTimeField("投稿日", auto_now_add=True)
#     commented_to = models.ForeignKey(Post, verbose_name="記事", on_delete=models.CASCADE, related_name='comments')
#     commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
#                                    verbose_name="投稿者",
#                                    on_delete=models.CASCADE)
#     class Meta:
#         db_table = 'comments'
#     def __str__(self):
#         return f'{self.pk} {self.text}'
    
class Comment(models.Model):
    text = models.TextField('コメント内容')
    post = models.ForeignKey(Post, verbose_name='対象記事', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    commented_at = models.DateTimeField("投稿日", auto_now_add=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   verbose_name="投稿者",
                                   on_delete=models.CASCADE)
    updated_at = models.DateTimeField("更新日", auto_now=True)
    is_updated = models.BooleanField(help_text='編集済みならTrue', default=False)
    def __str__(self):
        return self.text[:10]
    class Meta:
        db_table = 'comments'
class Tag(models.Model):
    name = models.CharField("タグ名", max_length=32)
    posts = models.ManyToManyField(Post, related_name='tags', related_query_name='tag')
    class Meta:
        db_table = "tags"
    
    def __str__(self):
        return f'{self.pk} {self.name}'
    