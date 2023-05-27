from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseNotAllowed
from snippets.models import Snippet, Comment
from snippets.forms import SnippetForm, CommentForm
from django.views.decorators.http import require_safe, require_http_methods, require_GET
from django.http import JsonResponse
from django.template.response import TemplateResponse
from urllib.parse import quote
# Create your views here.

@require_safe
def top(request):
    snippets = Snippet.objects.all()
    context = {"snippets": snippets}
    return render(request, "snippets/top.html", context) 
# def top(request):
#     return HttpResponse(b"Hello World")

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm()
    return render(request, "snippets/snippet_new.html", {'form': form})
    # return HttpResponse("スニペットの登録")

@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden("このスニペットの編集は許可されていません")
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect(snippet_detail, snippet_id=snippet.pk)
    else:
        form = SnippetForm(instance=snippet)
    return render(request, "snippets/snippet_edit.html", {'form': form})
    # return HttpResponse("スニペットの編集")

@require_safe
def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    context = {'snippet': snippet, 'comment_form': CommentForm}
    return render(request, 'snippets/snippet_detail.html', context)
# @require_safe
# def snippet_detail(request, snippet_id):
#     try:
#         snippet = Snippet.objects.get(id=snippet_id)
#     except Snippet.DoesNotExist:
#         return HttpResponseNotFound("Snippet is not found")
#     return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})
@login_required
@require_http_methods(["GET", "POST", "HEAD"])
def comment_new(request, snippet_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            target_snippet = Snippet.objects.get(id=snippet_id)
            comment = form.save(commit=False)
            comment.commented_by = request.user
            comment.commented_to = target_snippet
            comment.save()
            # comments = Comment.objects.filter(commented_to=target_snippet)
            # context = { 'comments': comments }
            return redirect(snippet_detail, snippet_id=snippet_id)
    else:
        form = CommentForm()
    return render(request, "snippets/comment_new.html", {'form': form})

@require_safe
def comment_detail(request, snippet_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    context = {'comment': comment}
    return render(request, 'snippets/comment_detail.html', context)

def snippet_list_api(request):
    snippets = Snippet.objects.all()
    return JsonResponse({"snippets": snippets})


@require_GET
def hello(request):
    context = {'username': 'c-bata'}
    return TemplateResponse(request, 'hello.html', context)
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