from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Имя')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_task(self):
        """Валидная форма создает запись в Task."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': f'{self.user}'})
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id
            ).exists()
        )

    def test_edit_post(self):
        """Проверка формы редактирования поста"""
        post = Post.objects.create(
            author=self.user,
            text='Тестовая пост',
        )
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый тест новый',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{post.id}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{post.id}'}
            ))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый тест новый',
                group=self.group.id
            ).exists())
        self.assertFalse(
            Post.objects.filter(
                text='Тестовый текст',
                group=self.group.id
            ).exists())
