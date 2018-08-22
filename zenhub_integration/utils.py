#!/usr/bin/env python
import csv
import json
import frappe
import requests
from github import Github


def get_zenhub(token, repo_id, endpoint, issue):
    PARAMS = {"access_token": token}
    ZENHUB_URL = "https://api.zenhub.io/p1/repositories/{}/{}/{}".format(
        repo_id, endpoint, issue)
    return requests.get(ZENHUB_URL, params=PARAMS).json()


def get_zenhub_data(tasks, zenhub_token, zenhub_repo_id):
    for task in tasks:
        task = frappe.get_doc("Task", task.name)
        zenhub_data = get_zenhub(zenhub_token, zenhub_repo_id, "issues",
                                 task.github_issue_no)

        task.estimate_story_points = zenhub_data.get(
            "estimate", {}).get("value")

        if zenhub_data.get("is_epic"):
            task.is_group = 1

            issues = get_zenhub(zenhub_token, zenhub_repo_id,
                                "epics", task.github_issue_no).get("issues")

            for issue in issues:
                if frappe.db.exists("Task", {"github_issue_no": issue.get("issue_number")}):
                    frappe.db.set_value("Task", {"github_issue_no": issue.get(
                        "issue_number")}, "parent_task", task.name, update_modified=False)

        task.save()
        frappe.db.commit()


def get_issues():
    settings = frappe.get_single("ZenHub Settings")
    for repo in settings.repositories:
        tasks = get_github_data(settings.get_password(
            "github_token"), repo.github_repo_name)
        get_zenhub_data(tasks, settings.get_password(
            "zenhub_token"), repo.zenhub_repo_id)


def get_github_data(access_token, repo_name):
    tasks = []
    g = Github(access_token)
    issues = g.get_repo(repo_name).get_issues(milestone="*")
    for issue in issues:
        tasks.append(process_issue(issue))
    return tasks


def process_issue(issue):
    project = get_or_create_project(issue)
    priority = get_priority(issue)
    return create_or_update_task(issue, project, priority)


def get_priority(issue):
    # Ugly code to extract Priorities from Labels
    for label in issue.labels:
        if "Priority" in label.name:
            return label.name[10:]


def get_or_create_project(issue):
    # Ugly code to extract Client names from Labels
    customer_name = ""
    project_name = ""
    for label in issue.labels:
        if "Client" in label.name:
            customer_name = label.name[8:]
            if not frappe.db.exists("Customer", customer_name):
                customer = frappe.new_doc("Customer")
                customer.customer_name = customer_name
                customer.save()
                frappe.db.commit()

    if not hasattr(issue.milestone, "title"):
        return

    if customer_name:
        project_name = "{} ({})".format(
            issue.milestone.title, customer_name)
    else:
        project_name = issue.milestone.title

    if not frappe.db.exists("Project", project_name):
        project = frappe.new_doc("Project")
        project.project_name = project_name
        project.customer = customer_name
        project.save()

    frappe.db.commit()
    return project_name


def create_or_update_task(issue, project, priority):
    if not frappe.db.exists("Task", {"github_sync_id": issue.id}):
        task = frappe.new_doc("Task")
    else:
        task = frappe.get_doc("Task", {"github_sync_id": issue.id})
    task.subject = issue.title[:140]
    task.issue_text = issue.title
    task.github_sync_id = issue.id
    task.description = issue.body
    task.status = issue.state.title()
    task.github_issue_link = issue.html_url
    task.github_issue_no = issue.number
    task.project = project
    task.status = issue.state.title()
    if priority:
        task.priority = priority
    task.save()
    frappe.db.commit()
    return task
