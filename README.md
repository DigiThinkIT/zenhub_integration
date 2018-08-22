# Zenhub Integration

This is a fairly opinionated ERPNext App that automatically turns your ZenHub Sprint into a Project on ERPNext.

## Why?

Well, we wanted to move our internal time tracking to ERPNext because our currently solution was really just *okay*.

The idea is to use our [Desktop Time Tracking app](https://github.com/DigiThinkIT/erpnext-timer-app) to connect to ERPNext, so that we can pull tasks and track time against them.

## Data Mapping

Firstly, we have some labels we use on our GitHub Issues that we're gonna use to map some ERPNext features.

* `Client: [Client-Name]`
* `Priority: [Low/Medium/High/Urgent]`


This is the mapping that happens between Zenhub + Github and ERPNext :-
* Each Issue is a Task
* Each Epic is a Parent Task with Tasks under it
* Each Client is a Customer
* Each Sprint (Milestone) is a Project
    * However, if you're using the client label, the script will create separate projects for each client, and one catch-all project for issues without a client

**The Script deliberately only pulls issues that have a milestone, this is to reduce clutter**

## Custom Fields

There are some Custom fields that also get injected, here's the extra data you'll also get in the Task Document

* Estimate
* Github Issue Link
* GitHub Sync ID (Hidden)
* GitHub Issue Number (Hidden)

## Some gotchas

The subject field of "Task" has a limit of 140 characters, so, when pulling from Github I truncate it to 140 characters max. However, the full issue title gets stored in a custom field called "Issue Text".
