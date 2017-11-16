from django.test import TestCase
import accounts.views
from unittest.mock import patch

class SendLoginEmailViewTest(TestCase):
    def test_redirects_to_home_page(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'jose@example.com'
            })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_POST(self, mock_send_mail):

        self.client.post('/accounts/send_login_email', data={
            'email': 'jose@example.com'
            })

        self.assertTrue(mock_send_mail.called)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link to Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, ['jose@example.com'])

    def test_adds_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email' : 'jose@example.com'
            }, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(message.message, 
            'Check your email, we have sent you a log in link.')
        self.assertEqual(message.tags, 'success')