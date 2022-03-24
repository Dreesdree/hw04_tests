from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели User корректно работает __str__."""
        user = self.user
        expected_object_name = user.username
        self.assertEqual(expected_object_name, str(user))

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = self.post
        expected_object_name = post.text
        self.assertEqual(expected_object_name, str(post))

    def test_verbose_name_post(self):
        """Проверяем verbose_name совпадает с ожидаемым в модели Post."""
        post = self.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value
                )

    def test_help_text_post(self):
        """Проверяем help_text совпадает с ожидаемым в модели Post."""
        post = self.post
        field_help_texts = {
            'text': 'Текст нового поста',
            'author': 'Автор поста',
            'group': 'Группа поста',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value
                )


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = self.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_verbose_name_group(self):
        """Проверяем verbose_name совпадает с ожидаемым в модели Group."""
        group = self.group
        field_verboses = {
            'title': 'Группа',
            'slug': 'Уникальный ID',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name,
                    expected_value
                )

    def test_help_text_group(self):
        """Проверяем help_text совпадает с ожидаемым в модели Group."""
        group = self.group
        field_help_texts = {
            'title': 'Название группы',
            'slug': 'ID группы',
            'description': 'Подробнее',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value
                )
