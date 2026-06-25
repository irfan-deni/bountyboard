import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from tasks.models import Bid, Review, Task
from users.models import Badge, Profile

# Default password applied to any demo user we create for the first time.
DEMO_PASSWORD = "demo12345"

# XP -> rank tiers (kept in sync with users.models.Profile.RANK_CHOICES).
RANK_TIERS = [
    (1300, "elite"),
    (450, "expert"),
    (120, "apprentice"),
    (0, "novice"),
]


def rank_for_xp(xp):
    """Return the rank string matching an XP value."""
    for threshold, rank in RANK_TIERS:
        if xp >= threshold:
            return rank
    return "novice"


# Demo users: (username, first_name, email, role, xp, rating, bio).
# Posters keep default xp/rank; hunters get varied progression.
DEMO_USERS = [
    # Posters
    ("alya", "Alya", "alya@demo.unikl.my", "poster", 0, 4.7,
     "Final-year student who always has errands to delegate."),
    ("hafiz", "Hafiz", "hafiz@demo.unikl.my", "poster", 0, 4.5,
     "Club committee member posting design and media gigs."),
    ("mei", "Mei", "mei@demo.unikl.my", "poster", 0, 4.9,
     "Research assistant who outsources reading and admin work."),
    # Hunters
    ("daniel", "Daniel", "daniel@demo.unikl.my", "hunter", 0, 4.2,
     "New hunter eager to take on first few campus tasks."),
    ("nurin", "Nurin", "nurin@demo.unikl.my", "hunter", 120, 4.4,
     "Apprentice hunter who loves quick delivery runs."),
    ("ahmad", "Ahmad", "ahmad@demo.unikl.my", "hunter", 450, 4.6,
     "Expert coder happy to debug Django and Python issues."),
    ("priya", "Priya", "priya@demo.unikl.my", "hunter", 1300, 4.8,
     "Elite all-rounder with a strong track record on campus."),
]

# Demo tasks: (title, description, category, bounty, deadline_in_days, status).
# Status assignment of 'claimed'/'completed' tasks is handled in handle().
DEMO_TASKS = [
    (
        "Print 20 pages & deliver to Dewan Sri Wawasan",
        "Need 20 pages printed (black and white) and hand-delivered to the "
        "registration desk at Dewan Sri Wawasan before the event starts.",
        "delivery",
        "5.00",
        2,
        "open",
    ),
    (
        "Debug a Django view error",
        "My Django task detail view throws a 500 error on submit. Looking for "
        "someone to find the bug and explain the fix over a quick call.",
        "coding",
        "30.00",
        5,
        "completed",
    ),
    (
        "Take portfolio photos around campus",
        "Looking for a hunter to shoot 15-20 candid and posed portfolio photos "
        "around campus landmarks. Bring your own camera.",
        "photography",
        "20.00",
        7,
        "claimed",
    ),
    (
        "Buy lunch from cafe & deliver to library",
        "Buy a set lunch from the main cafe and drop it off at the library "
        "level 2 study area. RM8 service fee plus the meal cost reimbursed.",
        "delivery",
        "8.00",
        1,
        "open",
    ),
    (
        "Summarize three journal articles",
        "Read three short journal articles (PDFs provided) and write a one-page "
        "summary of each with key findings and takeaways.",
        "tutoring",
        "15.00",
        4,
        "open",
    ),
]


class Command(BaseCommand):
    help = "Seed realistic demo data for BountyBoard (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        posters, hunters = self._seed_users()
        tasks = self._seed_tasks(posters, hunters)
        self._seed_bids(tasks, hunters)
        self._seed_reviews(tasks)
        self._seed_badges(hunters)
        self._report()

    # ------------------------------------------------------------------ users
    def _seed_users(self):
        posters = {}
        hunters = {}
        for (username, first_name, email, role, xp, rating, bio) in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"first_name": first_name, "email": email},
            )
            if created:
                user.set_password(DEMO_PASSWORD)
                user.save()

            Profile.objects.get_or_create(
                user=user,
                defaults={
                    "role": role,
                    "xp": xp,
                    "rank": rank_for_xp(xp),
                    "rating": rating,
                    "bio": bio,
                },
            )

            if role == "poster":
                posters[username] = user
            else:
                hunters[username] = user
        return posters, hunters

    # ------------------------------------------------------------------ tasks
    def _seed_tasks(self, posters, hunters):
        poster_cycle = list(posters.values())
        # A stable hunter to attach to claimed/completed tasks.
        assigned_hunter = hunters.get("priya") or next(iter(hunters.values()))

        tasks = {}
        for index, (title, description, category, bounty, days, status) in enumerate(
            DEMO_TASKS
        ):
            poster = poster_cycle[index % len(poster_cycle)]
            deadline = timezone.now() + datetime.timedelta(days=days)

            defaults = {
                "poster": poster,
                "description": description,
                "category": category,
                "bounty": bounty,
                "status": status,
                "deadline": deadline,
            }
            # Claimed and completed tasks need an assigned hunter.
            if status in ("claimed", "completed"):
                defaults["hunter"] = assigned_hunter

            task, _ = Task.objects.get_or_create(
                title=title,
                defaults=defaults,
            )
            tasks[title] = task
        return tasks

    # ------------------------------------------------------------------- bids
    def _seed_bids(self, tasks, hunters):
        # (task title, hunter username, message) for a couple of open tasks.
        bid_specs = [
            (
                "Print 20 pages & deliver to Dewan Sri Wawasan",
                "daniel",
                "I'm near the print shop now and can deliver within the hour.",
            ),
            (
                "Print 20 pages & deliver to Dewan Sri Wawasan",
                "nurin",
                "Happy to take this, I pass Dewan Sri Wawasan on my way.",
            ),
            (
                "Summarize three journal articles",
                "ahmad",
                "I summarize papers often and can turn this around by tomorrow.",
            ),
        ]
        for title, username, message in bid_specs:
            task = tasks.get(title)
            hunter = hunters.get(username)
            if task is None or hunter is None:
                continue
            Bid.objects.get_or_create(
                task=task,
                hunter=hunter,
                defaults={"message": message},
            )

    # ---------------------------------------------------------------- reviews
    def _seed_reviews(self, tasks):
        # Poster reviews the assigned hunter on the completed task.
        completed = tasks.get("Debug a Django view error")
        if completed is None or completed.hunter is None:
            return
        Review.objects.get_or_create(
            task=completed,
            reviewer=completed.poster,
            reviewee=completed.hunter,
            defaults={
                "rating": 5,
                "comment": "Found the bug fast and explained the fix clearly. "
                "Would hire again!",
            },
        )

    # ----------------------------------------------------------------- badges
    def _seed_badges(self, hunters):
        if not hunters:
            return
        # Award the 'Reliable' badge to the highest-XP hunter. Every demo user
        # gets a Profile in _seed_users, so look the winner up by XP directly.
        top_profile = (
            Profile.objects.filter(user__in=hunters.values())
            .order_by("-xp")
            .first()
        )
        if top_profile is None:
            return
        Badge.objects.get_or_create(
            profile=top_profile,
            name="Reliable",
            defaults={
                "description": "Consistently completes tasks on time with great reviews.",
            },
        )

    # ----------------------------------------------------------------- report
    def _report(self):
        self.stdout.write(self.style.SUCCESS("Demo data seeded (idempotent)."))
        self.stdout.write(
            self.style.SUCCESS(
                "Users: {users} | Profiles: {profiles} | Tasks: {tasks} "
                "(open={open}, claimed={claimed}, completed={completed}) | "
                "Bids: {bids} | Reviews: {reviews} | Badges: {badges}".format(
                    users=User.objects.count(),
                    profiles=Profile.objects.count(),
                    tasks=Task.objects.count(),
                    open=Task.objects.filter(status="open").count(),
                    claimed=Task.objects.filter(status="claimed").count(),
                    completed=Task.objects.filter(status="completed").count(),
                    bids=Bid.objects.count(),
                    reviews=Review.objects.count(),
                    badges=Badge.objects.count(),
                )
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Demo login password for seeded users: '%s'" % DEMO_PASSWORD
            )
        )
