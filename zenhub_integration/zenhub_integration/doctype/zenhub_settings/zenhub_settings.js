// Copyright (c) 2018, Bloom Stack, Inc and contributors
// For license information, please see license.txt

frappe.ui.form.on('ZenHub Settings', {
	refresh: function(frm) {
		frm.page.set_primary_action(__("Get Issues"), function() {
			frappe.call({
				method: "get_issues",
				callback: function() {
					frappe.msgprint("Syncing issues in background")
				}
			});
		}).addClass('btn btn-primary');
	}
});
