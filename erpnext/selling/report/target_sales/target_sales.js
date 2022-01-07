// Copyright (c) 2016, Ming Promotion and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Target Sales"] = {
	"filters": [
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options":'Fiscal Year',
			"default": frappe.sys_defaults.fiscal_year
		},
		{
			"fieldname":"based_on",
			"label": __("Based On"),
			"fieldtype": "Select",
			"options":[
				{ "value": "Quotation", "label": __("Quotation") },
				{ "value": "Sales Order", "label": __("Sales Order") },
				// { "value": "Job Order", "label": __("Job Order") }
			],
			"default": "Quotation"
		},
	]
};
