from django.contrib import admin



class BaseOwnerAdmin(admin.ModelAdmin):
  """
    1、用来自动补充文章、分类、标签、侧边栏、友链这些 Model 的 owner
    2、用来针对 queryset 过滤当前用户数据
  """
  exclude = ('owner', )


  """
  问题：防止任何作者可以随意把自己创建的内容改为本作者的
  解决：把 owner 字段设为当前的登录用户
  解析 save_model(self, request, obj, form, change)
    通过给 obj.owner 赋值，达到自动设置 owner 的目的
    request 就是当前请求，request.user 就是当前登录的用户；如果是未登录的情况下，request.user 拿到的是匿名对象
    obj 就是当前要保存的对象，而 form 是页面提交过来的表单之后的对象，change 用于标记本次保存的数据时新增的还是更新的
  """

  def save_model(self, request, obj, form, change):
    obj.owner = request.user
    return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

  def get_queryset(self, request):
    qs = super(BaseOwnerAdmin, self).get_queryset(request)
    return qs.filter(owner=request.user)

