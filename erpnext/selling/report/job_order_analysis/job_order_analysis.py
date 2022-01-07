# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import copy

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	data, chart_data, columns = [], [], []

	validate_filters(filters)

	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	# chart_data = prepare_data(data, filters)

	# print(columns, data, chart_data)

	return columns, data

def get_columns(filters):
	columns = [
		{
			"label":_("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 90
		},
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 120
		},
		{
			"label":_("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 130
		}]

	if not filters.get("group_by_so"):
		columns.append({
			"label":_("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		})

	columns.extend([
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 80,
			"convertible": "qty"
		},
		{
			"label": _("Nilai Job Order"),
			"fieldname": "nilai_jo",
			"fieldtype": "Currency",
			"width": 220,
		},
		{
			"label": _("Nilai Bersih JO"),
			"fieldname": "net_jo",
			"fieldtype": "Currency",
			"width": 220,
		},
		{
			"label": _("Nilai Sales"),
			"fieldname": "sales_value",
			"fieldtype": "Currency",
			"width": 220,
		},
		{
			"label":_("Delivery Date"),
			"fieldname": "delivery_date",
			"fieldtype": "Date",
			"width": 120
		},
	])
	columns.append({
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 100
		})


	return columns

def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and so.transaction_date between %(from_date)s and %(to_date)s"

	if filters.get("company"):
		conditions += " and so.company = %(company)s"

	if filters.get("sales_order"):
		conditions += " and so.name in %(sales_order)s"

	if filters.get("status"):
		conditions += " and so.status in %(status)s"

	return conditions

def prepare_data(data, filters):
	data = []
	for record in data:
		row = {
			"date": record.date,
			"sales_order": record.sales_order,
			"status": record.on_time,
			"customer": record.customer,
			"item_code": record.nm_product,
			"qty": record.qty,
			"nilai_jo": record.nilai_jo,
			"net_jo": record.nilai_bersih_jo,
			"sales_value": record.nilai_sales,
			"delivery_date": record.delivery_date,
			"company": record.company
		}
		data.append(row)

	return data


def get_data(conditions, filters):

	data = frappe.db.sql("""
		SELECT
			so.transaction_date as date,
			so.delivery_date as delivery_date,
			so.name as sales_order, so.status, 
			so.customer, so.nm_product, so.qty, so.on_time, 
			so.nilai_job_order, so.nilai_bersih_jo, so.nilai_sales,
			so.company
		FROM
			`tabSales Order` so
		WHERE
			so.status not in ('Stopped', 'Closed', 'On Hold')
			and so.docstatus = 1
			{conditions}
		ORDER BY so.transaction_date ASC
	""".format(conditions=conditions), filters, as_dict=1)

	return data

# def prepare_chart_data(filters):
# 	value_wise_map = {}
# 	labels, datapoints = [], []

# 	for row in data:
# 		value_key = row.get("sales_order")

# 		if not value_key in value_wise_map:
# 			value_wise_map[value_key] = 0

# 		value_wise_map[value_key] = flt(value_wise_map[value_key]) + flt(row.get("sales_value"))
# 	value_wise_map = {		
# 		item: value for item,
# 		value in (
# 			sorted(value_wise_map.items(),
# 				key = lambda i: i[1],
# 				reverse=True
# 			)
# 		)
# 	}

# 	for key in value_wise_map:
# 		labels.append(key)
# 		datapoints.append(value_wise_map[key])

# 	return {
# 		"data" : {
# 			"labels": labels,
# 			"datasets" : [
# 				{
# 					"name" : _("Nilai Sales"),
# 					"values" : datapoints[:30]
# 				}
# 			]
# 		},
# 		"type": 'bar',
# 		"height": 300
# 	}
