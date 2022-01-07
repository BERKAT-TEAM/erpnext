// Copyright (c) 2021, Ming Promotion and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Rent Info', {
	onload: function(frm) {
		//fetch item details
		frm.add_fetch("item_code", "item_name", "location")
	}
	// refresh: function(frm) {

	// }
});
