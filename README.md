# BountyBoard

BountyBoard is a campus-based student task marketplace built with Django. Students can post small paid tasks, hunters can claim or bid on jobs, and both sides build trust through ratings.

Bounty amounts are listed in RM/MYR. BountyBoard does not process payments; students arrange payment outside the system.

## Project Concept

Posters create bounties with a deadline and cash reward. Hunters browse available tasks, claim or bid on them, complete the work, submit proof, and receive reviews after completion.

Example bounties:

- Print and deliver an assignment to Block C for RM10
- Debug a Python or Django error for RM30
- Take campus portfolio photos for RM20
- Buy food from the cafe and deliver it to the library for RM8 plus meal cost
- Summarize journal articles for a literature review for RM15

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Django templates |
| Database | SQLite |
| Authentication | Django authentication system |
| Media Uploads | Django media files |

## User Roles

| Role | Description |
| --- | --- |
| Poster | Posts tasks, sets bounty amounts, approves completion, reviews hunters |
| Hunter | Browses jobs, claims tasks, submits completion proof, earns reputation |
| Admin | Moderates users, tasks, categories, and platform activity |

## Core Features

- User registration, login, logout, and profile management
- Poster and Hunter profile roles
- Task posting with title, description, bounty, category, deadline, and status
- RM/MYR bounty display with payment handled outside the platform
- Open task browsing and category filtering
- Bids or claim messages from hunters
- Task completion proof uploads
- Reviews and ratings between users
- Django admin panel for moderation

## Task Categories

- Delivery
- Coding Help
- Design
- Tutoring
- Errands
- Photography
- Other

## Current Project Structure

```text
bountyboard/
├── core/              # Django project settings and root URLs
├── tasks/             # Task, bid, and review models
├── users/             # User profile models
├── docs/              # Project documentation
├── manage.py
├── README.md
└── .gitignore
```

## Database Overview

Main data models:

- User: provided by Django auth
- Profile: rating, bio, avatar
- Task: poster, hunter, title, description, bounty, category, status, deadline, proof image
- Bid: task, hunter, message, timestamp
- Review: task, reviewer, reviewee, rating, comment

## App Flow

```text
Home -> Browse open bounties
Search -> Filter by category, bounty, and deadline
Post Task -> Create a campus bounty
Task Detail -> View details, bid, claim, or submit proof
Profile -> View posted tasks, completed jobs, and rating
Admin Panel -> Manage users, tasks, reviews, and moderation
```

## Local Setup

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies and build the CSS:

```bash
npm install
npm run build
```

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

Open the Django admin at:

```text
http://127.0.0.1:8000/admin/
```

## Docker Setup

Build and start the app with Docker Compose:

```bash
docker compose up --build
```

If port `8000` is already in use, run it on another port:

```bash
APP_PORT=8001 docker compose up --build
```

Open the app at:

```text
http://localhost:8000/
```

If you used `APP_PORT=8001`, open:

```text
http://localhost:8001/
```

Open the Django admin at:

```text
http://localhost:8000/admin/
```

Create an admin user inside the running container:

```bash
docker compose exec web python manage.py createsuperuser
```

Stop the Docker containers:

```bash
docker compose down
```

The Docker setup uses SQLite stored in the `sqlite_data` Docker volume.

## Development Notes

- This project uses SQLite for local development.
- Uploaded media files are stored under `media/` and should not be committed.
- The local virtual environment should stay outside version control.
- Keep business logic simple and demo-friendly for coursework presentation.
