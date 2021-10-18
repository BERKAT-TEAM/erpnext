# Copyright (c) 2021, Ming Promotion and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class JobOrderItem(Document):
	pass

def on_doctype_update():
	frappe.db.add_index("Sales Order Item", ["item_code", "warehouse"])