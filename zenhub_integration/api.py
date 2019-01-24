import frappe
import json
from utils import process_issue, get_github_issue

VALID_EVENTS = ["issues"]


@frappe.whitelist(allow_guest=True)
def push_github_event():
	payload = frappe.local.request
	event_type = payload.headers.get("X-GitHub-Event")
	if event_type not in VALID_EVENTS:
		return

	payload_data = json.loads(payload.data)
	if payload_data.get("action") in ["labeled", "unlabeled", "opened", "edited", "deleted", "closed"]:
		issue = get_github_issue(payload_data.get("issue").get("number"))
		process_issue(issue)


@frappe.whitelist(allow_guest=True)
def push_zenhub_event(allow_guest=True):
	payload = frappe.local.request
	payload_data = json.loads(payload.data)
	task = frappe.get_doc(
		"Task", {"github_issue_link": payload_data.get("github_url")})
	if payload_data.get("type") == "estimate_cleared":
		estimate = 0
	elif payload_data.get("type") == "estimate_set":
		estimate = payload_data.get("estimate")

	task.estimate_story_points = estimate
	task.save(ignore_permissions=True)
