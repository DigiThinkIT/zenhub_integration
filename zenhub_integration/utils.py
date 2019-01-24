#!/usr/bin/env python
import csv
import json
import frappe
import misaka as m
import requests
from github import Github


def get_zenhub(token, repo_id, endpoint, issue):
    PARAMS = {"access_token": token}
    ZENHUB_URL = "https://api.zenhub.io/p1/repositories/{}/{}/{}".format(
        repo_id, endpoint, issue)
    return requests.get(ZENHUB_URL, params=PARAMS).json()


def get_zenhub_data(tasks, zenhub_token, zenhub_repo_id):
    if not tasks:
        tasks = frappe.get_all("Task", filters={"is_developer_task" : 1})

    for task in tasks:
        task = frappe.get_doc("Task", task.name)
        zenhub_data = get_zenhub(zenhub_token, zenhub_repo_id, "issues",
                                 task.github_issue_no)

        task.estimate_story_points = zenhub_data.get(
            "estimate", {}).get("value")

        # task.status = zenhub_data.get("pipeline").get("name")

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
        get_zenhub_data(tasks=tasks, zenhub_token=settings.get_password(
            "zenhub_token"), zenhub_repo_id=repo.zenhub_repo_id)


def get_github_data(access_token, repo_name):
    tasks = []
    g = Github(access_token)
    issues = g.get_repo(repo_name).get_issues()
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
        if "Project:" in label.name:
            customer_name = label.name[9:]
            # if not frappe.db.exists("Customer", customer_name):
            #     customer = frappe.new_doc("Customer")
            #     customer.customer_name = customer_name
            #     customer.save(ignore_permissions=1)
            #     frappe.db.commit()

    if customer_name:
        project_name = "Project : {}".format(customer_name)

        if not frappe.db.exists("Project", project_name):
            project = frappe.new_doc("Project")
            project.project_name = project_name
            # project.customer = customer_name
            project.save(ignore_permissions=1)

        frappe.db.commit()
        return project_name


def create_or_update_task(issue, project, priority):
    if not frappe.db.exists("Task", {"github_sync_id": issue.id}):
        task = frappe.new_doc("Task")
    else:
        task = frappe.get_doc("Task", {"github_sync_id": issue.id})
    task.subject = issue.title[:140]
    task.github_sync_id = issue.id
    task.description = m.html(issue.body)
    task.status = issue.state.title()
    task.github_issue_link = issue.html_url
    task.github_issue_no = issue.number
    task.creation = issue.created_at
    task.is_developer_task = 1
    task.project = project
    if priority:
        task.priority = priority

    task.owner = get_user_email(issue.user.login)

    task.save(ignore_permissions=1)

    if issue.comments:
        for comment in issue.get_comments():
            # Cause this is the only way Frappe will add a comment with the correct username
            frappe.session.user = get_user_email(comment.user.login)
            add_or_update_comment(task.name, comment)
    frappe.db.commit()
    return task

def get_github_repo():
    settings = frappe.get_single("ZenHub Settings")
    g = Github(settings.get_password("github_token"))
    return g.get_repo(settings.create_in_repo)

def get_github_issue(issue_no):
    g = get_github_repo()
    return g.get_issue(issue_no)

def get_user_email(username):
    return frappe.db.get_value("GitHub Username Map", filters={"github_username" : username}, fieldname="user")

def add_or_update_comment(task_name, comment):
    if not frappe.db.exists("Communication", {"github_comment_id": comment.id}):
        task = frappe.new_doc("Communication")
    else:
        task = frappe.get_doc("Communication", {"github_comment_id": comment.id})

    task.update({
        "doctype":"Communication",
        "communication_type": "Comment",
        "sender": frappe.session.user,
        "comment_type": "Comment",
        "reference_doctype": "Task",
        "reference_name": task_name,
        "content": comment.body,
        "communication_date" : comment.created_at,
        "github_comment_id" : comment.id
    }).save(ignore_permissions=True)