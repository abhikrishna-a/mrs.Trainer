import random
import math
from django.core.management.base import BaseCommand
from quizzes.models import Role, Topic, Question, AnswerOption, StarterCode, TestCase

# ─── Question text templates ──────────────────────────────

MCQ_TEMPLATES = {
    "quantitative": [
        "If x + {a} = {b}, what is the value of x?",
        "What is {a}% of {b}?",
        "Simplify: {a} + {b} * {c} - {d}",
        "A train travels {a} km in {b} hours. What is its speed in km/h?",
        "Find the average of {a}, {b}, and {c}.",
        "If the ratio of two numbers is {a}:{b} and their sum is {c}, find the larger number.",
        "What is the probability of rolling a {a} on a fair six-sided die?",
        "If an item costs Rs.{a} and is sold at a {b}% profit, what is the selling price?",
        "How many distinct ways can {a} books be arranged on a shelf?",
        "The simple interest on Rs.{a} at {b}% per annum for {c} years is:",
    ],
    "logical-reasoning": [
        "Find the next term in the series: {a}, {b}, {c}, {d}, ?",
        "All {A} are {B}. Some {B} are {C}. Therefore:",
        "If '{a}' is coded as '{b}', how is '{c}' coded?",
        "Pointing to a man, a woman said, 'He is the son of my mother's only daughter.' How is the man related to the woman?",
        "A is the brother of B. B is the sister of C. How is A related to C?",
        "If a clock shows {a}:{b}, what is the angle between the hour and minute hands?",
        "Statement: {statement_1}. Conclusion: {conclusion}",
        "In a certain language, '{a}' means '{b}'. What does '{c}' mean?",
        "Which of the following does not belong to the group?",
        "If {a} > {b} and {b} > {c}, then:",
    ],
    "python": [
        "What is the output of `print(type([]))`?",
        "Which of the following is a mutable data type in Python?",
        "What will be the result of `{list_expr}`?",
        "Which keyword is used to define a function in Python?",
        "What does the `len()` function return for an empty list?",
        "Which of the following correctly handles an exception in Python?",
        "What is the output of `print(2 ** {a})`?",
        "Which method is used to add an element to a set?",
        "What will `'{a},{b},{c}'.split(',')` return?",
        "Which of the following creates a list comprehension?",
    ],
    "dsa": [
        "What is the time complexity of binary search on a sorted array of {a} elements?",
        "Which data structure operates on a LIFO principle?",
        "What is the minimum number of nodes in a complete binary tree of height {a}?",
        "Which sorting algorithm has the best average-case time complexity?",
        "How many edges does a graph with {a} vertices have if it is a tree?",
        "What is the output of an in-order traversal of this binary tree?",
        "Which data structure is best for implementing a priority queue?",
        "What is the worst-case time complexity of quicksort?",
        "A hash table with {a} slots uses linear probing. How many collisions occur for keys {b}?",
        "What is the space complexity of depth-first search?",
    ],
}

CODING_TEMPLATES = {
    "python": [
        "Write a function `solve()` that returns the sum of all even numbers from 1 to {a}.",
        "Implement `solve()` to check whether a given string is a palindrome.",
        "Write `solve()` that finds the factorial of {a} using recursion.",
        "Implement `solve()` to return the {a}th Fibonacci number.",
        "Write `solve()` that counts the number of vowels in a given string.",
    ],
    "dsa": [
        "Implement `solve()` to reverse a linked list.",
        "Write `solve()` to find the maximum subarray sum (Kadane's algorithm).",
        "Implement `solve()` to merge two sorted arrays.",
        "Write `solve()` to detect a cycle in a linked list.",
        "Implement `solve()` to perform level-order traversal of a binary tree.",
    ],
}

def _pick_template(templates, topic_name):
    pool = templates.get(topic_name, templates.get(list(templates.keys())[0], []))
    return random.choice(pool)

# ─── Distribution constants ──────────────────────────────
# Full (JS coding available): 1000 total
# No-JS-coding: 898 total

ROLES_DATA = [
    {"name": "Quantitative Aptitude", "slug": "quantitative", "icon": "Q"},
    {"name": "Logical Reasoning", "slug": "logical-reasoning", "icon": "L"},
    {"name": "Python Programming", "slug": "python", "icon": "Py"},
    {"name": "Data Structures & Algorithms", "slug": "dsa", "icon": "DS"},
]

# Per-role counts: (mcq_count, coding_count)
FULL_DISTRIBUTION = {
    "quantitative": (193, 0),
    "logical-reasoning": (182, 0),
    "python": (111, 117),
    "dsa": (60, 166),
}

# Difficulty split per category
DIFFICULTY_SPLIT = {"easy": 0.30, "medium": 0.40, "hard": 0.30}


def distribute_difficulty(count):
    easy = math.floor(count * DIFFICULTY_SPLIT["easy"])
    hard = math.floor(count * DIFFICULTY_SPLIT["hard"])
    medium = count - easy - hard
    return {"easy": easy, "medium": medium, "hard": hard}


class Command(BaseCommand):
    help = "Seed questions for the aptitude platform"

    def handle(self, *args, **options):
        distribution = FULL_DISTRIBUTION
        total = sum(sum(v) for v in distribution.values())

        self.stdout.write(f"Seeding {total} questions...")

        for rd in ROLES_DATA:
            role, _ = Role.objects.get_or_create(
                slug=rd["slug"],
                defaults={"name": rd["name"], "description": f"{rd['name']} questions"},
            )

        topics = self._create_topics()
        self._create_questions(distribution, topics)

        self.stdout.write(self.style.SUCCESS(f"Seeded {Question.objects.count()} questions total."))

    def _create_topics(self):
        topic_data = {
            "quantitative": [
                ("Algebra", "ALG", "A"), ("Arithmetic", "ART", "B"),
                ("Geometry", "GEO", "C"), ("Number Theory", "NUM", "D"),
                ("Probability & Stats", "PRB", "E"),
            ],
            "logical-reasoning": [
                ("Series Completion", "SER", "F"), ("Syllogisms", "SYL", "G"),
                ("Blood Relations", "BLD", "H"), ("Direction Sense", "DIR", "I"),
                ("Puzzles", "PZZ", "J"),
            ],
            "python": [
                ("Basics", "PYB", "K"), ("Data Types", "PYD", "L"),
                ("OOP", "PYO", "M"), ("File Handling", "PYF", "N"),
                ("Libraries", "PYL", "O"),
            ],
            "dsa": [
                ("Arrays", "ARR", "U"), ("Linked Lists", "LNK", "V"),
                ("Trees", "TRE", "W"), ("Graphs", "GRF", "X"),
                ("Dynamic Programming", "DYN", "Y"),
            ],
        }

        topics = {}
        for role_slug, tlist in topic_data.items():
            role = Role.objects.get(slug=role_slug)
            for i, (name, short, icon) in enumerate(tlist):
                topic, _ = Topic.objects.get_or_create(
                    role=role, name=name,
                    defaults={"short_name": short, "icon": icon, "order": i},
                )
                topics.setdefault(role_slug, []).append(topic)
        return topics

    def _create_questions(self, distribution, topics):
        q_num = 0
        for role_slug, (mcq_count, coding_count) in distribution.items():
            role_topics = topics[role_slug]

            for qtype, count in [("mcq", mcq_count), ("coding", coding_count)]:
                if count == 0:
                    continue
                diffs = distribute_difficulty(count)
                topic_role_name = role_topics[0].role.name if role_topics else role_slug
                for diff, n in diffs.items():
                    for i in range(n):
                        q_num += 1
                        topic = random.choice(role_topics)
                        slug = f"{role_slug}-{qtype}-{diff}-{q_num}"
                        title = f"Q{q_num}: {diff.title()} {qtype.upper()}"

                        text = self._generate_question_text(
                            topic_name=topic.name,
                            topic_role_name=topic_role_name,
                            diff=diff, qtype=qtype, q_num=q_num
                        )

                        q = Question.objects.create(
                            topic=topic,
                            title=title,
                            slug=slug,
                            text=text,
                            difficulty=diff,
                            question_type=qtype,
                            order=q_num,
                        )

                        if qtype == "mcq":
                            self._create_mcq_options(q)
                        else:
                            self._create_coding(q)

    def _generate_question_text(self, topic_name, topic_role_name, diff, qtype, q_num):
        if qtype == "mcq":
            templates = MCQ_TEMPLATES.get(topic_role_name, list(MCQ_TEMPLATES.values())[0])
            template = random.choice(templates)
            a, b, c, d = random.randint(2, 99), random.randint(1, 500), random.randint(1, 50), random.randint(1, 20)
            return template.format(
                a=a, b=b, c=c, d=d,
                A=chr(65 + random.randint(0, 25)), B=chr(65 + random.randint(0, 25)), C=chr(65 + random.randint(0, 25)),
                list_expr=f"[x**2 for x in range({a})]",
                statement_1=f"All {chr(65 + random.randint(0, 25))}s are {chr(65 + random.randint(0, 25))}s",
                conclusion=f"Some {chr(65 + random.randint(0, 25))}s are {chr(65 + random.randint(0, 25))}s",
            )
        templates = CODING_TEMPLATES.get(topic_role_name, list(CODING_TEMPLATES.values())[0])
        template = random.choice(templates)
        return template.format(a=random.randint(5, 50))

    def _create_mcq_options(self, q):
        correct_idx = random.randint(0, 3)
        for i in range(4):
            AnswerOption.objects.create(
                question=q,
                text=f"Option {'ABCD'[i]}",
                is_correct=(i == correct_idx),
                order=i,
            )

    def _create_coding(self, q):
        StarterCode.objects.create(
            question=q,
            python_code="def solve():\n    pass\n",
        )
        for i in range(3):
            TestCase.objects.create(
                question=q,
                stdin="",
                expected_output=f"test output {i}"[:999],
                is_hidden=(i >= 2),
                order=i,
            )
