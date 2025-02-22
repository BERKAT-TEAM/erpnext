from __future__ import unicode_literals

from frappe import _


def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions against this Sales Person. See timeline below for details'),
		# 'fieldname': 'sales_person',
		'fieldname': 'owner',
		'transactions': [
			{
				'label': _('Sales'),
				'items': [
					'Quotation',
					# 'Sales Order', 
					# 'Delivery Note', 
					# 'Sales Invoice'
				]
			},
		]
	}
