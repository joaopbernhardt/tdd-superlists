from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_item(self):

        self.browser.get(self.live_server_url)

        # Sends invalid data
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: 
            self.browser.find_element_by_css_selector('#id_text:invalid')
            )

        # Fills valid and send
        self.get_item_input_box().send_keys('Buy Milk!')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
            )
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy Milk!')

        # Another invalid entry
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Fills second item
        self.get_item_input_box().send_keys('Make tea!')
        self.wait_for(lambda:
            self.browser.find_element_by_css_selector('#id_text:valid')
            )
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Finnaly, both items are displayed
        self.wait_for_row_in_list_table('1: Buy Milk!')
        self.wait_for_row_in_list_table('2: Make tea!')

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Buy dupl item')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy dupl item')

        self.get_item_input_box().send_keys('Buy dupl item')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You've already got this in your list"))