# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt


from erpnext.accounts.doctype.pos_profile.test_pos_profile import make_pos_profile
from erpnext.selling.page.point_of_sale.point_of_sale import get_items
from erpnext.stock.doctype.item.test_item import make_item
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpnext.tests.utils import ERPNextTestCase


class TestPointOfSale(ERPNextTestCase):
	def test_item_search(self):
		"""
		Test Stock and Service Item Search.
		"""

		pos_profile = make_pos_profile()
		item1 = make_item("Test Stock Item", {"is_stock_item": 1})
		make_stock_entry(
			item_code="Test Stock Item", qty=10, to_warehouse="_Test Warehouse - _TC", rate=500
		)

		result = get_items(
			start=0,
			page_length=20,
			price_list=None,
			item_group=item1.item_group,
			pos_profile=pos_profile.name,
			search_term="Test Stock Item",
		)
		filtered_items = result.get("items")

		self.assertEqual(len(filtered_items), 1)
		self.assertEqual(filtered_items[0]["item_code"], "Test Stock Item")
		self.assertEqual(filtered_items[0]["actual_qty"], 10)

		item2 = make_item("Test Service Item", {"is_stock_item": 0})
		result = get_items(
			start=0,
			page_length=20,
			price_list=None,
			item_group=item2.item_group,
			pos_profile=pos_profile.name,
			search_term="Test Service Item",
		)
		filtered_items = result.get("items")

		self.assertEqual(len(filtered_items), 1)
		self.assertEqual(filtered_items[0]["item_code"], "Test Service Item")
