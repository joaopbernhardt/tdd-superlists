from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
#from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest


from .base import FunctionalTest
User = get_user_model()

class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'jose@example.com'
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.add_list_item('Item 1')
        self.add_list_item('Item 2')
        first_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Item 1')
            )
        self.browser.find_element_by_link_text('Item 1').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
            )

        self.browser.get(self.live_server_url)
        self.add_list_item('Item B1')
        second_list_url = self.browser.current_url

        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Item B1')
            )
        self.browser.find_element_by_link_text('Item B1').click()

        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
            )

        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements_by_link_text('My lists'),
            []
            ))