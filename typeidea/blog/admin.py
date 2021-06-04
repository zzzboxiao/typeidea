from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin



class PostInline(admin.TabularInline):
  fields = ('title', 'desc')
  model = Post  # 文章组件内联
  extra = 1  # 控制额外多几个


@admin.register(Category,site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
  inlines = [PostInline,]
  list_display = ('name','status','is_nav','created_time','post_count')
  fields = ('name','status','is_nav')

  def post_count(self, obj):
    return obj.post_set.count()

  post_count.short_description = '文章数量'
  


@admin.register(Tag,site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name','status','created_time')
    fields = ('name','status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    # 自定义过滤器只展示当前用户分类
    title = '分类过滤器'
    parameter_name = "owner_category"

    # 返回要展示的内容和查询用的 id (就是上面Query 用的)
    def lookups(self, request, model_admin):
      return Category.objects.filter(owner=request.user).values_list('id','name')

    """
      根据 URL Query 的内容返回列表页数据。比如如果 URL 最后的 Query 是 ?owner_category=1,
      那么这里拿到的 self.value() 就是 1，此时就会根据 1 来过滤 QuerySet。这里的 QuerySet 是
      列表页所有展示数据的合集，即 post 的数据集
    """
    def queryset(self, request, queryset):
      category_id = self.value()
      if category_id:
        return queryset.filter(category_id=self.value())
      return queryset


  
@admin.register(Post,site=custom_site)
class PostAdmin(BaseOwnerAdmin):
  form = PostAdminForm
  list_display = [
    'title','category','status','created_time','owner','operator'
  ]
  list_display_links = []
  list_filter = [CategoryOwnerFilter,]
  search_fields = ['title', 'category__name']

  actions_on_top = True
  actions_on_bottom = True

  # 编辑页面(保存和编辑按钮),是否显示在顶部
  # save_on_top = True

  # 通过 exclude 可以指定哪些字段不展示
  exclude = ('owner',)

  # fields = (
  #   ('category','title'),
  #   'desc',
  #   'status',
  #   'content',
  #   'tag'
  # )

  fieldsets = (
      ('基础配置', {
          # "description": "基础配置描述",
          "fields": (
              ('category','title'),
              'status'
          ),
      }),
      ('内容', {
          "fields": (
              'desc',
              'content'
          ),
      }),
      ('额外信息', {
          "classes": ('collapse',),
          "fields": (
              ('tag',),
          ),
      }),
  )

  filter_vertical = ('tag',)
  # filter_horizontal = ('tag',)
  

  def operator(self, obj):
    return format_html(
      '<a herf="{}">编辑</a>',reverse('cus_admin:blog_post_change',args=(obj.id,))
    )

  operator.short_description = '操作'

  # class Media:
  #   css = {
  #     'all': ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',)
  #   }
  #   js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js')



# 后台管理查看操作日志
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
  list_display = ['object_repr','object_id','action_flag','user','change_message']
