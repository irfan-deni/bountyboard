import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from tasks.models import Review, Task
from users.models import Profile


# Default password applied to any demo user we create for the first time.
DEMO_PASSWORD = "demo12345"

# Demo students: (username, first_name, email, phone, bio).
DEMO_USERS = [
    (
        "alya",
        "Alya",
        "alya@demo.unikl.my",
        "+60 12-345 6789",
        "Final-year student who always has errands to delegate.",
    ),
    (
        "hafiz",
        "Hafiz",
        "hafiz@demo.unikl.my",
        "+60 13-234 5678",
        "Club committee member, posts media and design gigs.",
    ),
    (
        "mei",
        "Mei",
        "mei@demo.unikl.my",
        "+60 11-2345 6789",
        "",
    ),
    (
        "daniel",
        "Daniel",
        "daniel@demo.unikl.my",
        "+60 16-987 6543",
        "New on campus and keen to pick up quick tasks.",
    ),
    (
        "nurin",
        "Nurin",
        "nurin@demo.unikl.my",
        "+60 17-555 1234",
        "Loves delivery runs between classes.",
    ),
    (
        "ahmad",
        "Ahmad",
        "ahmad@demo.unikl.my",
        "+60 19-321 7788",
        "",
    ),
    (
        "priya",
        "Priya",
        "priya@demo.unikl.my",
        "+60 14-678 9900",
        "Happy to debug Django and Python issues for fellow students.",
    ),
]

# Demo tasks: (title, description, category, bounty, deadline_in_days).
# Status and hunter assignment are handled in handle().
DEMO_TASKS = [
    (
        "Print 20 pages & deliver to Dewan Sri Wawasan",
        "Need 20 pages printed (black and white) and hand-delivered to the "
        "registration desk at Dewan Sri Wawasan before the event starts.",
        "delivery",
        "5.00",
        2,
    ),
    (
        "Debug a Django view error",
        "My Django task detail view throws a 500 error on submit. Looking for "
        "someone to find the bug and explain the fix over a quick call.",
        "coding",
        "30.00",
        5,
    ),
    (
        "Take portfolio photos around campus",
        "Looking for someone to shoot 15-20 candid and posed portfolio photos "
        "around campus landmarks. Bring your own camera.",
        "photography",
        "20.00",
        7,
    ),
    (
        "Buy lunch from cafe & deliver to library",
        "Buy a set lunch from the main cafe and drop it off at the library "
        "level 2 study area. RM8 service fee plus the meal cost reimbursed.",
        "delivery",
        "8.00",
        1,
    ),
    (
        "Summarize three journal articles",
        "Read three short journal articles (PDFs provided) and write a one-page "
        "summary of each with key findings and takeaways.",
        "tutoring",
        "15.00",
        4,
    ),
]


class Command(BaseCommand):
    help = "Seed realistic demo data for BountyBoard (idempotent)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Delete existing demo data (reviews, tasks, profiles, and "
            "non-superuser users) before seeding.",
        )

    def _flush(self):
        Review.objects.all().delete()
        Task.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

    @transaction.atomic
    def handle(self, *args, **options):
        if options["fresh"]:
            self._flush()

        # ------------------------------------------------------------- users
        users = {}
        for username, first_name, email, phone, bio in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first_name, "email": email},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()

            Profile.objects.update_or_create(
                user=user,
                defaults={"phone": phone, "bio": bio},
            )
            users[username] = user

        usernames = [row[0] for row in DEMO_USERS]

        # ------------------------------------------------------------- tasks
        # Cycle posters across the demo users; mark one task completed and one
        # claimed, each with a hunter who is not the poster, rest stay open.
        tasks = []
        for index, (title, description, category, bounty, days) in enumerate(DEMO_TASKS):
            poster = users[usernames[index % len(usernames)]]

            if index == 0:
                status = "completed"
            elif index == 1:
                status = "claimed"
            else:
                status = "open"

            hunter = None
            if status in ("claimed", "completed"):
                for candidate_username in usernames:
                    candidate = users[candidate_username]
                    if candidate != poster:
                        hunter = candidate
                        break

            task, _ = Task.objects.get_or_create(
                title=title,
                defaults={
                    "poster": poster,
                    "hunter": hunter,
                    "description": description,
                    "category": category,
                    "bounty": bounty,
                    "status": status,
                    "deadline": timezone.now() + datetime.timedelta(days=days),
                },
            )
            tasks.append(task)

        # ----------------------------------------------------------- reviews
        # One review left by the poster for the hunter on the completed task.
        completed_task = tasks[0]
        if completed_task.hunter is not None:
            Review.objects.get_or_create(
                task=completed_task,
                reviewer=completed_task.poster,
                reviewee=completed_task.hunter,
                defaults={
                    "rating": 5,
                    "comment": "Delivered everything on time and was easy to deal "
                    "with. Would hire again!",
                },
            )

        # ------------------------------------------------------------ report
        self.stdout.write(
            self.style.SUCCESS(
                "Demo data seeded (idempotent). "
                "Users: {users} | Profiles: {profiles} | Tasks: {tasks} "
                "(open={open}, claimed={claimed}, completed={completed}) | "
                "Reviews: {reviews} | Demo password: '{password}'".format(
                    users=User.objects.filter(is_superuser=False).count(),
                    profiles=Profile.objects.count(),
                    tasks=Task.objects.count(),
                    open=Task.objects.filter(status="open").count(),
                    claimed=Task.objects.filter(status="claimed").count(),
                    completed=Task.objects.filter(status="completed").count(),
                    reviews=Review.objects.count(),
                    password=DEMO_PASSWORD,
                )
            )
        )
