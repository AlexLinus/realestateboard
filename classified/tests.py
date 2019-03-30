from django.contrib.auth.models import User
from django.test import TestCase
from .models import Classified
from .forms import ComplaintsForm

# Create your tests here.
class ClassifiedTest(TestCase):
    def setUp(self):
        #Установки запускаются перед каждым тестом
        user = User.objects.create_user('test_user', 'myemail@testing.com', 'alex124')
        get_user = User.objects.get(username__iexact='test_user')
        Classified.objects.create(flat_square=51, flat_floor=4,  total_floor=7, flat_price=150000, slug='xren-znaet', author_phone='+75822551251', is_active=True, author=get_user)

    def test_adding_classified(self):
        my_classified = Classified.objects.get(slug__iexact='xren-znaet')

        self.assertTrue(my_classified, 'Все сработало как надо!')
        self.assertEqual(my_classified.get_absolute_url(), '/classified/xren-znaet/' )
        # Сравнить значение с ожидаемым результатом
        #self.assertEquals(field_label, 'first name')


class ClassifiedTest(TestCase):
    def test_complaint_form(self):
        user = User.objects.create_user('test_user', 'myemail@testing.com', 'alex124')
        get_user = User.objects.get(username__iexact='test_user')
        classified = Classified.objects.create(flat_square=51, flat_floor=4,  total_floor=7, flat_price=150000, slug='xren-znaet', author_phone='+75822551251', is_active=True, author=get_user)
        form_data = {'complaint_body': 'текст обычный', 'classified': classified, 'captcha_answer': 51}
        form = ComplaintsForm(data=form_data)
        self.assertTrue(form.is_valid())