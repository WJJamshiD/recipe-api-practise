from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag, Ingredient, Recipe, image_file_path


def sample_user(email='sample@gmail.com', password='expass'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating new user with an email successful"""
        email = 'test@gmail.com'
        password = '123asdasgaf'
        user = get_user_model().objects.create_user(
                                    email=email,
                                    password=password
                                )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMail.COM'
        user = get_user_model().objects.create_user(email, 'asdasd22')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test121')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
                                'testasd@gmail.COM',
                                'test545'
                            )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = Tag.objects.create(
            user=sample_user(),
            name='Vagan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = Recipe.objects.create(
            user=sample_user(),
            title='My first recipe',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)
    
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = image_file_path(None, 'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'

        self.assertEqual(file_path, exp_path)



