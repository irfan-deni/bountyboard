# Database Schema

## User (`django.contrib.auth.models.User`)

| Field | Type | Notes |
|---|---|---|
| id | PK | auto-increment |
| username | varchar(150) | unique |
| email | varchar(254) | |
| password | varchar(128) | hashed |
| is_superuser | bool | full admin |
| date_joined | datetime | |
| last_login | datetime | nullable |

## Profile (`users.Profile`)

| Field | Type | Notes |
|---|---|---|
| id | PK | auto-increment |
| user | FK → User | one-to-one |
| phone | varchar(15) | blank |

## Bounty / Task (`tasks.Task`)

| Field | Type | Notes |
|---|---|---|
| id | PK | auto-increment |
| poster | FK → User | |
| hunter | FK → User | nullable, who claimed/completed the task |
| title | varchar(200) | |
| description | text | |
| category | varchar(20) | Delivery / Coding Help / Design / Tutoring / Errands / Photography / Other |
| bounty | decimal(8,2) | in RM |
| status | varchar(10) | Open / Claimed / Completed / Closed |
| deadline | datetime | |
| created_at | datetime | auto now |

## Review (`tasks.Review`)

| Field | Type | Notes |
|---|---|---|
| id | PK | auto-increment |
| task | FK → Task | |
| reviewer | FK → User | poster or hunter giving the review |
| reviewee | FK → User | the other party being reviewed |
| rating | int | 1–5 |
| comment | text | |
| created_at | datetime | auto now |

## Relationships

```
User ──→ Profile         (1:1)
User ──→ Task (poster)   (1:N)
User ──→ Task (hunter)   (1:N)
Task ──→ Review          (1:N)
```
