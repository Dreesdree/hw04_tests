from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Имя')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}
                    ): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': 'Имя'}
                    ): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.pk}
                    ): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.pk}
                    ): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_post(self):
        """Принимает объект поста и проверяет его атрибуты"""
        response = self.guest_client.get(
            reverse("posts:post_detail", kwargs={"post_id": self.post.id})
        )
        field_1 = response.context.get("post").text
        field_2 = response.context.get("post").author
        field_3 = response.context.get("post").group
        self.assertEqual(field_1, self.post.text)
        self.assertEqual(field_2, self.post.author)
        self.assertEqual(field_3, self.post.group)

    def test_index_show_correct_context(self):
        """Список постов в шаблоне index равен ожидаемому контексту."""
        response = self.guest_client.get(reverse("posts:index"))
        expected = list(Post.objects.all()[:10])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_group_list_show_correct_context(self):
        """Список постов в шаблоне group_list равен ожидаемому контексту."""
        response = self.guest_client.get(
            reverse("posts:group_list", kwargs={"slug": self.group.slug})
        )
        expected = list(Post.objects.filter(group_id="1")[:10])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_profile_show_correct_context(self):
        """Список постов в шаблоне profile равен ожидаемому контексту."""
        response = self.guest_client.get(
            reverse("posts:profile", args=(self.post.author,))
        )
        expected = list(Post.objects.filter(author_id="1")[:10])
        self.assertEqual(list(response.context["page_obj"]), expected)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        self.check_post()

    def test_create_edit_show_correct_context(self):
        """Шаблон create_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse("posts:post_edit", kwargs={"post_id": self.post.id})
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_create_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse("posts:post_create"))
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["form"].fields[value]
                self.assertIsInstance(form_field, expected)

    def check_group_in_pages(self):
        """Проверяем создание group при создании поста на страницах."""
        const = {"group": self.post.group}
        form_fields = {
            reverse("posts:index"): const,
            reverse("posts:group_list",
                    kwargs={"slug": self.group.slug}): const,
            reverse("posts:profile",
                    kwargs={"username": self.post.author}): const,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                response = self.authorized_client.get(value)
                form_field = response.context["page_obj"].fields[value]
                self.assertIn(form_field, expected)

    def check_group_not_in_mistake_group_list_page(self):
        """Проверяем чтобы созданный Пост не попап в чужую группу."""
        response = self.authorized_client.get(
            reverse("posts:group_list", kwargs={"slug": self.group.slug})
        )
        form_fields = {
            "group": self.post.group,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context["page_obj"].fields[value]
                self.assertNotIn(form_field, expected)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Имя')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание'
        )
        cls.posts = [
            Post.objects.create(
                author=cls.user,
                text='Текст поста № {i}',
                group=cls.group
            )
            for i in range(13)
        ]

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        """На первой странице 10 постов"""
        url_paginator_test = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}),
            reverse('posts:profile', kwargs={
                'username': self.user.username})
        ]
        for url_name in url_paginator_test:
            with self.subTest(url_name=url_name):
                response = self.authorized_client.get(url_name)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """На второй оставшиеся 3 поста"""
        url_paginator_test = [
            reverse('posts:index') + '?page=2',
            reverse(
                'posts:group_list', kwargs={
                    'slug': self.group.slug}) + '?page=2',
            reverse(
                'posts:profile', kwargs={
                    'username': self.user.username}) + '?page=2'
        ]
        for url_name in url_paginator_test:
            with self.subTest(url_name=url_name):
                response = self.authorized_client.get(url_name)
                self.assertEqual(len(response.context['page_obj']), 3)
