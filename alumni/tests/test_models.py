from django.test import TestCase, SimpleTestCase
from alumni.models import User, AlumniProfile


class TestRemovedModels(TestCase):
    def test_otp_model_removed(self):
        from alumni import models
        self.assertFalse(hasattr(models, 'OTP'))

    def test_alumni_edit_request_model_removed(self):
        from alumni import models
        self.assertFalse(hasattr(models, 'AlumniEditRequest'))


class TestUserModelSimplified(TestCase):
    def test_user_has_no_coordinator_field(self):
        field_names = [f.name for f in User._meta.get_fields()]
        self.assertNotIn('is_coordinator', field_names)

    def test_user_has_no_created_at_field(self):
        field_names = [f.name for f in User._meta.get_fields()]
        self.assertNotIn('created_at', field_names)


class TestURLPatterns(SimpleTestCase):
    def test_only_required_urls_exist(self):
        from django.urls import resolve
        self.assertTrue(resolve('/'))
        self.assertTrue(resolve('/register/'))
        self.assertTrue(resolve('/directory/'))
        self.assertTrue(resolve('/directory/1/'))
        self.assertTrue(resolve('/directory/1/edit/'))

    def test_old_urls_removed(self):
        from django.urls import resolve
        with self.assertRaises(Exception):
            resolve('/login/')
        with self.assertRaises(Exception):
            resolve('/verify-otp/')
        with self.assertRaises(Exception):
            resolve('/dashboard/')
        with self.assertRaises(Exception):
            resolve('/profile/')
        with self.assertRaises(Exception):
            resolve('/chat/')
        with self.assertRaises(Exception):
            resolve('/jobs/')
        with self.assertRaises(Exception):
            resolve('/events/')


class TestAlumniProfileFields(TestCase):
    def test_profile_has_simplified_fields(self):
        user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            phone='9876543210',
            first_name='Test',
            last_name='User',
            password='testpass',
        )
        profile = AlumniProfile.objects.create(
            user=user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone='9876543210',
            department='CSE',
            year_of_passing=2020,
            current_company='Google',
            current_role='Engineer',
            current_city='Bangalore',
        )

        field_names = [f.name for f in AlumniProfile._meta.get_fields()]

        self.assertIn('first_name', field_names)
        self.assertIn('last_name', field_names)
        self.assertIn('email', field_names)
        self.assertIn('phone', field_names)
        self.assertIn('department', field_names)
        self.assertIn('year_of_passing', field_names)
        self.assertIn('current_company', field_names)
        self.assertIn('current_role', field_names)
        self.assertIn('current_city', field_names)

        self.assertNotIn('skills', field_names)
        self.assertNotIn('willing_to_mentor', field_names)
        self.assertNotIn('linkedin_url', field_names)
        self.assertNotIn('profile_photo', field_names)
        self.assertNotIn('selfie_url', field_names)
        self.assertNotIn('current_address', field_names)
        self.assertNotIn('permanent_address', field_names)
        self.assertNotIn('approved', field_names)
        self.assertNotIn('approved_by', field_names)

    def test_profile_stores_all_fields(self):
        user = User.objects.create_user(
            username='test2@example.com',
            email='test2@example.com',
            phone='9876543211',
            first_name='Test2',
            last_name='User2',
            password='testpass',
        )
        profile = AlumniProfile.objects.create(
            user=user,
            first_name='Test2',
            last_name='User2',
            email='test2@example.com',
            phone='9876543211',
            department='ECE',
            year_of_passing=2019,
            current_company='Microsoft',
            current_role='Developer',
            current_city='Hyderabad',
        )

        profile.refresh_from_db()
        self.assertEqual(profile.first_name, 'Test2')
        self.assertEqual(profile.last_name, 'User2')
        self.assertEqual(profile.email, 'test2@example.com')
        self.assertEqual(profile.phone, '9876543211')
        self.assertEqual(profile.department, 'ECE')
        self.assertEqual(profile.year_of_passing, 2019)
        self.assertEqual(profile.current_company, 'Microsoft')
        self.assertEqual(profile.current_role, 'Developer')
        self.assertEqual(profile.current_city, 'Hyderabad')
