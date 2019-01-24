import frappe
from utils import get_github_repo, get_github_issue
from frappe.utils.background_jobs import enqueue

def _create_or_update_issue(doc):
    if not doc.is_developer_task:
        return

    title = doc.subject
    body = frappe.utils.to_markdown(doc.description)

    if not doc.github_issue_link:
        repo = get_github_repo()
        issue = repo.create_issue(title=title, body=body)
    else:
        issue = get_github_issue(doc.github_issue_no)
        issue.edit(title=title, body=body)

def create_or_update_issue(doc, method):
    enqueue(_create_or_update_issue, doc=doc)

def update_zenhub_pipeline(doc):
    pass