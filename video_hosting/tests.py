from django.test import TestCase
from .models import Video, Comment
from django.urls import reverse
from .forms import RegisrationForm, UserLoginForm, CommentForm


class VideoModelTest(TestCase):
    """
    Tests for Video model
    """
    
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Video.objects.create(title='test title', description='test description', image='test image', file='test file')
    
    def test_title_content(self):
        video = Video.objects.get(id=1)
        expected_object_name = f'{video.title}'
        self.assertEquals(expected_object_name, 'test title')
    
    def test_description_content(self):
        video = Video.objects.get(id=1)
        expected_object_name = f'{video.description}'
        self.assertEquals(expected_object_name, 'test description')
    
    def test_image_content(self):
        video = Video.objects.get(id=1)
        expected_object_name = f'{video.image}'
        self.assertEquals(expected_object_name, 'test image')
    
    def test_file_content(self):
        video = Video.objects.get(id=1)
        expected_object_name = f'{video.file}'
        self.assertEquals(expected_object_name, 'test file')
    
    def test_object_name_is_title(self):
        video = Video.objects.get(id=1)
        expected_object_name = video.title
        self.assertEquals(expected_object_name, str(video))


class VideoViewTest(TestCase):
    """
    Tests for Video views
    """
        
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Video.objects.create(title='test title', description='test description', image='test image', file='test file')
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('video', args=[1]))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('video', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_hosting/video.html')
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('stream', args=[1]))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('stream', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_hosting/video.html')
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'video_hosting/home.html')    


def valid_registration():
    form_data = {'username': 'test', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword'}
    form = RegisrationForm(data=form_data)
    return form.is_valid(), form


class RegistrationFormTest(TestCase):
    """
    Tests for Registration form
    """
    
    def test_registration_form(self):
        register = valid_registration()
        self.assertTrue(register)

    def test_registration_form_invalid_email(self):
        form_data = {'username': 'test', 'email': 'test', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = RegisrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_pass(self):
        form_data = {'username': 'test', 'email': 'test@example.com', 'password1': 'testpassword', 'password2': 'testpassword1'}
        form = RegisrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_username(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'email': 'test@lol.com', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = RegisrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_registration_form_invalid_email(self):
        valid_registration()[1].save()
        form_data = {'username': 'test1', 'email': 'test@example', 'password1': 'testpassword', 'password2': 'testpassword'}
        form = RegisrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserLoginTest(TestCase):
    """
    Tests for User login
    """
    
    def test_login(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_invalid_username(self):
        valid_registration()[1].save()
        form_data = {'username': 'test1', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_invalid_password(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword1'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserTokenTest(TestCase):
    """
    Tests for User token
    """
    
    def test_token_obtain(self):
        valid_registration()[1].save()
        response = self.client.post('/api/token/', {'username': 'test', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')
        return response.json()['refresh']


    def test_token_refresh(self):
        response = self.client.post('/api/token/refresh/', data={'refresh': self.test_token_obtain()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access')


class UserLogoutTest(TestCase):
    """
    Tests for User logout
    """
    
    def test_logout(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def test_logout_invalid(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)


class PasswordResetTest(TestCase):
    """
    Tests for Password reset
    """
    def test_password_reset(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302) 
        response = self.client.post('/accounts/password_reset/', {'email': 'test@example.com'})
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "We've emailed you instructions for setting your password. You should receive the email shortly!")


class CommentModelTest(TestCase):
    """
    Tests for Comment model
    """
    def test_comment(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302)
        video = Video.objects.create(
            title='Test video',
            description='Test video description',
            image='media/image/tWbfk65PEbA.jpg',
            file='media/video/360.mp4',
        )
        comment = Comment.objects.create(
            video=video,
            text='Test comment',
        )
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(comment.video, video)


class CommentFormTest(TestCase):
    """
    Tests for Comment form
    """
    def test_comment_form(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302)
        form_data = {'text': 'Test comment'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['text'], 'Test comment')

    def test_comment_form_invalid(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302)
        form_data = {'text': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'text': ['This field is required.']})

    def test_comment_form_invalid_length(self):
        valid_registration()[1].save()
        form_data = {'username': 'test', 'password': 'testpassword'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post('/accounts/login/', form_data)
        self.assertEqual(response.status_code, 302)
        form_data = {'text': 'a' * 1001}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())


