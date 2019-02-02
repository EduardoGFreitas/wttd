from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscrição/ must return code 200 """
        resp = self.client.get('/inscricao/')
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        tags = (
            ('<form',1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"',1),
            ('type="submit"',1)

        )
        """HTML must contains input tags """
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)


    def test_csrf(self):
        """ HTML must contains CSRF """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)



class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='21-99618-6180')

        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """ Valid Post should redirect to /inscricao/ """
        self.assertEqual(302, self.response.status_code)

    def test_subscribe_email(self):
        self.assertAlmostEqual(1, len(mail.outbox))

class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='21-99618-6180')

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
