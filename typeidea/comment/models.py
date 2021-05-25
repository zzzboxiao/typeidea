from django.db import models
from blog.models import Post



class Comment(models.Model):
  STATUS_NORMAL = 1
  STATUS_DELETE = 0

  STATUS_ITEMS = (
    (STATUS_NORMAL, '正常'),
    (STATUS_DELETE, '删除')
  )
  target = models.ForeignKey(Post, verbose_name='评论目标',on_delete=models.CASCADE) # 删除关联数据,与之关联也删除
  content = models.CharField(max_length=2000, verbose_name='内容')
  nickname = models.CharField(max_length=50, verbose_name='昵称')
  website = models.URLField(max_length=200, verbose_name='网站')
  email = models.EmailField(max_length=254, verbose_name='邮箱')
  status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
  created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

  class Meta:
    verbose_name = verbose_name_plural = '评论'

