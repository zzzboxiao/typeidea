from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView


from blog.views import CommonViewMixin
from .models import Link


class LinkListView(ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    context_object_name = 'config/links.html'
    template_name = "config/links.html"