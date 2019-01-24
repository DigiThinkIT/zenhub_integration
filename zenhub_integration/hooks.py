# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "zenhub_integration"
app_title = "Zenhub Integration"
app_publisher = "Bloom Stack, Inc"
app_description = "Automatically pulls data from Github and ZenHub"
app_icon = "octicon octicon-octoface"
app_color = "light blue"
app_email = "valmik@bloomstack.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/zenhub_integration/css/zenhub_integration.css"
# app_include_js = "/assets/zenhub_integration/js/zenhub_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/zenhub_integration/css/zenhub_integration.css"
# web_include_js = "/assets/zenhub_integration/js/zenhub_integration.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "zenhub_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "zenhub_integration.install.before_install"
# after_install = "zenhub_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "zenhub_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Task": {
# 		"on_update": "zenhub_integration.hook_events.create_or_update_issue"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"daily": [
# 		"zenhub_integration.utils.get_issues"
#     ]
# }

# Testing
# -------

# before_tests = "zenhub_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "zenhub_integration.event.get_events"
# }

