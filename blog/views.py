from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .models import Post, Comment

# コメント、返信フォーム
CommentForm = forms.modelform_factory(Comment, fields=('text', ))


class PostList(generic.ListView):
    """記事一覧"""
    model = Post


class PostDetail(generic.DetailView):
    """記事詳細"""
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # どのコメントにも紐づかないコメント=記事自体へのコメント を取得する
        context['comment_list'] = self.object.comment_set.filter(parent__isnull=True)
        return context


def comment_create(request, post_pk):
    """記事へのコメント作成"""
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        comment = form.save(commit=False)
        comment.post = post
        comment.commented_by = request.user
        comment.save()
        return redirect('blog:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'blog/comment_form.html', context)


def reply_create(request, comment_pk):
    """コメントへの返信"""
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        reply = form.save(commit=False)
        reply.parent = comment
        reply.post = post
        reply.commented_by = request.user
        reply.save()
        return redirect('blog:post_detail', pk=post.pk)

    context = {
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request, 'blog/comment_form.html', context)

# from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
# from blog.models import Snippet, Comment
from blog.forms import PostForm, CommentForm
from django.views.decorators.http import require_safe, require_http_methods, require_GET
# from django.http import JsonResponse
# from django.template.response import TemplateResponse
from urllib.parse import quote
# # Create your views here.

@require_safe
def top(request):
    posts = Post.objects.all()
    context = {"posts": posts}
    return render(request, "blog/top.html", context) 
# def top(request):
#     return HttpResponse(b"Hello World")

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid(): 
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_new.html", {'form': form})
    # return HttpResponse("スニペットの登録")

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.created_by_id != request.user.id:
        return HttpResponseForbidden("この記事の編集は許可されていません")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            post.is_updated = True
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form})
@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.commented_by_id != request.user.id:
        return HttpResponseForbidden("このコメントの編集は許可されていません")
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            comment.is_updated = True
            comment.save()
            return redirect('blog:post_detail', pk=comment.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, "blog/comment_edit.html", {'form': form})
    # return HttpResponse("スニペットの編集")

# @require_safe
# def post_detail(request, post_id, comments):
#     post = get_object_or_404(Post, pk=post_id)
#     context = {'post': post, 'comment_form': CommentForm, 'comments': comments}
#     return render(request, 'blog/post_detail.html', context)
# @require_safe
# def snippet_detail(request, snippet_id):
#     try:
#         snippet = Snippet.objects.get(id=snippet_id)
#     except Snippet.DoesNotExist:
#         return HttpResponseNotFound("Snippet is not found")
#     return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})
# @login_required
# @require_http_methods(["GET", "POST", "HEAD"])
# def comment_new(request, post_id):
#     if request.method == 'POST':
#         post = get_object_or_404(Post, pk=post_id)
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.commented_by = request.user
#             # comment.commented_to = post
#             comment.save()
#             # comments = Comment.objects.filter(commented_to=target_snippet)
#             # context = { 'comments': comments }
#             return redirect('blog:post_detail', post_id=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, "blog/comment_new.html", {'form': form})

# @require_safe
# def comment_detail(request, snippet_id, comment_id):
#     comment = get_object_or_404(Comment, pk=comment_id)
#     context = {'comment': comment}
#     return render(request, 'snippets/comment_detail.html', context)

# def snippet_list_api(request):
#     snippets = Snippet.objects.all()
#     return JsonResponse({"snippets": snippets})


# @require_GET
# def hello(request):
#     context = {'username': 'c-bata'}
#     return TemplateResponse(request, 'hello.html', context)
# def hello(request):
#     if request.method != "GET":
#         # GETメソッド以外は、405 Method Not Allowedを返す。
#         response = HttpResponseNotAllowed(["GET"])
#         return response
#     context = {'username': 'c-bata'}
#     return TemplateResponse(request, 'hello.html', context)

# def hello(request):
#     response = HttpResponse(b"Hello World", status=200)
#     response['Cache-Control'] = 'max-age=3600' # ヘッダーのセット
#     return response

def handler400(request, exception):
    return render(request, 'errors/400.html', {}, status=400)
def handler403(request, exception):
    return render(request, 'errors/403.html', {}, status=403)
def handler404(request, exception):
    context = {"request_path": quote(request.path)}
    return render(request, 'errors/404.html', context, status=404)
def handler500(request):
    return render(request, 'errors/500.html', {}, status=500)