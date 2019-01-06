from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """Get /inscrição/ must return code 200 """
        response = self.client.get('/inscricao/')
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(
            self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)  # atualizar essa linha
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """ HTML must contains CSRF """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form """
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fileds(self):
        """Form must have 4 fields """
        form = self.resp.context['form']
        self.assertSequenceEqual(
            ['name', 'cpf', 'email', 'phone'], list(form.fields))
