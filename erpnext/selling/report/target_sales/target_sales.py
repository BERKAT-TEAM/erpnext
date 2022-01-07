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
			"label": _("Month"),
			"fieldtype": "Data",
			"fieldname": "month",
			"width": 200
		},
		{
			"label": _("Year"),
			"fieldtype": "Data",
			"fieldname": "year",
			"width": 100
		},
		{ 
			"label": _("Achievement"), 
			"fieldtype": "Currency", 
			"fieldname": "achievement", 
			"width": 250 
		}, { 
			"label": _("Percentage"), 
			"fieldtype": "Float", 
			"fieldname": "percent", 
			"width": 50 
		},
		{ 
			"label": _("Target"), 
			"fieldtype": "Currency", 
			"fieldname": "target", 
			"width": 250 
		}
	]

def get_data(filters):

	print(filters)

	data, temp, join = [], [], []
	
	records = get_target(filters)
	jo_records = get_daily_report(filters)
	
	for record in records:
		row = {
			"year": record[0],
			"target": record[1],
		}
		data.append(row)
	
	for record in jo_records:
		month = ()
		if record[0] == 1:
			month = 'January'
		elif record[0] == 2:
			month = 'February'
		elif record[0] == 3:
			month = 'March'
		elif record[0] == 4:
			month = 'April'
		elif record[0] == 5:
			month = 'May'
		elif record[0] == 6:
			month = 'June'
		elif record[0] == 7:
			month = 'July'
		elif record[0] == 8:
			month = 'August'
		elif record[0] == 9:
			month = 'September'
		elif record[0] == 10:
			month = 'October'
		elif record[0] == 11:
			month = 'November'
		else:
			month = 'December'
		
		row = {
			"month": month,
			"achievement": record[1],
		}
		temp.append(row)

	join = data + temp
	return join
	

def get_target(filters):
	query = frappe.db.sql(""" 
		SELECT 
			st.year, st.target  
		FROM `tabSales Target` st
		WHERE st.year = %(s)s 
	""", { 
		"s": filters.fiscal_year 
	})

	return query


def get_daily_report(filters):
	query = frappe.db.sql("""
		SELECT month(qo_item.creation), SUM(qo.grand_total)
		FROM `tabQuotation` qo, `tabQuotation Item` qo_item, `tabTarget Detail` tgt, `tabUser` u
		WHERE qo.docstatus = 1 AND year(qo_item.creation) = %(t)s
		GROUP BY month(qo_item.creation)
	""", {
		"t": int(filters.fiscal_year)
	})

	return query

def get_chart_data(data):

	value_wise_map = {}
	labels, datapoints = [], []

	for row in data:
		value_key = row.get("month")

		if not value_key in value_wise_map:
			value_wise_map[value_key] = 0

		value_wise_map[value_key] = flt(value_wise_map[value_key]) + flt(row.get("achievement"))
	value_wise_map = {		
		item: value for item,
		value in (
			sorted(value_wise_map.items(),
				key = lambda i: i[1],
				reverse=False
			)
		)
	}

	del value_wise_map[None]
	print(value_wise_map) 

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
	# return data