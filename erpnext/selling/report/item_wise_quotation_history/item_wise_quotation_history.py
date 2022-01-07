# Copyright (c) 2013, Ming Promotion and contributors
# License: MIT. See LICENSE

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils.nestedset import get_descendants_of

def execute(filters=None):
	# columns, data = [], []
	filters = frappe._dict(filters or {})
	
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))
	
	columns = get_columns(filters)
	data = get_data(filters)

	chart_data = get_chart_data(data)

	return columns, data, None, chart_data

def get_columns(filters):
	return [
		{
			"label": _("Item Code"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"options": "Item",
			"width": 350
		},
		{
			"label": _("Item Name"),
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 200
		},
		{
			"label": _("Item Group"),
			"fieldtype": "Data",
			"fieldname": "item_group",
			# "options": "Item Group",
			"width": 200
		},
		{
			"label": _("Quantity"),
			"fieldtype": "Float",
			"fieldname": "quantity",
			"width": 100
		},
		{
			"label": _("Rate"),
			"fieldname": "rate",
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"fieldtype": "Currency",
			"width": 200
		},
		# {
		# 	"label": _("Transaction Date"),
		# 	"fieldtype": "Date",
		# 	"fieldname": "transaction_date",
		# 	"width": 200
		# },
		{
			"label": _("Company"),
			"fieldtype": "Link",
			"fieldname": "company",
			"options": 'Company',
			"width": 250
		},
	]


def get_data(filters):
	data = []

	company_list = get_descendants_of("Company", filters.get("company"))
	quo_records = get_quotation_details(company_list, filters)
	for record in quo_records:
		row = {
			"item_code": record[1],
			"item_name": record[2],
			"item_group": record[3],
			"quantity": record[4],
			"rate": record[6],
			"amount": record[5],
			# "transaction_date": record[7],
			"company": record[8]
		}
		data.append(row)
	return data

def get_quotation_details(company_list, filters):
	
	query = frappe.db.sql("""
		SELECT
			so.customer_name, so_item.item_code, so_item.item_name, i.item_group, SUM(so_item.qty), SUM(so_item.amount), 
			SUM(so_item.rate), so.transaction_date, so.company
		FROM
			`tabQuotation` so, `tabQuotation Item` so_item, `tabItem` i
		WHERE
			so_item.parent = so.name
			AND so_item.item_code = i.name
			AND so.company in ('Ming Media Promotion')
			AND so.docstatus = 1 
			AND so.status != 'Expired'
			AND so.transaction_date >= %(s)s
			AND so.transaction_date <= %(t)s
		GROUP BY so_item.item_code
		ORDER By SUM(so_item.amount) DESC
	""", {
		"s": filters.from_date,
		"t": filters.to_date
	})

	return query

def get_chart_data(data):
	item_wise_quo_map = {}
	labels, datapoints = [], []

	for row in data:
		item_key = row.get("item_name")

		if not item_key in item_wise_quo_map:
			item_wise_quo_map[item_key] = 0

		item_wise_quo_map[item_key] = flt(item_wise_quo_map[item_key]) + flt(row.get("amount"))

	item_wise_quo_map = { 
		item: value for item, 
		value in (
			sorted(item_wise_quo_map.items(), 
			key = lambda i: i[1], 
			reverse=True
			)
		)
	}

	for key in item_wise_quo_map:
		labels.append(key)
		datapoints.append(item_wise_quo_map[key])

	return {
		"data" : {
			"labels" : labels[:30], # show max of 30 items in chart
			"datasets" : [
				{
					"name" : _(" Total Sales Amount"),
					"values" : datapoints[:30]
				}
			]
		},
		"type" : "bar"
	}