// Copyright (c) 2016, Ming Promotion and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Top Sales Person Quotation-based"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options":'Fiscal Year',
			"default": frappe.sys_defaults.fiscal_year
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		}
	]
}