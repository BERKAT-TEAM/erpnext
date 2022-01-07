# Copyright (c) 2013, Ming Promotion and contributors
# License: MIT. See LICENSE

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate, today
from frappe.utils.nestedset import get_descendants_of
from dateutil.relativedelta import relativedelta


def execute(filters=None):
	
	columns, data = [], []
	filters = frappe._dict(filters or  {})

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
			# {
			# 	"label": _("Name"),
			# 	"fieldtype": "Data",
			# 	"fieldname": "name",
			# 	"width": 200
			# },
			{
				"label": _("Total Quantity"),
				"fieldtype": "Float",
				"fieldname": "qty",
				"width": 150
			},
			{
				"label": _("Total Value"),
				"fieldtype": "Currency",
				"fieldname": "grand_total",
				"width": 150
			}
		]

def get_data(filters):
	data = []

	records = get_report(filters)
	# del records[None]

	for record in records:
		row = {
			"sales_name": record[0],
			# "name": record[0],
			"qty": record[1],
			"grand_total": record[2]
		}
		data.append(row)
	return data

def get_report(filters):
	
	query = frappe.db.sql("""
		SELECT 
			qo.sales_name, 
			COUNT(qo.sales_name), 
			SUM(qo.grand_total),
			qo.owner
		FROM `tabQuotation` qo
		WHERE 
			qo.docstatus = 1 
			AND year(qo.creation) = %(t)s 
			AND qo.owner != 'vara@mingpromo.com' 
			AND qo.status != 'Expired'
			AND qo.sales_name != 'MING'
		GROUP BY qo.sales_name
	""", {
		"t": int(filters.fiscal_year)
	})

	print(query)
	return query

def get_chart_data(data):
	value_wise_map = {}
	labels, datapoints = [], []

	for row in data:
		value_key = row.get("sales_name")

		if not value_key in value_wise_map:
			value_wise_map[value_key] = 0

		value_wise_map[value_key] = flt(value_wise_map[value_key]) + flt(row.get("grand_total"))
	value_wise_map = {		
		item: value for item,
		value in (
			sorted(value_wise_map.items(),
				key = lambda i: i[1],
				reverse=True
			)
		)
	}

	for key in value_wise_map:
		labels.append(key)
		datapoints.append(value_wise_map[key])

	return {
		"data" : {
			"labels" : labels[:30], # show max of 30 items in chart
			"datasets" : [
				{
					"name" : _(" Achievement"),
					"values" : datapoints[:30]
				}
			]
		},
		"type" : "bar"
	}
