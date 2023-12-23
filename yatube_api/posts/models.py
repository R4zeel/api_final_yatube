from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    # тут сначала пытался задать группу явно при отстутствующих данных
    # о группе в POST запросе, но у меня не получилось это сделать 
    # через сериализатор + подумал, что хардкодить номер группы 
    # совсем некорректно. Пока лучшего решения, чем добавить 
    # null=true в поле модели не нашёл
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='posts', null=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Group(models.Model):
    title = models.CharField(max_length=16)
    description = models.TextField()
    slug = models.SlugField()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
