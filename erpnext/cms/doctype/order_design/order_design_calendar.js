// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar["Order Design"] = {
	field_map: {
		"start": "tanggal_upload",
		"end": "deadline",
		"id": "name",
		"title": "no_jo",
		"allDay": "allDay"
	},
	gantt: true,
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "customer",
			"options": "Customer",
			"label": __("Customer")
		}
	]
}
