# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bloom Stack, Inc and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from zenhub_integration.utils import get_issues
from frappe.utils.background_jobs import enqueue

class ZenHubSettings(Document):
	def get_issues(self):
		enqueue(get_issues, timeout="3000")
		frappe.msgprint("Fetching issues in Background")
