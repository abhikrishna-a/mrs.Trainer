import json
import os
import random
from django.core.management.base import BaseCommand
from quizzes.models import Role, Topic, Question, AnswerOption, StarterCode, TestCase

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data")

ROLES_DATA = [
    {"name": "Quantitative Aptitude", "slug": "quantitative", "icon": "Q"},
    {"name": "Logical Reasoning", "slug": "logical-reasoning", "icon": "L"},
    {"name": "Python Programming", "slug": "python", "icon": "Py"},
    {"name": "Data Structures & Algorithms", "slug": "dsa", "icon": "DS"},
]

TOPIC_DATA = {
    "quantitative": [
        ("Algebra", "ALG", "A"),
        ("Arithmetic", "ART", "B"),
        ("Geometry", "GEO", "C"),
        ("Number Theory", "NUM", "D"),
        ("Probability & Stats", "PRB", "E"),
    ],
    "logical-reasoning": [
        ("Series Completion", "SER", "F"),
        ("Syllogisms", "SYL", "G"),
        ("Blood Relations", "BLD", "H"),
        ("Direction Sense", "DIR", "I"),
        ("Puzzles", "PZZ", "J"),
    ],
    "python": [
        ("Basics", "PYB", "K"),
        ("Data Types", "PYD", "L"),
        ("OOP", "PYO", "M"),
        ("File Handling", "PYF", "N"),
        ("Libraries", "PYL", "O"),
    ],
    "dsa": [
        ("Arrays", "ARR", "U"),
        ("Linked Lists", "LNK", "V"),
        ("Trees", "TRE", "W"),
        ("Graphs", "GRF", "X"),
        ("Dynamic Programming", "DYN", "Y"),
    ],
}

FILENAME_TOPIC_MAP = {
    "algebra": "Algebra",
    "arithmetic": "Arithmetic",
    "geometry": "Geometry",
    "number_theory": "Number Theory",
    "probability_stats": "Probability & Stats",
    "series_completion": "Series Completion",
    "syllogisms": "Syllogisms",
    "blood_relations": "Blood Relations",
    "direction_sense": "Direction Sense",
    "puzzles": "Puzzles",
    "arrays": "Arrays",
    "linked_lists": "Linked Lists",
    "trees": "Trees",
    "graphs": "Graphs",
    "dynamic_programming": "Dynamic Programming",
    "basics": "Basics",
    "data_types": "Data Types",
    "oop": "OOP",
    "file_handling": "File Handling",
    "libraries": "Libraries",
    "python_basics": "Basics",
    "python_data_types": "Data Types",
    "python_oop": "OOP",
    "python_file_handling": "File Handling",
    "python_libraries": "Libraries",
}


def _filename_to_topic_name(filename):
    name = filename.replace(".json", "")
    return FILENAME_TOPIC_MAP.get(name, name.replace("_", " ").title())


class Command(BaseCommand):
    help = "Seed questions from curated fixture files"

    def handle(self, *args, **options):
        Question.objects.all().delete()

        for rd in ROLES_DATA:
            Role.objects.get_or_create(
                slug=rd["slug"],
                defaults={"name": rd["name"], "description": f"{rd['name']} questions"},
            )

        self._create_topics()
        mcq_count = self._load_mcq_fixtures()
        coding_count = self._load_coding_fixtures()
        total = Question.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {total} questions ({mcq_count} MCQ, {coding_count} coding) across "
                f"{Topic.objects.count()} topics."
            )
        )

    def _create_topics(self):
        for role_slug, tlist in TOPIC_DATA.items():
            role = Role.objects.get(slug=role_slug)
            for i, (name, short, icon) in enumerate(tlist):
                Topic.objects.get_or_create(
                    role=role,
                    name=name,
                    defaults={"short_name": short, "icon": icon, "order": i},
                )

    def _load_mcq_fixtures(self):
        mcq_dir = os.path.join(FIXTURES_DIR, "mcq")
        if not os.path.isdir(mcq_dir):
            return 0
        count = 0
        for fname in sorted(os.listdir(mcq_dir)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(mcq_dir, fname)
            with open(path, encoding="utf-8") as f:
                questions_data = json.load(f)

            topic_name = _filename_to_topic_name(fname)
            try:
                topic = Topic.objects.get(name__iexact=topic_name)
            except Topic.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Topic '{topic_name}' not found, skipping {fname}")
                )
                continue

            for q_data in questions_data:
                slug = self._make_slug(topic, q_data["title"])
                q = Question.objects.create(
                    topic=topic,
                    title=q_data["title"],
                    slug=slug,
                    text=q_data["text"],
                    explanation=q_data.get("explanation", ""),
                    difficulty=q_data["difficulty"],
                    question_type="mcq",
                )
                options = list(q_data["options"])
                random.shuffle(options)
                for i, opt in enumerate(options):
                    AnswerOption.objects.create(
                        question=q,
                        text=opt["text"],
                        is_correct=opt["is_correct"],
                        order=i,
                    )
                count += 1
        return count

    def _load_coding_fixtures(self):
        coding_dir = os.path.join(FIXTURES_DIR, "coding")
        if not os.path.isdir(coding_dir):
            return 0
        count = 0
        for fname in sorted(os.listdir(coding_dir)):
            if not fname.endswith(".json"):
                continue
            path = os.path.join(coding_dir, fname)
            with open(path, encoding="utf-8") as f:
                problems_data = json.load(f)

            topic_name = _filename_to_topic_name(fname)
            try:
                topic = Topic.objects.get(name__iexact=topic_name)
            except Topic.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f"Topic '{topic_name}' not found, skipping {fname}")
                )
                continue

            for p_data in problems_data:
                slug = self._make_slug(topic, p_data["title"])
                q = Question.objects.create(
                    topic=topic,
                    title=p_data["title"],
                    slug=slug,
                    text=p_data["text"],
                    difficulty=p_data["difficulty"],
                    question_type="coding",
                )
                StarterCode.objects.create(
                    question=q,
                    python_code=p_data["starter_code"],
                )
                for i, tc in enumerate(p_data["test_cases"]):
                    TestCase.objects.create(
                        question=q,
                        stdin=tc["stdin"],
                        expected_output=tc["expected_output"],
                        is_hidden=tc.get("is_hidden", False),
                        order=tc.get("order", i),
                    )
                count += 1
        return count

    def _make_slug(self, topic, title):
        base = f"{topic.short_name.lower()}-{title.lower().replace(' ', '-')}"
        base = "".join(c for c in base if c.isalnum() or c == "-")[:100]
        slug = base
        counter = 1
        while Question.objects.filter(slug=slug).exists():
            counter += 1
            slug = f"{base}-{counter}"
        return slug
