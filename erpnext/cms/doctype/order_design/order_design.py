# Copyright (c) 2021, Ming Promotion and contributors
# For license information, please see license.txt


from __future__ import unicode_literals

from collections import Counter

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_url, getdate, add_days, nowdate
from frappe.utils.verified_command import get_signed_params

class OrderDesign(Document):
	def before_insert(self):
		number_of_order_design_slot = frappe.db.sql(
			"""SELECT COUNT(name) FROM `tabOrder Design` WHERE `tabOrder Design`.creation >= %(s)s""", 
			{"s": getdate()})[0][0]
		if number_of_order_design_slot == 20:
			frappe.throw(_('Slot already full. Try again tomorrow :) <br> Slot sudah penuh. Silahkan coba di esok hari :)'))
