from django.contrib.auth import get_user_model

from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest
from django.urls import resolve
from blog.views import top, post_new, post_edit, PostDetail
from blog.models import Post


UserModel = get_user_model()
# Create your tests here.

class TopPageTest(TestCase):
    def test_top_page_returns_200_and_expected_title(self):
        response = self.client.get("/")
        self.assertContains(response, "ようこそMaeplegoへ", status_code=200)

    def test_top_page_uses_expected_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blog/top.html")

class TopPageRenderPostsTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="top_secret_pass0001",
        )
        self.post = Post.objects.create(
            title="title1",
            content="content1",
            created_by=self.user,
        )
    def test_should_return_post_title(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.post.title)
    def test_should_return_screen_user_id(self):
        request = RequestFactory().get("/")
        request.user = self.user
        response = top(request)
        self.assertContains(response, self.user.username)
class PostDetailTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.post = Post.objects.create(
            title="タイトル",
            content="内容",
            created_by=self.user,
        )
    def test_should_use_expected_template(self):
        response = self.client.get("/posts/detail/%s/" % self.post.id)
        self.assertTemplateUsed(response, "blog/post_detail.html")
        
    def test_top_page_returns_200_and_expected_heading(self):
        response = self.client.get("/posts/detail/%s/" % self.post.id)
        self.assertContains(response, self.post.title, status_code=200)

class CreatePostTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            username="test_user",
            email="test@example.com",
            password="secret",
        )
        self.client.force_login(self.user) # ユーザーログイン
        
    def test_render_creation_form(self):
        response = self.client.get("/posts/new/")
        self.assertContains(response, "記事を作成", status_code=200)
        
    def test_create_post(self):
        data = {'title': 'タイトル', 'content': '内容'}
        self.client.post("/posts/new/", data)
        post = Post.objects.get(title='タイトル')
        self.assertEqual('内容', post.content)
    
class CreatePostTest(TestCase):
    def test_should_resolve_post_new(self):
        found = resolve("/posts/new/")
        self.assertEqual(post_new, found.func)
class PostDetailTest(TestCase):
    def test_should_resolve_post_detail(self):
        found = resolve("/posts/detail/1/")
        self.assertEqual("blog:post_detail", found.view_name)
class EditPostTest(TestCase):
    def test_should_resolve_post_edit(self):
        found = resolve("/posts/detail/1/edit/")
        self.assertEqual(post_edit, found.func)
        
        