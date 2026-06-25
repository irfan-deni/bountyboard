# BountyBoard Requirements

This document defines the required features for the BountyBoard Django project.

## Product Summary

BountyBoard is a campus micro-job marketplace where students post paid tasks and other students complete them. The platform should be easy to demo, visually engaging, and focused on student use cases.

## User Roles

| Role | Requirements |
| --- | --- |
| Poster | Can create tasks, view their posted tasks, approve work, and review hunters |
| Hunter | Can browse tasks, bid or claim tasks, submit proof, earn XP, and receive reviews |
| Admin | Can manage users, tasks, categories, reviews, and moderation through Django admin |

## Functional Requirements

### Authentication

- Users can register an account.
- Users can log in and log out.
- Users have a profile linked to their Django auth user.
- Each profile has a role: Poster or Hunter.

### Profiles

- Profiles must show username, role, rank, XP, rating, bio, avatar, and badges.
- Hunters should show claimed or completed tasks.
- Posters should show posted tasks.
- Ratings should help other users judge trustworthiness.

### Task Posting

- Posters can create a task with title, description, bounty amount, category, and deadline.
- Tasks start with an Open status.
- Posters can view and manage their own tasks.

### Task Browsing

- Users can browse open tasks.
- Users can filter or search by category, bounty amount, and deadline.
- Task cards should clearly show title, bounty, category, deadline, and status.

### Bidding and Claiming

- Hunters can submit a bid or claim message for an open task.
- A task can store the selected hunter once assigned.
- Claimed tasks should no longer appear as open for other hunters.

### Proof Submission

- Hunters can submit proof of completion, such as an uploaded image.
- Posters can review the proof before approving completion.
- Completed tasks should update the hunter's XP and progress.

### Reviews

- Posters can review hunters after task completion.
- Hunters can review posters after task completion if implemented.
- Reviews include a 1 to 5 rating and a written comment.
- Profile rating should be based on received reviews.

### Gamification

- Hunters earn XP from completed jobs.
- Hunter ranks should progress from Novice to Apprentice, Expert, and Elite Hunter.
- Badges should be awarded for achievements such as reliability, speed, and category specialization.
- A leaderboard should show top hunters by XP, completed tasks, or weekly activity.

### Admin Moderation

- Admins can manage users and profiles.
- Admins can manage tasks, bids, reviews, and badges.
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

- Home page with open bounties and featured leaderboard
- Search or browse page with filters
- Task creation page
- Task detail page
- Profile page
- Leaderboard page
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
- A poster can create a task with a bounty and deadline.
- A hunter can browse open tasks and bid or claim one.
- A task can move from Open to Claimed to Completed.
- A completed task can receive a review.
- Hunter XP, rank, badges, or leaderboard data can be displayed.
- Admin users can moderate core records through Django admin.
