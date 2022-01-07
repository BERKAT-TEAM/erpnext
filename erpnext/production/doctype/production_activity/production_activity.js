// Copyright (c) 2021, Ming Promotion and contributors
// For license information, please see license.txt

frappe.ui.form.on('Production Activity', {
	// refresh: function(frm) {
	setup: function(frm) {
		frm.set_df_property('user', 'owner', true)
	}
	// }
});
