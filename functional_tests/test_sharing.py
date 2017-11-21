from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage

def quit_if_possible(browser):
    try: browser.quit()
    except: pass

class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Jose is logged in
        self.create_pre_authenticated_session('jose@example.com')
        self.browser.get(self.live_server_url)
        jose_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(jose_browser))

        # His friend Oni is also in the site
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        self.create_pre_authenticated_session('oni@example.com')
        self.browser.get(self.live_server_url)

        # Jose goes to homepage and starts a new list
        self.browser = jose_browser
        list_page = ListPage(self).add_list_item('Get help')

        # He notices a Share option
        share_box = list_page.get_share_box()
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
            )

        # He shares the list. The page is updated to say that.
        list_page.share_list_with('oni@example.com')

        # Oni goes to the lists page
        self.browser = oni_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Jose's list and clicks it
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oni sees its Jose's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(),
            'jose@example.com'
            ))

        # He adds an item
        list_page.add_list_item('Hi Jose!')

        # Jose refreshes the page and sees Oni's item
        self.browser = jose_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Jose!', 2)