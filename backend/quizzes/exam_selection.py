import random
from django.db.models import Max, Q, F
from .models import Role, Topic, Question, ExamSession, ExamSessionQuestion, UserAttempt


def get_available_questions(user, role=None, exclude_ids=None):
    """Get questions ranked by recency (never-asked first)."""
    exclude_ids = exclude_ids or set()
    qs = Question.objects.filter(topic__role=role) if role else Question.objects.all()
    qs = qs.exclude(id__in=exclude_ids)

    qs = qs.annotate(
        last_asked=Max("attempts__created_at", filter=Q(attempts__user=user))
    ).order_by(F("last_asked").asc(nulls_first=True), "id")

    return list(qs)


def borrow_with_cap(user, roles, needed_per_role, cap=2, floor=4):
    """
    Borrow questions from rich roles to fill sparse ones.
    cap=2: max borrow per role. floor=4: if a role has fewer than this, borrow.
    """
    role_questions = {}
    role_avail = {}

    for role in roles:
        available = get_available_questions(user, role=role)
        role_avail[role] = available
        role_questions[role] = []

    # Fill each role up to needed_per_role
    for role in roles:
        needed = needed_per_role
        available = role_avail[role]

        if len(available) >= floor:
            # Role has enough — take from its own pool
            role_questions[role] = available[:needed]
        else:
            # Role is sparse — take what it has, borrow the rest
            role_questions[role] = available
            deficit = needed - len(role_questions[role])

            # Find donor roles (sorted by most available)
            donors = sorted(
                [r for r in roles if r != role and len(role_avail[r]) > needed_per_role],
                key=lambda r: len(role_avail[r]),
                reverse=True,
            )

            borrowed = 0
            for donor in donors:
                if borrowed >= deficit:
                    break
                donor_available = [q for q in role_avail[donor] if q not in role_questions[role]]
                take = min(cap, deficit - borrowed, len(donor_available))
                role_questions[role].extend(donor_available[:take])
                borrowed += take

    return role_questions


def select_full_mock_questions(user, total=30, per_role=6):
    """Select 30 questions: 6 per role, interleaved round-robin."""
    roles = list(Role.objects.all())
    if not roles:
        return []

    role_questions = borrow_with_cap(user, roles, per_role)

    # Round-robin interleaving
    selected = []
    max_len = max(len(qs) for qs in role_questions.values()) if role_questions else 0
    for i in range(max_len):
        for role in roles:
            qs = role_questions.get(role, [])
            if i < len(qs):
                selected.append(qs[i])

    return selected[:total]


def select_category_drill_questions(user, role, total=20):
    """Select up to 20 questions from a single role."""
    available = get_available_questions(user, role=role)
    return available[:total]


def start_exam(user, mode, role=None):
    """Create an ExamSession with selected questions."""
    if mode == "full_mock":
        questions = select_full_mock_questions(user)
    else:
        questions = select_category_drill_questions(user, role)

    session = ExamSession.objects.create(
        user=user,
        mode=mode,
        role=role,
        total_questions=len(questions),
    )

    for i, q in enumerate(questions):
        ExamSessionQuestion.objects.create(
            session=session,
            question=q,
            order=i,
        )

    return session
