# Copyright (c) 2013, Ming Promotion and contributors
# License: MIT. See LICENSE

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
	columns, data = [], []
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
			"label": _("Sales"),
			"fieldtype": "Data",
			"fieldname": "sales_name",
			"width": 200
		},
		{
			"label": _("Customer"),
			"fieldtype": "Data",
			"fieldname": "customer_name",
			"width": 250
		},
		{
			"label": _("Territory"),
			"fieldtype": "Link",
			"fieldname": "territory",
			"options": "Territory",
			"width": 150
		},
		{
			"label": _("Net Sales"),
			"fieldname": "grand_total",
			"options": "Currency",
			"width": 200
		}
	]


def get_data(filters):
	data = []

	jo_records = get_job_order(filters)
	for record in jo_records:
		row = {
			"sales_name": record[0],
			"customer_name": record[1],
			"territory": record[2],
			"grand_total": record[3]
		}
		data.append(row)
	return data

def get_job_order(filters):
	
	query = frappe.db.sql("""
		SELECT
			quo.sales_name, quo.customer_name, quo.territory, SUM(quo.grand_total)
		FROM
			`tabQuotation` quo
		WHERE
			quo.company in ('Ming Media Promotion')
			AND quo.docstatus = 1 
			AND transaction_date >= %(s)s
			AND transaction_date <= %(t)s
		GROUP BY customer_name
		ORDER BY grand_total DESC
	""", { "s": filters.from_date, "t": filters.to_date})

	return query

def get_chart_data(data):
	item_wise_quo_map = {}
	labels, datapoints = [], []

	for row in data:
		item_key = row.get("customer_name")

		if not item_key in item_wise_quo_map:
			item_wise_quo_map[item_key] = 0

		item_wise_quo_map[item_key] = flt(item_wise_quo_map[item_key]) + flt(row.get("grand_total"))

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