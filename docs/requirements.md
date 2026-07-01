# BountyBoard Requirements

This document defines the required features for the BountyBoard Django project.

## Product Summary

BountyBoard is a campus micro-job marketplace where students post paid tasks and other students complete them. The platform should be easy to demo, visually engaging, and focused on student use cases.

## User Roles

| Role | Requirements |
| --- | --- |
| Student | Can browse bounties, post tasks with RM/MYR bounty amounts, claim tasks, submit proof, and receive reviews |
| Admin | Can manage users, tasks, reviews, and moderation through Django admin |

Poster and Hunter are task-based labels, not separate account types. A student is the poster for tasks they create and the hunter for tasks they claim.

## Functional Requirements

### Authentication

- Users can register an account.
- Users can log in and log out.
- Users have a profile linked to their Django auth user.
- Students use one account and can act as poster or hunter depending on the task.

### Profiles

- Profiles should show username, rating, bio, and avatar when those features are available.
- Hunters should show claimed or completed tasks.
- Posters should show posted tasks.
- Ratings should help other users judge trustworthiness.

### Task Posting

- Logged-in students can create a task with title, description, bounty amount, category, and deadline.
- Tasks start with an Open status.
- Students can view and manage tasks they created.

### Bounty Amount and Payment

- Task creators must set a bounty amount in RM/MYR.
- The bounty amount is displayed clearly on task cards and task detail pages.
- BountyBoard does not process, hold, or transfer money.
- Payment is handled outside the system between the task creator and the assigned student.
- Outside payment methods can include cash, bank transfer, TNG eWallet, DuitNow, or any method both students agree on.
- The platform only tracks the task, claim status, proof, completion, and reviews.

### Task Browsing

- Users can browse open tasks.
- Users can filter or search by category, bounty amount, and deadline.
- Task cards should clearly show title, bounty, category, deadline, and status.

### Bidding and Claiming

- Logged-in students can submit a claim message for open tasks they did not create.
- A task can store the selected hunter once assigned.
- Claimed tasks should no longer appear as open for other hunters.

### Proof Submission

- The assigned student can submit proof of completion, such as an uploaded image.
- The task creator can review the proof before approving completion.
- Completed tasks should update the hunter's progress.

### Reviews

- Students can review each other after task completion.
- Reviews include a 1 to 5 rating and a written comment.
- Profile rating should be based on received reviews.

### Admin Moderation

- Admins can manage users and profiles.
- Admins can manage tasks, bids, and reviews.
- Admins can remove inappropriate listings or problematic users.

## Non-Functional Requirements

- Use Django as the backend framework.
- Use SQLite for local development.
- Use Django templates with HTML, CSS, and JavaScript for the frontend.
- Use Django's built-in authentication system.
- Keep pages responsive for desktop and mobile screens.
- Validate user input on forms.
- Keep implementation simple enough for coursework demonstration.
- Do not commit local databases, media uploads, virtual environments, or secrets.

## Suggested Pages

- Home page with open bounties
- Search or browse page with filters
- Task creation page
- Task detail page
- Profile page
- Login and registration pages
- Admin panel

## Suggested Demo Data

- Print 20 pages and deliver to Dewan Sri Wawasan for RM5
- Debug a Django view error for RM30
- Take portfolio photos around campus for RM20
- Buy lunch from the cafe and deliver to the library for RM8 plus meal cost
- Summarize three journal articles for RM15

## Acceptance Criteria

- A user can register, log in, and view a profile.
- A student can create a task with a bounty amount in RM/MYR and a deadline.
- A student can browse open tasks and claim one they did not create.
- A task can move from Open to Claimed to Completed.
- A completed task can receive a review.
- The system clearly states that payment is handled outside BountyBoard.
- Hunter reputation and progress data can be displayed as an enhancement.
- Admin users can moderate core records through Django admin.
