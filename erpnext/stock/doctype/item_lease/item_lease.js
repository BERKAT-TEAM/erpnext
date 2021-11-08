// Copyright (c) 2021, Ming Promotion and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Lease', {
	// refresh: function(frm) {
		onload: function(frm) {
			//fetch item details
			frm.add_fetch("item_code", "item_name", "location")
		}
	// }
});
