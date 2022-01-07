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
	if filters.period == 'Daily':
		return [
			{
				"label": _("Sales"),
				"fieldtype": "Data",
				"fieldname": "sales_name",
				"width": 200
			},
			{
				"label": _("Target"),
				"fieldtype": "Data",
				"fieldname": "target",
				"width": 150
			},
			{
				"label": _("Today's Deal"),
				"fieldtype": "Float",
				"fieldname": "grand_total",
				"width": 150
			},
			{
				"label": _("Customer"),
				"fieldtype": "Data",
				"fieldname": "customer",
				"width": 200
			},
			{
				"label": _("Area"),
				"fieldtype": "Data",
				"fieldname": "area",
				"width": 200
			},
			{
				"label": _("Percentage"),
				"fieldtype": "Data",
				"fieldname": "percentage",
				"width": 100
			},
			{
				"label": _("Created On"),
				"fieldtype": "Data",
				"fieldname": "created",
				"width": 200
			}
		]
	if filters.period == 'Monthly':
		return [
			{
				"label": _("Sales"),
				"fieldtype": "Data",
				"fieldname": "sales_name",
				"width": 200
			},
			{
				"label": _("Target"),
				"fieldtype": "Currency",
				"fieldname": "target",
				"width": 150
			},
			{ "label": _("January's Deal"), "fieldtype": "Currency", "fieldname": "january_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_jan", "width": 50 },
			{ "label": _("Feb's Deal"), "fieldtype": "Currency", "fieldname": "feb_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_feb", "width": 50 },
			{ "label": _("March's Deal"), "fieldtype": "Currency", "fieldname": "marc_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_marc", "width": 50 },
			{ "label": _("Apr's Deal"), "fieldtype": "Currency", "fieldname": "apr_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_apr", "width": 50 },
			{ "label": _("May's Deal"), "fieldtype": "Currency", "fieldname": "may_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_may", "width": 50 },
			{ "label": _("June's Deal"), "fieldtype": "Currency", "fieldname": "june_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_june", "width": 50 },
			{ "label": _("July's Deal"), "fieldtype": "Currency", "fieldname": "july_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_july", "width": 50 },
			{ "label": _("Aug's Deal"), "fieldtype": "Currency", "fieldname": "aug_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_aug", "width": 50 },
			{ "label": _("Sep's Deal"), "fieldtype": "Currency", "fieldname": "sep_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_sep", "width": 50 },
			{ "label": _("Oct's Deal"), "fieldtype": "Currency", "fieldname": "oct_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_oct", "width": 50 },
			{ "label": _("Nov's Deal"), "fieldtype": "Currency", "fieldname": "nov_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_nov", "width": 50 },
			{ "label": _("Dec's Deal"), "fieldtype": "Currency", "fieldname": "dec_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_dec", "width": 50 },
			{ "label": _("Total Deal"), "fieldtype": "Currency", "fieldname": "total_deal", "width": 150 }, { "label": _("Percentage"), "fieldtype": "Data", "fieldname": "per_dec", "width": 50 }
		]

def get_data(filters):
	data = []
	
	jo_records = get_daily_report(filters)
	if filters.period == 'Daily':
		for record in jo_records:
			row = {
				"sales_name": record[0],
				"target": record[1],
				"grand_total": record[2],
				"customer": record[3],
				"area": record[4],
				"percentage": 0,
				"created": record[5]
			}
			data.append(row)
		return data
	elif filters.period == 'Monthly':
		for record in jo_records:
			row = {
				"sales_name": record[0],
				"target": record[1],
				"january_deal": record[2], "per_jan": 0,
				"feb_deal": record[3], "per_feb": 0,
				"marc_deal": record[4], "per_marc": 0,
				"apr_deal": record[5], "per_apr": 0,
				"may_deal": record[6], "per_may": 0,
				"june_deal": record[7], "per_june": 0,
				"july_deal": record[8], "per_july": 0,
				"aug_deal": record[9], "per_aug": 0,
				"sep_deal": record[10], "per_sep": 0,
				"oct_deal": record[11], "per_oct": 0,
				"nov_deal": record[12], "per_nov": 0,
				"dec_deal": record[13], "per_dec": 0,
				"total_deal": record[14]
			}
			data.append(row)
		return data
	else:
		return ("Turn Back")


def get_daily_report(filters):
	if filters.period == 'Daily':
		query = frappe.db.sql("""
			SELECT 
				u.full_name, tgt.target_amount, qo.grand_total, qo.customer_name, qo_item.item_name, date(qo_item.creation)
			FROM `tabQuotation` qo, `tabQuotation Item` qo_item, `tabTarget Detail` tgt, `tabUser` u
			WHERE
				date(qo_item.creation) = %(s)s
				AND qo.owner = qo_item.owner
				AND qo.owner = u.name
				AND tgt.parent = u.name
				AND qo.docstatus = 1
		
		""", {
			"s": getdate(today())
		})
		print(filters.fiscal_year)
		print(getdate(today()) - relativedelta(days=1))
		return query

	elif filters.period == 'Monthly':
		query = frappe.db.sql("""
			SELECT 
				u.full_name, tgt.target_amount, 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-01-01' AND '%(t)s-01-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-02-01' AND '%(t)s-02-29', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-03-01' AND '%(t)s-03-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-04-01' AND '%(t)s-04-30', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-05-01' AND '%(t)s-05-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-06-01' AND '%(t)s-06-30', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-07-01' AND '%(t)s-07-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-08-01' AND '%(t)s-08-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-09-01' AND '%(t)s-09-30', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-10-01' AND '%(t)s-10-31', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-11-01' AND '%(t)s-11-30', qo.grand_total, NULL)), 
				SUM(IF(qo_item.creation BETWEEN '%(t)s-12-01' AND '%(t)s-12-31', qo.grand_total, NULL)),
				SUM(qo.grand_total)
			FROM `tabQuotation` qo, `tabQuotation Item` qo_item, `tabTarget Detail` tgt, `tabUser` u
			WHERE
				qo.owner = qo_item.owner
				AND qo.owner = u.name
				AND qo.docstatus = 1
				AND tgt.parent = u.name
			GROUP BY u.full_name
		""", {
			"t": int(filters.fiscal_year)
		})
		print(query)
		return query
	else:
		return ("Turn Back")

def get_chart_data(filters):
	return filters