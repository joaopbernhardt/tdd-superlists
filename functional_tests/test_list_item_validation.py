from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_item(self):

        self.browser.get(self.live_server_url)

        # Sends invalid data
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: 
            self.browser.find_element_by_css_selector('#id_text:invalid')
            )

        # Fills valid and send
        self.add_list_item('Buy Milk!')

        # Another invalid entry
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Fills second item
        self.add_list_item('Make tea!')

        # Finnaly, both items are displayed
        self.wait_for_row_in_list_table('1: Buy Milk!')
        self.wait_for_row_in_list_table('2: Make tea!')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)

        self.add_list_item('Buy dupl item')

        
        self.get_item_input_box().send_keys('Buy dupl item')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.add_list_item('Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()))

        self.get_item_input_box().send_keys('a')

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()))