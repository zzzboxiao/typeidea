from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView,ListView
from django.db.models import Q

from .models import Post, Tag, Category
from config.models import SideBar


"""
class-based view 的处理流程
class-based view 对外暴露的接口是 as_view
《Django企业开发实战 高效Python Web框架指南》 7.6.2总结

get_context_data 方法, 用来获取上下文数据并最终将其传入模板
get_queryset 方法, 用来获取指定 Model 或 QuerySet 的数据

"""

class CommonViewMixin:
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'sidebars': SideBar.get_all()
    })
    context.update(Category.get_navs())
    print('===>',context)
    return context
  

class IndexView(CommonViewMixin,ListView):
  queryset = Post.latest_posts()
  paginate_by = 5   # 每一页显示的文章数量
  context_object_name = 'post_list'   # 如果不设置此项, 在模板中需要使用object_list变量 
  template_name = 'blog/list.html'


class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'    # 如果不设置此项, 在模板中需要使用object_list变量
    """
      pk_url_kwarg 是 设置从URL定义中获取数据的参数名，不设置该变量，则默认为 pk, 例子如下
      url(r'^post/(?P<pk>\d+).html', PostDetailView.as_view(), name='post-detail')
      
      因此，如果要使用 pk_url_kwarg = 'post_id'，则必须将 URL 路径修改为:
      url(r'^post/(?P<post_id>\d+).html', PostDetailView.as_view(), name='post-detail')
    """
    # pk_url_kwarg = 'post_id'
    template_name = "blog/detail.html"


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    context_object_name = 'post_list'  # 如果不设置此项, 在模板中需要使用object_list变量
    template_name = "blog/list.html"


class CategoryView(IndexView):
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      category_id = self.kwargs.get('category_id')  # 从URL定义中获取数据
      category = get_object_or_404(Category, pk=category_id)
      context.update({
        'category': category
      })
      return context
  
  def get_queryset(self):
    """ 重写queryset,根据分类过滤 """
    queryset = super().get_queryset()
    category_id = self.kwargs.get('category_id') # 从URL定义中获取数据
    return queryset.filter(category_id=category_id)


class TagView(IndexView):
  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      tag_id = self.kwargs.get('tag_id')   # 从URL定义中获取数据
      tag = get_object_or_404(Tag, pk=tag_id)
      context.update({
        'tag': tag
      })
      return context
  
  def get_queryset(self):
    """ 重写queryset,根据分类过滤 """
    queryset = super().get_queryset()
    tag_id = self.kwargs.get('tag_id') # 从URL定义中获取数据
    return queryset.filter(tag_id=tag_id)
  
  
class SearchView(IndexView):
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'keyword': self.request.GET.get('keyword', '')
    })
    return context
  
  def get_queryset(self):
      queryset = super().get_queryset()
      keyword = self.request.GET.get('keyword')
      if not keyword:
        return queryset
      return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
  

class AuthorView(IndexView):
  def get_queryset(self):
      queryset = super().get_queryset()
      author_id = self.kwargs.get('owner_id')
      return queryset.filter(owner__id=author_id)
    




"""
def post_list(request, category_id=None, tag_id=None):
  tag = None
  category = None
  if tag_id:
    post_list, tag = Post.get_by_tag(tag_id)
  elif category_id:
    post_list, category = Post.get_by_category(category_id)
  else:
    post_list = Post.latest_posts()

  context = {
    'category': category,
    'tag': tag,
    'post_list': post_list,
    'sidebars': SideBar.get_all()
  }
  context.update(Category.get_navs())
  return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
  try:
    post = Post.objects.get(id=post_id)
  except Post.DoesNotExist:
    post = None
  context = {
    'post': post,
    'sidebars': SideBar.get_all()
  }
  context.update(Category.get_navs())
  return render(request, 'blog/detail.html', context=context)
"""