from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse
from .models import Play

@login_required
def graph(request):
    return render(request, 'blog/graph.html')

@login_required
def play_count_by_month(request):
    data = Play.objects.all() \
        .extra(select={'month': connections[Play.objects.db].ops.date_trunc_sql('month', 'date')}) \
        .values('month') \
        .annotate(count_items=Count('id'))
    return JsonResponse(list(data), safe=False)

@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
