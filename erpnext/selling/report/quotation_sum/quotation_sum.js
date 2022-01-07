// Copyright (c) 2016, Ming Promotion and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Quotation SUM"] = {
	"filters": [
		{
			fieldname:"from_date",

			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -4),
		},
		{
			fieldname:"to_date",
		
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		}
	]
}