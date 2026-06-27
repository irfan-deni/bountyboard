# Database Schema

BountyBoard is a campus task marketplace where a **poster** offers a cash bounty for a task and a **hunter** completes it. This document describes the current data model: the `Profile` extension of the built-in Django user, and the `Task`, `Claim`, `Proof`, and `Review` models that drive the task lifecycle.

## Relationships overview

- **User 1—1 Profile** — every user has exactly one profile (auto-created on signup).
- **User 1—\* Task (as poster)** — a user can post many tasks.
- **User 1—\* Task (as hunter)** — a user can be assigned to many tasks.
- **Task 1—\* Claim** and **User 1—\* Claim (as hunter)** — a task receives many claims; a hunter makes many claims. Each `(task, hunter)` pair is unique (a hunter can claim a given task only once).
- **Task 1—\* Proof** and **User 1—\* Proof (as hunter)** — a task can have proof submissions; a hunter can submit many proofs.
- **Task 1—\* Review**, **User 1—\* Review (as reviewer)**, and **User 1—\* Review (as reviewee)** — a task can carry reviews from both parties; each user gives and receives reviews.

### ER sketch

```
                ┌─────────┐  1      1  ┌─────────┐
                │  User   ├────────────┤ Profile │
                └────┬────┘            └─────────┘
                     │
     poster (1:N)    │    hunter (1:N, nullable)
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            │
   ┌─────────┐                    │
   │  Task   │◄───────────────────┘
   └────┬────┘
        │ 1:N        1:N           1:N
        ├──────────────┬───────────────┐
        ▼              ▼               ▼
   ┌─────────┐    ┌─────────┐     ┌─────────┐
   │  Claim  │    │  Proof  │     │ Review  │
   └─────────┘    └─────────┘     └─────────┘
   (hunter)        (hunter)        (reviewer,
   unique per                       reviewee)
   (task,hunter)
```

## User (`django.contrib.auth.models.User`)

BountyBoard uses Django's built-in authentication user. It is referenced by every other model but is not redefined here; the application-specific fields live on `Profile`.

## Profile (`users.Profile`)

Extends `User` with campus-marketplace profile details. A `Profile` is created automatically for every new `User` through a `post_save` signal.

| Field | Type | Constraints / Notes |
|---|---|---|
| user | OneToOneField → User | `on_delete=CASCADE`; one profile per user |
| phone | CharField(max_length=15) | `blank=True` |
| bio | TextField | `blank=True` |
| avatar | ImageField | `upload_to='avatars/'`, `blank=True` |

## Task (`tasks.Task`)

A bounty posting. Created by a poster and, once a claim is accepted, assigned to a hunter.

| Field | Type | Constraints / Notes |
|---|---|---|
| poster | ForeignKey → User | `on_delete=CASCADE`, `related_name='posted_tasks'` |
| hunter | ForeignKey → User | `on_delete=SET_NULL`, `null=True`, `blank=True`, `related_name='claimed_tasks'`; set only when a claim is accepted |
| title | CharField(max_length=200) | required |
| description | TextField | required |
| category | CharField(max_length=20) | choices: `delivery`, `coding` (Coding Help), `design`, `tutoring`, `errands`, `photography`, `other` |
| bounty | DecimalField(max_digits=8, decimal_places=2) | amount in RM (Malaysian Ringgit) |
| status | CharField(max_length=12) | `default='open'`; choices: `open`, `in_progress`, `completed`, `done`, `closed` (`closed` is defined but currently unused) |
| deadline | DateTimeField | required |
| created_at | DateTimeField | `auto_now_add=True` |

## Claim (`tasks.Claim`)

A hunter's request to take on a task. The poster reviews claims and accepts one, which assigns that hunter to the task.

| Field | Type | Constraints / Notes |
|---|---|---|
| task | ForeignKey → Task | `on_delete=CASCADE`, `related_name='claims'` |
| hunter | ForeignKey → User | `on_delete=CASCADE`, `related_name='claims'` |
| status | CharField(max_length=10) | `default='pending'`; choices: `pending`, `accepted`, `rejected` |
| created_at | DateTimeField | `auto_now_add=True` |

**Meta:** `unique_together = ('task', 'hunter')` — a hunter can claim a task only once; `ordering = ['-created_at']` — newest claims first.

## Proof (`tasks.Proof`)

Evidence submitted by the assigned hunter to demonstrate that the task was completed, for the poster to review.

| Field | Type | Constraints / Notes |
|---|---|---|
| task | ForeignKey → Task | `on_delete=CASCADE`, `related_name='proofs'` |
| hunter | ForeignKey → User | `on_delete=CASCADE` |
| image | ImageField | `upload_to='proofs/'`; required |
| description | TextField | `blank=True` |
| created_at | DateTimeField | `auto_now_add=True` |

## Review (`tasks.Review`)

A rating and comment left after a task is finished. Both the poster and the hunter may review each other on a completed or done task.

| Field | Type | Constraints / Notes |
|---|---|---|
| task | ForeignKey → Task | `on_delete=CASCADE`, `related_name='reviews'` |
| reviewer | ForeignKey → User | `on_delete=CASCADE`, `related_name='given_reviews'`; the party leaving the review |
| reviewee | ForeignKey → User | `on_delete=CASCADE`, `related_name='received_reviews'`; the party being reviewed |
| rating | IntegerField | choices: `1`–`5` |
| comment | TextField | required |
| created_at | DateTimeField | `auto_now_add=True` |

## Task status lifecycle

A task moves through the following states:

```
open ──► in_progress ──► completed ──► done
```

1. **open** — The poster publishes the task. Hunters submit `Claim` records.
2. **in_progress** — The poster accepts one hunter's claim. That hunter is assigned to the task (the `Task.hunter` field is set), and all other pending claims for the task are rejected.
3. **completed** — The hunter submits a `Proof`, and the poster approves the completion.
4. **done** — The hunter confirms that payment has been received.

Once a task is **completed** or **done**, both the poster and the hunter can each leave one `Review` of the other.

> The `closed` status is defined on the model but is not currently used by the application.

## Notes on payment and currency

Payment is handled **outside the application** (for example, cash or e-wallet). BountyBoard does not process or hold funds; it only tracks the task, its claims, proof of completion, and the resulting reviews. All bounty amounts are expressed in **Malaysian Ringgit (RM / MYR)**.
