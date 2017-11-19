from django.test import TestCase
from lists.forms import (
    ItemForm, ExistingListItemForm, NewListForm,
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR)
from lists.models import List, Item
import unittest
from unittest.mock import patch, Mock

class ItemFormTest(TestCase):
    def test_form_render_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a To-do item"',
            form.as_p())
        self.assertIn('class="form-control input-lg"',
            form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'],
            [EMPTY_ITEM_ERROR])

class ExistingListItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a To-do item"', form.as_p())
        

    def test_form_validation_for_blank_item(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_duplicate_item(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': '1'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])

class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_from_post_data_if_user_not_authenticated(
        self, mock_List_create_new
        ):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.asser_called_once_with(
            first_item_text = 'new item text'
            )

    @patch('lists.forms.List.create_new')
    def test_save_creates_new_list_with_owner_if_user_is_authenticated(
        self, mock_List_create_new
        ):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.asser_called_once_with(
            first_item_text = 'new item text', owner=user
            )

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    @patch('lists.forms.List.create_new')
    def test_save_returns_new_list_object(self, mock_List_create_new):
        user = Mock(is_authenticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)