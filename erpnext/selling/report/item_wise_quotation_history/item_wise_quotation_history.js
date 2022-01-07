// Copyright (c) 2016, Ming Promotion and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item-wise Quotation History"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			fieldname:"from_date",
			reqd: 1,
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			reqd: 1,
			default: frappe.datetime.get_today(),
			label: __("To Date"),
			fieldtype: "Date",
		},
		// {
		// 	fieldname:"item_code",
		// 	label: __("Item"),
		// 	fieldtype: "Link",
		// 	options: "Item",
		// 	get_query: () => {
		// 		return {
		// 			query: "erpnext.controllers.queries.item_query"
		// 		}
		// 	}
		// }
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		let format_fields = ["qty", "amount"];

		if (in_list(format_fields, column.fieldname) && data && data[column.fieldname] > 0) {
			value = "<span style='color:green;'>" + value + "</span>";
		}
		return value;
	}
};
