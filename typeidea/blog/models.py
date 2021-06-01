from django.db import models
from django.contrib.auth.models import User




class Category(models.Model):
  STATUS_NORMAL = 1
  STATUS_DELETE = 0

  STATUS_ITEMS = (
    (STATUS_NORMAL, '正常'),
    (STATUS_DELETE, '删除')
  )

  name = models.CharField(max_length=50,verbose_name='名称')
  status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
  is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
  owner = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE) # 删除关联数据,与之关联也删除
  created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

  class Meta:
    verbose_name = verbose_name_plural = '分类'

  def __str__(self):
    return self.name

  @classmethod
  def get_navs(cls):
    categories = cls.objects.filter(status=cls.STATUS_NORMAL)
    nav_categories = []
    normal_categories = []
    for cate in categories:
      if cate.is_nav:
        nav_categories.append(cate)
      else:
        normal_categories.append(cate)
    return {
      'navs': nav_categories,
      'categories': normal_categories
    }



class Tag(models.Model):
  STATUS_NORMAL = 1
  STATUS_DELETE = 0

  STATUS_ITEMS = (
    (STATUS_NORMAL, '正常'),
    (STATUS_DELETE, '删除')
  )

  name = models.CharField(max_length=10,verbose_name='名称')
  status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
  owner = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE) # 删除关联数据,与之关联也删除
  created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')

  class Meta:
    verbose_name = verbose_name_plural = '标签'

  def __str__(self):
    return self.name
  

class Post(models.Model):
  STATUS_NORMAL = 1
  STATUS_DELETE = 0
  STATUS_DRAFT = 2
  STATUS_ITEMS = (
    (STATUS_NORMAL, '正常'),
    (STATUS_DELETE, '删除'),
    (STATUS_DRAFT, '草稿')
  )

  title = models.CharField(max_length=255, verbose_name='标题')
  desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
  content = models.TextField(verbose_name='正文', help_text='正文必须为 MarkDown 格式')
  status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
  category = models.ForeignKey(Category, verbose_name='分类',on_delete=models.CASCADE) # 删除关联数据,与之关联也删除
  tag = models.ManyToManyField(Tag, verbose_name='标签')
  owner = models.ForeignKey(User, verbose_name='作者',on_delete=models.CASCADE) # 删除关联数据,与之关联也删除
  created_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
  pv = models.PositiveIntegerField(default=1)
  uv = models.PositiveIntegerField(default=1)
  
  class Meta:
    ordering = ['-id']
    verbose_name = verbose_name_plural = '文章'

  def __str__(self):
    return self.title

    """

      关联管理器(对象调用):
      多对多: 双向均有关联管理器
      一对多: 只有多的那个类的对象有关联管理器，即反向才有

      正向查询: 属性名,             从主键表,去查询外键表(ManyToManyField或ForeignKey定义的Model类)或者表本身的数据
      反向查询: 小写类名加 _set      从外键表去查询主键表

      一对一的反向, 用 对象.小写类名 即可, 不用加 _set
    """

  # @staticmethod 该方法声明为静态方法,从而可以实现无需实例化即可调用
  # 使用 @staticmethod 后, 不需要在添加实例化  def get_by_tag(self, tag_id):
  @staticmethod
  def get_by_tag(tag_id):
    try:
      tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
      tag = None
      post_list = []
    else:
      """
      反向查询, Tag 表 和 Post 表示多对多的关系，查询所有 Tag 是 tag ，同时状态为正常的文章
      Post 主键表    Tag  外键表
      class Post:
        ......
        tag = models.ManyToManyField(Tag, verbose_name='标签')
        ......

        使用select_related()方法一次性的把“表关联的对象”都查询出来放入对象中，再次查询时就不需要再连接数据库，节省了后面查询数据库的次数和时间。
      """
      post_list = tag.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
    return post_list, tag

  @staticmethod
  def get_by_category(category_id):
    try:
      category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
      category = None
      post_list = []
    else:
      # select_related()的作用: post_list[0].owner.username
      post_list = category.post_set.filter(status=Post.STATUS_NORMAL).select_related('owner','category')
    return post_list, category

  @classmethod
  def latest_posts(cls):
    queryset = cls.objects.filter(status=cls.STATUS_NORMAL)

  @classmethod
  def hot_posts(cls):
    return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')