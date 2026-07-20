"""Generate all remaining fixture files."""
import json, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seed_data")
MCQ_DIR = os.path.join(BASE, "mcq")
CODING_DIR = os.path.join(BASE, "coding")

TOPIC_MCQ_MAP = {
    "syllogisms": "Logical Reasoning",
    "direction_sense": "Direction Sense",
    "puzzles": "Puzzles",
}
TOPIC_CODING_MAP = {
    "linked_lists": "Linked Lists",
    "trees": "Trees",
    "graphs": "Graphs",
    "dynamic_programming": "Dynamic Programming",
    "basics": "Basics",
    "data_types": "Data Types",
    "oop": "OOP",
    "file_handling": "File Handling",
    "libraries": "Libraries",
}

MCQ_FILES_TO_CREATE = {
    "syllogisms", "direction_sense", "puzzles",
    "arrays", "linked_lists", "trees", "graphs", "dynamic_programming",
    "basics", "data_types", "oop", "file_handling", "libraries",
}
CODING_FILES_TO_CREATE = {
    "linked_lists", "trees", "graphs", "dynamic_programming",
    "basics", "data_types", "oop", "file_handling", "libraries",
}

# ─── MCQ CONTENT GENERATORS ──────────────────────────────────

def syllogisms():
    return [
        {
            "title": "Universal Affirmative",
            "text": "Statements:\nAll squares are rectangles.\nAll rectangles are quadrilaterals.\n\nWhich conclusion is definitely true?",
            "difficulty": "easy",
            "options": [
                {"text": "All squares are quadrilaterals", "is_correct": True},
                {"text": "All quadrilaterals are squares", "is_correct": False},
                {"text": "Some rectangles are not squares", "is_correct": False},
                {"text": "No square is a quadrilateral", "is_correct": False},
            ],
            "explanation": "If all A are B and all B are C, then all A are C (syllogism rule). So all squares are quadrilaterals. The converse (all quadrilaterals are squares) is false.",
        },
        {
            "title": "Universal Negative",
            "text": "Statements:\nNo bird is a mammal.\nAll bats are mammals.\n\nWhich conclusion is definitely true?",
            "difficulty": "easy",
            "options": [
                {"text": "No bat is a bird", "is_correct": True},
                {"text": "No mammal is a bat", "is_correct": False},
                {"text": "All bats are birds", "is_correct": False},
                {"text": "Some birds are bats", "is_correct": False},
            ],
            "explanation": "Bats are mammals (statement 2). No bird is a mammal (statement 1). Therefore, no bat can be a bird. 'No mammal is a bat' is false because bats are mammals.",
        },
        {
            "title": "Particular Affirmative",
            "text": "Statements:\nSome fruits are sweet.\nAll sweet things are tasty.\n\nWhich conclusion follows?",
            "difficulty": "medium",
            "options": [
                {"text": "Some fruits are tasty", "is_correct": True},
                {"text": "All fruits are tasty", "is_correct": False},
                {"text": "All tasty things are sweet", "is_correct": False},
                {"text": "No fruit is tasty", "is_correct": False},
            ],
            "explanation": "From 'some A are B' and 'all B are C', we can conclude 'some A are C'. Some fruits (which are sweet) must be tasty since all sweet things are tasty.",
        },
        {
            "title": "No Valid Conclusion",
            "text": "Statements:\nSome students are athletes.\nSome athletes are musicians.\n\nWhich conclusion follows?",
            "difficulty": "medium",
            "options": [
                {"text": "No definite conclusion", "is_correct": True},
                {"text": "Some students are musicians", "is_correct": False},
                {"text": "All athletes are students", "is_correct": False},
                {"text": "Some musicians are not students", "is_correct": False},
            ],
            "explanation": "With two 'some' statements, no definite relationship can be established between students and musicians. The overlapping groups might or might not intersect.",
        },
        {
            "title": "Complementary Pair",
            "text": "Statements:\nSome pens are pencils.\nSome pencils are erasers.\n\nWhich of the following is a complementary pair?",
            "difficulty": "hard",
            "options": [
                {"text": "Some pens are erasers AND No pen is an eraser", "is_correct": True},
                {"text": "All pens are erasers AND Some erasers are not pens", "is_correct": False},
                {"text": "Some pencils are pens AND No pencil is a pen", "is_correct": False},
                {"text": "All pencils are erasers AND Some erasers are pencils", "is_correct": False},
            ],
            "explanation": "With 'some A are B' and 'some B are C', the relationship between A and C is unknown. 'Some pens are erasers' and 'No pen is an eraser' form a complementary (either-or) pair where one must be true.",
        },
        {
            "title": "All and Some Negation",
            "text": "Statements:\nAll birds have feathers.\nSome animals with feathers cannot fly.\n\nWhich conclusion follows?",
            "difficulty": "medium",
            "options": [
                {"text": "Some birds cannot fly", "is_correct": False},
                {"text": "Some animals with feathers are birds", "is_correct": True},
                {"text": "No bird can fly", "is_correct": False},
                {"text": "All flying animals have feathers", "is_correct": False},
            ],
            "explanation": "All birds have feathers, so birds are a subset of 'animals with feathers'. Therefore, some animals with feathers are definitely birds. We cannot conclude anything about birds' ability to fly.",
        },
        {
            "title": "Only Statement",
            "text": "Statement:\nOnly intelligent students can solve this puzzle.\nRam solved the puzzle.\n\nWhich conclusion follows?",
            "difficulty": "medium",
            "options": [
                {"text": "Ram is intelligent", "is_correct": True},
                {"text": "Only Ram is intelligent", "is_correct": False},
                {"text": "No one else can solve the puzzle", "is_correct": False},
                {"text": "Ram is not intelligent", "is_correct": False},
            ],
            "explanation": "'Only X can do Y' means Y implies X (if Y then X). Since Ram solved the puzzle (Y is true), Ram must be intelligent (X is true).",
        },
        {
            "title": "Except Statement",
            "text": "Statement:\nAll students except those with backlogs can sit for placements.\nRavi has no backlogs.\n\nWhich conclusion follows?",
            "difficulty": "medium",
            "options": [
                {"text": "Ravi can sit for placements", "is_correct": True},
                {"text": "Ravi cannot sit for placements", "is_correct": False},
                {"text": "Only Ravi can sit for placements", "is_correct": False},
                {"text": "No one with backlogs can sit", "is_correct": False},
            ],
            "explanation": "'All except A are B' means if not A then B. Since Ravi has no backlogs (not A), he can sit for placements (B).",
        },
        {
            "title": "Venn Diagram Analysis",
            "text": "Statements:\nSome doctors are teachers.\nAll teachers are educated.\n\nWhich Venn diagram correctly represents the relationship?",
            "difficulty": "easy",
            "options": [
                {"text": "Doctors overlap with teachers, teachers inside educated", "is_correct": True},
                {"text": "Doctors and teachers are separate, both inside educated", "is_correct": False},
                {"text": "Teachers overlap with educated, doctors outside educated", "is_correct": False},
                {"text": "All three are completely separate", "is_correct": False},
            ],
            "explanation": "Some doctors are teachers (overlapping circles). All teachers are educated (teachers circle inside educated circle). Doctors may be partially or wholly inside educated.",
        },
        {
            "title": "Three Statements",
            "text": "Statements:\nAll A are B.\nNo B is C.\nSome C are D.\n\nWhich conclusion follows?",
            "difficulty": "hard",
            "options": [
                {"text": "No A is C", "is_correct": True},
                {"text": "Some A are D", "is_correct": False},
                {"text": "All A are D", "is_correct": False},
                {"text": "No B is D", "is_correct": False},
            ],
            "explanation": "All A are B, and no B is C. Therefore, no A is C (this is a valid syllogism: A\u2286B, B\u2229C=\u2205 \u2234 A\u2229C=\u2205). The relationship between A/C and D cannot be determined from the given statements.",
        },
    ]

def direction_sense():
    return [
        {
            "title": "Two Turns",
            "text": "Rohan starts walking north. He turns right, then right again. In which direction is he now facing?",
            "difficulty": "easy",
            "options": [
                {"text": "South", "is_correct": True},
                {"text": "North", "is_correct": False},
                {"text": "East", "is_correct": False},
                {"text": "West", "is_correct": False},
            ],
            "explanation": "Starting North \u2192 turn right (East) \u2192 turn right (South). Two right turns from North is South. The common mistake is confusing the direction after each turn.",
        },
        {
            "title": "Distance Calculation",
            "text": "A man walks 5 km east, then 3 km south, then 5 km west. How far is he from his starting point?",
            "difficulty": "medium",
            "options": [
                {"text": "3 km", "is_correct": True},
                {"text": "5 km", "is_correct": False},
                {"text": "13 km", "is_correct": False},
                {"text": "8 km", "is_correct": False},
            ],
            "explanation": "East 5 km then west 5 km cancels (net 0 east-west). He ends up 3 km south of the start. Distance = 3 km. Choosing 13 km adds all distances without considering cancellation.",
        },
        {
            "title": "Shadow Direction (Morning)",
            "text": "If a man is standing facing east in the morning, where does his shadow fall?",
            "difficulty": "easy",
            "options": [
                {"text": "Behind him (west)", "is_correct": True},
                {"text": "In front of him (east)", "is_correct": False},
                {"text": "To his left (north)", "is_correct": False},
                {"text": "To his right (south)", "is_correct": False},
            ],
            "explanation": "The sun rises in the east in the morning. If facing east, the sun is in front, so the shadow falls behind (west). The common mistake is thinking the sun is behind you when facing east.",
        },
        {
            "title": "Complex Path",
            "text": "A starts from a point, walks 2 km north, turns right and walks 3 km, then turns right and walks 2 km. How far and in which direction is A from the start?",
            "difficulty": "medium",
            "options": [
                {"text": "3 km east", "is_correct": True},
                {"text": "2 km west", "is_correct": False},
                {"text": "3 km west", "is_correct": False},
                {"text": "5 km east", "is_correct": False},
            ],
            "explanation": "North 2 km \u2192 right (East) 3 km \u2192 right (South) 2 km. The north and south movements cancel (2 km each). He is left 3 km east of the start. Choosing 5 km adds all distances. Choosing 3 km west reverses the direction.",
        },
        {
            "title": "Right Turn Confusion",
            "text": "Maya is facing southeast. She turns 135\u00b0 clockwise. Which direction is she facing now?",
            "difficulty": "hard",
            "options": [
                {"text": "West", "is_correct": True},
                {"text": "East", "is_correct": False},
                {"text": "North", "is_correct": False},
                {"text": "South", "is_correct": False},
            ],
            "explanation": "Clockwise from SE: SE \u2192 S (45\u00b0) \u2192 SW (90\u00b0) \u2192 W (135\u00b0). A 135\u00b0 clockwise turn from southeast faces west. The opposite mistake (anticlockwise) would give east.",
        },
        {
            "title": "Relative Direction",
            "text": "A is to the east of B. C is to the north of A. D is to the west of C. In which direction is D from B?",
            "difficulty": "hard",
            "options": [
                {"text": "North-west", "is_correct": False},
                {"text": "North-east", "is_correct": True},
                {"text": "South-west", "is_correct": False},
                {"text": "Cannot be determined", "is_correct": False},
            ],
            "explanation": "B at origin. A is east of B. C is north of A (so C is northeast of B). D is west of C (so D is north/north-east of B). D is to the northeast of B.",
        },
        {
            "title": "Three Right Turns",
            "text": "If a person is facing north and makes three consecutive right turns, which direction is he facing?",
            "difficulty": "easy",
            "options": [
                {"text": "West", "is_correct": True},
                {"text": "East", "is_correct": False},
                {"text": "North", "is_correct": False},
                {"text": "South", "is_correct": False},
            ],
            "explanation": "North \u2192 right (East) \u2192 right (South) \u2192 right (West). Three right turns is equivalent to one left turn from North, which faces West.",
        },
        {
            "title": "Meeting Point",
            "text": "P walks 5 m north, then 6 m east. Q walks 5 m south, then 4 m west. If both start from the same point, what is the distance between them?",
            "difficulty": "hard",
            "options": [
                {"text": "10\u221a2 m", "is_correct": True},
                {"text": "2\u221a61 m", "is_correct": False},
                {"text": "10\u221a6 m", "is_correct": False},
                {"text": "20 m", "is_correct": False},
            ],
            "explanation": "P ends at (6, 5) from origin (east, north). Q ends at (-4, -5). Difference = (10, 10). Distance = \u221a(10\u00b2 + 10\u00b2) = \u221a200 = 10\u221a2 m. Choosing 20 m naively adds the individual distances.",
        },
    ]

def puzzles_mcq():
    return [
        {
            "title": "Linear Seating",
            "text": "Five friends A, B, C, D, E sit in a row. A is at one end. B is to the immediate left of C. D is between A and E. Who is in the middle?",
            "difficulty": "medium",
            "options": [
                {"text": "E", "is_correct": True},
                {"text": "C", "is_correct": False},
                {"text": "D", "is_correct": False},
                {"text": "B", "is_correct": False},
            ],
            "explanation": "Let's solve: A at left end. D between A and E: A, D, E. B is immediate left of C: B, C. Combined: A, D, E, B, C. Middle position (3rd) is E. Common mistake is placing D in the middle.",
        },
        {
            "title": "Circular Seating",
            "text": "Four persons P, Q, R, S sit around a circular table facing the center. P sits to the immediate left of Q. R sits opposite P. Who sits to the immediate right of Q?",
            "difficulty": "medium",
            "options": [
                {"text": "S", "is_correct": True},
                {"text": "R", "is_correct": False},
                {"text": "Q", "is_correct": False},
                {"text": "P", "is_correct": False},
            ],
            "explanation": "P is immediately left of Q. With 4 persons around a circle and R opposite P, the only arrangement is Q, P, S, R (clockwise). Working clockwise from Q: P is left, then S, then R. S is to Q's immediate right.",
        },
        {
            "title": "Ordering by Height",
            "text": "U is taller than V. W is taller than X but shorter than V. Y is shorter than X. Who is the shortest?",
            "difficulty": "easy",
            "options": [
                {"text": "Y", "is_correct": True},
                {"text": "X", "is_correct": False},
                {"text": "V", "is_correct": False},
                {"text": "W", "is_correct": False},
            ],
            "explanation": "U > V > W > X > Y. Y is the shortest. Y is shorter than X, and X is shorter than W, and W is shorter than V, so Y is the shortest overall.",
        },
        {
            "title": "Blood Relations Puzzle",
            "text": "A is the father of B. C is the sister of A. D is the son of C. How is D related to B?",
            "difficulty": "easy",
            "options": [
                {"text": "Cousin", "is_correct": True},
                {"text": "Brother", "is_correct": False},
                {"text": "Nephew", "is_correct": False},
                {"text": "Uncle", "is_correct": False},
            ],
            "explanation": "A is B's father. C is A's sister (B's aunt). D is C's son. So D is B's first cousin. Choosing 'brother' confuses the cousin relationship with sibling.",
        },
        {
            "title": "Scheduling",
            "text": "Three exams - Math, Physics, Chemistry - are scheduled on Monday, Tuesday, Wednesday. Math is not on Wednesday. Physics is on Tuesday. On which day is Chemistry?",
            "difficulty": "easy",
            "options": [
                {"text": "Monday", "is_correct": False},
                {"text": "Wednesday", "is_correct": True},
                {"text": "Tuesday", "is_correct": False},
                {"text": "Cannot be determined", "is_correct": False},
            ],
            "explanation": "Physics = Tuesday. Math \u2260 Wednesday, so Math = Monday. Then Chemistry = Wednesday (only day left).",
        },
        {
            "title": "Truth Teller / Liar",
            "text": "In a room, two people say:\nX says: 'Y is a liar.'\nY says: 'X is a liar.'\nWhat can be concluded?",
            "difficulty": "hard",
            "options": [
                {"text": "Both are lying", "is_correct": False},
                {"text": "One is lying and one is telling the truth", "is_correct": True},
                {"text": "Both are telling the truth", "is_correct": False},
                {"text": "Cannot be determined", "is_correct": False},
            ],
            "explanation": "If X is truthful, then Y is a liar, so Y's statement 'X is a liar' is false (consistent). If X is lying, then Y is truthful, so Y's statement 'X is a liar' is true (consistent). Either way, one is truthful, one is lying.",
        },
        {
            "title": "Ranking Puzzle",
            "text": "In a class of 40 students, Ravi is 8th from the top. What is his rank from the bottom?",
            "difficulty": "easy",
            "options": [
                {"text": "33rd", "is_correct": True},
                {"text": "32nd", "is_correct": False},
                {"text": "34th", "is_correct": False},
                {"text": "31st", "is_correct": False},
            ],
            "explanation": "Rank from bottom = Total + 1 - Rank from top = 40 + 1 - 8 = 33. Choosing 32 forgets the +1 adjustment (40 - 8 = 32, rank from bottom should be 33).",
        },
        {
            "title": "Age Puzzle",
            "text": "Three years from now, Alex will be twice as old as Ben. Ben is currently 10 years old. How old is Alex now?",
            "difficulty": "easy",
            "options": [
                {"text": "17", "is_correct": False},
                {"text": "20", "is_correct": False},
                {"text": "23", "is_correct": True},
                {"text": "13", "is_correct": False},
            ],
            "explanation": "In 3 years, Ben will be 13. At that time, Alex = 2 \u00d7 13 = 26. So Alex is now 26 - 3 = 23. Choosing 17 arrives at Alex's age in 3 years without subtracting the 3 years back.",
        },
        {
            "title": "Complex Ordering",
            "text": "Five books are on a shelf. The red book is above the blue book. The green book is below the yellow book but above the red book. The black book is at the bottom. Which book is second from the top?",
            "difficulty": "hard",
            "options": [
                {"text": "Green", "is_correct": True},
                {"text": "Yellow", "is_correct": False},
                {"text": "Red", "is_correct": False},
                {"text": "Blue", "is_correct": False},
            ],
            "explanation": "Top to bottom: Yellow > Green > Red > Blue > Black. Second from top is Green. 'Green is below yellow but above red': Yellow > Green > Red. 'Red above blue': Red > Blue. 'Black at bottom': Black is last. So: Yellow, Green, Red, Blue, Black.",
        },
        {
            "title": "Day Puzzle",
            "text": "If the day after tomorrow is Thursday, what day was yesterday?",
            "difficulty": "medium",
            "options": [
                {"text": "Monday", "is_correct": True},
                {"text": "Sunday", "is_correct": False},
                {"text": "Tuesday", "is_correct": False},
                {"text": "Saturday", "is_correct": False},
            ],
            "explanation": "Day after tomorrow = Thursday means 2 days from now is Thursday. So today = Tuesday, and yesterday = Monday. A common mistake is counting forward from today incorrectly.",
        },
    ]

def arrays_mcq():
    return [
        {
            "title": "Array Index Access",
            "text": "In a 0-indexed array arr = [10, 20, 30, 40, 50], what is the value of arr[2]?",
            "difficulty": "easy",
            "options": [
                {"text": "30", "is_correct": True},
                {"text": "20", "is_correct": False},
                {"text": "40", "is_correct": False},
                {"text": "50", "is_correct": False},
            ],
            "explanation": "In 0-indexed arrays, arr[0]=10, arr[1]=20, arr[2]=30. The common 1-indexing mistake is to choose 20 (thinking index 2 means the second element).",
        },
        {
            "title": "Time Complexity - Linear Search",
            "text": "What is the worst-case time complexity of linear search in an array of N elements?",
            "difficulty": "easy",
            "options": [
                {"text": "O(N)", "is_correct": True},
                {"text": "O(1)", "is_correct": False},
                {"text": "O(log N)", "is_correct": False},
                {"text": "O(N\u00b2)", "is_correct": False},
            ],
            "explanation": "In the worst case, linear search examines all N elements (if the target is at the end or not present). So time complexity is O(N). O(log N) is binary search (requires sorted array).",
        },
        {
            "title": "Array Reversal",
            "text": "After reversing the array [1, 2, 3, 4, 5], what is the element at index 2?",
            "difficulty": "easy",
            "options": [
                {"text": "3", "is_correct": True},
                {"text": "2", "is_correct": False},
                {"text": "4", "is_correct": False},
                {"text": "5", "is_correct": False},
            ],
            "explanation": "Reversed array: [5, 4, 3, 2, 1]. Index 2 (0-indexed) = 3. Choosing 5 is arr[0] of reversed array. Choosing 2 is arr[3] of reversed.",
        },
        {
            "title": "Insertion Complexity",
            "text": "What is the time complexity of inserting an element at the beginning of an array (not a linked list)?",
            "difficulty": "medium",
            "options": [
                {"text": "O(1)", "is_correct": False},
                {"text": "O(N)", "is_correct": True},
                {"text": "O(log N)", "is_correct": False},
                {"text": "O(N\u00b2)", "is_correct": False},
            ],
            "explanation": "Inserting at the beginning requires shifting all existing elements right by one position, which takes O(N) time. This is a key difference between arrays and linked lists (where head insertion is O(1)).",
        },
        {
            "title": "Binary Search Precondition",
            "text": "Which precondition is necessary for binary search on an array?",
            "difficulty": "medium",
            "options": [
                {"text": "The array must be sorted", "is_correct": True},
                {"text": "The array must not contain duplicates", "is_correct": False},
                {"text": "The array must contain positive numbers only", "is_correct": False},
                {"text": "The array must have an even number of elements", "is_correct": False},
            ],
            "explanation": "Binary search requires the array to be sorted to work correctly. Without sorted order, the midpoint comparison cannot eliminate half the search space.",
        },
        {
            "title": "Subarray vs Subsequence",
            "text": "In array [1, 2, 3, 4], which of the following is a valid CONTIGUOUS subarray?",
            "difficulty": "medium",
            "options": [
                {"text": "[1, 3, 4]", "is_correct": False},
                {"text": "[2, 3, 4]", "is_correct": True},
                {"text": "[1, 4]", "is_correct": False},
                {"text": "[4, 1]", "is_correct": False},
            ],
            "explanation": "A contiguous subarray must maintain consecutive positions. [2, 3, 4] uses indices 1,2,3 (consecutive). [1, 3, 4] skips index 1 (value 2), so it's a subsequence but not a subarray.",
        },
        {
            "title": "Two-Dimensional Array Access",
            "text": "In a 3\u00d74 matrix stored in row-major order, how many elements are stored before the element at row 1, column 2 (0-indexed)?",
            "difficulty": "hard",
            "options": [
                {"text": "6", "is_correct": True},
                {"text": "5", "is_correct": False},
                {"text": "7", "is_correct": False},
                {"text": "4", "is_correct": False},
            ],
            "explanation": "In row-major, elements before (1,2) = 4 elements in row 0 + 2 elements in row 1 before column 2 = 4 + 2 = 6.",
        },
        {
            "title": "Stable Sorting",
            "text": "Which of the following sorting algorithms is STABLE (preserves relative order of equal elements)?",
            "difficulty": "medium",
            "options": [
                {"text": "Merge sort", "is_correct": True},
                {"text": "Quick sort", "is_correct": False},
                {"text": "Selection sort", "is_correct": False},
                {"text": "Heap sort", "is_correct": False},
            ],
            "explanation": "Merge sort is stable when implemented correctly (left subarray takes precedence on equal elements). Quick sort's partitioning is typically unstable. Selection sort swaps non-adjacent elements, breaking stability.",
        },
        {
            "title": "Two Sum Variant",
            "text": "Given sorted array [1, 2, 3, 4, 5], which approach finds if any pair sums to 7 in O(N) time?",
            "difficulty": "hard",
            "options": [
                {"text": "Two pointers (left=0, right=N-1)", "is_correct": True},
                {"text": "Brute force (check all pairs)", "is_correct": False},
                {"text": "Binary search for the complement", "is_correct": False},
                {"text": "Hash set (storing seen elements)", "is_correct": False},
            ],
            "explanation": "For a sorted array, the two-pointer technique (O(N)) is optimal: start left at 0, right at N-1, adjust based on sum comparison. Hash set (O(N) time, O(N) space) also works but uses extra space. Binary search for complement takes O(N log N).",
        },
        {
            "title": "Pivot in Rotated Array",
            "text": "In a rotated sorted array [4, 5, 6, 7, 0, 1, 2], which index is the pivot point (the smallest element)?",
            "difficulty": "medium",
            "options": [
                {"text": "Index 4 (value 0)", "is_correct": True},
                {"text": "Index 0 (value 4)", "is_correct": False},
                {"text": "Index 2 (value 6)", "is_correct": False},
                {"text": "Index 5 (value 1)", "is_correct": False},
            ],
            "explanation": "The pivot point in a rotated sorted array is where the smallest element is located (0 at index 4). This is where arr[i] < arr[i-1]. Choosing index 5 (value 1) is close but not the minimum.",
        },
    ]

def linked_lists_mcq():
    return [
        {
            "title": "Linked List Node Structure",
            "text": "What is the minimum number of fields required in a singly linked list node?",
            "difficulty": "easy",
            "options": [
                {"text": "2 (data, next pointer)", "is_correct": True},
                {"text": "1 (data only)", "is_correct": False},
                {"text": "3 (data, prev pointer, next pointer)", "is_correct": False},
                {"text": "2 (data, prev pointer)", "is_correct": False},
            ],
            "explanation": "A singly linked list node needs just data (the value) and a next pointer (reference to the next node). The prev pointer is only needed for doubly linked lists.",
        },
        {
            "title": "Head Insertion Complexity",
            "text": "What is the time complexity of inserting a node at the HEAD of a singly linked list?",
            "difficulty": "easy",
            "options": [
                {"text": "O(1)", "is_correct": True},
                {"text": "O(N)", "is_correct": False},
                {"text": "O(log N)", "is_correct": False},
                {"text": "O(N\u00b2)", "is_correct": False},
            ],
            "explanation": "Head insertion in a linked list is O(1): create the new node, point its next to the current head, update the head pointer. No traversal needed.",
        },
        {
            "title": "Tail Pointer Benefit",
            "text": "What advantage does maintaining a tail pointer provide in a singly linked list?",
            "difficulty": "medium",
            "options": [
                {"text": "O(1) insertion at the end", "is_correct": True},
                {"text": "O(1) deletion at the end", "is_correct": False},
                {"text": "O(1) access to any element", "is_correct": False},
                {"text": "O(1) reversal of the list", "is_correct": False},
            ],
            "explanation": "A tail pointer allows O(1) insertion at the end (append). Without it, you'd need O(N) traversal to find the last node. Deletion at the end still requires O(N) to find the second-to-last node.",
        },
        {
            "title": "Finding Middle Element",
            "text": "What is the optimal way to find the middle node of a singly linked list in one pass?",
            "difficulty": "medium",
            "options": [
                {"text": "Tortoise and hare (slow and fast pointers)", "is_correct": True},
                {"text": "Count nodes first, then traverse to middle", "is_correct": False},
                {"text": "Use an array to store all node addresses", "is_correct": False},
                {"text": "Recursively find the middle", "is_correct": False},
            ],
            "explanation": "The slow-fast pointer technique (tortoise moves 1 step, hare moves 2 steps) finds the middle in one pass without extra space. When hare reaches the end, slow is at the middle.",
        },
        {
            "title": "Linked List vs Array - Insertion",
            "text": "In which scenario does a linked list outperform an array?",
            "difficulty": "easy",
            "options": [
                {"text": "Frequent insertions in the middle", "is_correct": True},
                {"text": "Random access by index", "is_correct": False},
                {"text": "Memory locality during iteration", "is_correct": False},
                {"text": "Binary search", "is_correct": False},
            ],
            "explanation": "Linked lists excel at insertions in the middle: O(1) after reaching the position (vs O(N) for arrays due to shifting). Arrays are better for random access (O(1) vs O(N)).",
        },
        {
            "title": "Cycle Detection",
            "text": "Which algorithm is commonly used to detect a cycle in a linked list?",
            "difficulty": "medium",
            "options": [
                {"text": "Floyd's cycle detection (slow-fast)", "is_correct": True},
                {"text": "Binary search", "is_correct": False},
                {"text": "Merge sort", "is_correct": False},
                {"text": "Depth-first search", "is_correct": False},
            ],
            "explanation": "Floyd's cycle detection uses two pointers: slow (1 step) and fast (2 steps). If they meet, there's a cycle. This is O(N) time and O(1) space.",
        },
        {
            "title": "Doubly Linked List Deletion",
            "text": "In a doubly linked list, how many pointer updates are needed to delete a node (given a direct reference to the node)?",
            "difficulty": "hard",
            "options": [
                {"text": "2", "is_correct": True},
                {"text": "0", "is_correct": False},
                {"text": "4", "is_correct": False},
                {"text": "1", "is_correct": False},
            ],
            "explanation": "To delete a node in a doubly linked list: update prev.next = current.next, and next.prev = current.prev. That's 2 pointer updates. In a singly linked list, you'd need the previous node, requiring traversal.",
        },
        {
            "title": "Reversing a Linked List",
            "text": "What is the space complexity of iteratively reversing a singly linked list?",
            "difficulty": "easy",
            "options": [
                {"text": "O(1)", "is_correct": True},
                {"text": "O(N)", "is_correct": False},
                {"text": "O(log N)", "is_correct": False},
                {"text": "O(N\u00b2)", "is_correct": False},
            ],
            "explanation": "Iterative reversal uses 3 pointers (prev, curr, next), which is O(1) extra space. Recursive reversal uses O(N) stack space due to the call stack.",
        },
        {
            "title": "Skip List Purpose",
            "text": "What problem does a skip list solve in linked lists?",
            "difficulty": "hard",
            "options": [
                {"text": "Slow search in sorted linked lists", "is_correct": True},
                {"text": "Memory overhead of pointers", "is_correct": False},
                {"text": "Inability to store duplicate values", "is_correct": False},
                {"text": "Thread safety during concurrent access", "is_correct": False},
            ],
            "explanation": "Skip lists add multiple levels of 'express lanes' to speed up search in sorted linked lists, achieving O(log N) average search time instead of O(N).",
        },
        {
            "title": "LRU Cache Data Structure",
            "text": "Which data structure combination is typically used to implement an LRU cache?",
            "difficulty": "hard",
            "options": [
                {"text": "Doubly linked list + hash map", "is_correct": True},
                {"text": "Array + binary search tree", "is_correct": False},
                {"text": "Singly linked list + hash map", "is_correct": False},
                {"text": "Stack + queue", "is_correct": False},
            ],
            "explanation": "An LRU cache uses a doubly linked list (for O(1) move-to-front) and a hash map (for O(1) lookups by key). The doubly linked list allows the most recently used item to be moved to the head efficiently.",
        },
    ]

# Additional topic generators
def trees_mcq():
    return [
        {"title": "Binary Tree Maximum Children", "text": "What is the maximum number of children a node can have in a binary tree?", "difficulty": "easy", "options": [{"text": "2", "is_correct": True}, {"text": "1", "is_correct": False}, {"text": "3", "is_correct": False}, {"text": "Unlimited", "is_correct": False}], "explanation": "A binary tree restricts each node to at most 2 children (left and right). 'Binary' means 2-way branching."},
        {"title": "Tree Height", "text": "What is the height of a tree with a single node (the root)?", "difficulty": "easy", "options": [{"text": "0", "is_correct": True}, {"text": "1", "is_correct": False}, {"text": "2", "is_correct": False}, {"text": "Undefined", "is_correct": False}], "explanation": "The height of a tree with only a root node is 0 (counting edges) or 1 (counting nodes). Most commonly in CS, height = number of edges on longest path from root to leaf, which is 0 for a single node."},
        {"title": "BST Property", "text": "In a Binary Search Tree, where is the minimum value located?", "difficulty": "easy", "options": [{"text": "Leftmost node", "is_correct": True}, {"text": "Rightmost node", "is_correct": False}, {"text": "Root node", "is_correct": False}, {"text": "Any leaf node", "is_correct": False}], "explanation": "In a BST, all left subtree values are less than the root. The minimum is at the leftmost (deepest left) node. The maximum is at the rightmost node."},
        {"title": "Tree Traversal - Inorder", "text": "Which tree traversal visits nodes in ascending order in a BST?", "difficulty": "medium", "options": [{"text": "Inorder (left-root-right)", "is_correct": True}, {"text": "Preorder (root-left-right)", "is_correct": False}, {"text": "Postorder (left-right-root)", "is_correct": False}, {"text": "Level order (BFS)", "is_correct": False}], "explanation": "Inorder traversal of a BST visits left subtree (smaller), root, then right subtree (larger), resulting in sorted ascending order."},
        {"title": "Complete Binary Tree", "text": "A complete binary tree of height 3 (root at level 0) has at most how many nodes?", "difficulty": "medium", "options": [{"text": "15", "is_correct": True}, {"text": "7", "is_correct": False}, {"text": "14", "is_correct": False}, {"text": "8", "is_correct": False}], "explanation": "Maximum nodes in a complete binary tree of height h is 2^(h+1) - 1. For height 3: 2^4 - 1 = 15. Choosing 7 is for height 2."},
        {"title": "Heap Property", "text": "In a max-heap, where is the largest element always located?", "difficulty": "easy", "options": [{"text": "At the root", "is_correct": True}, {"text": "At a leaf", "is_correct": False}, {"text": "In the right subtree", "is_correct": False}, {"text": "At a random position", "is_correct": False}], "explanation": "In a max-heap, the heap property ensures the parent is always greater than or equal to its children. Therefore, the largest element must be at the root."},
        {"title": "AVL Tree Balance", "text": "In an AVL tree, what is the maximum allowed difference in height between left and right subtrees of any node?", "difficulty": "medium", "options": [{"text": "1", "is_correct": True}, {"text": "0", "is_correct": False}, {"text": "2", "is_correct": False}, {"text": "log N", "is_correct": False}], "explanation": "AVL trees maintain a balance factor (height difference) of at most 1 for every node. A difference of 0 would be too restrictive (perfectly balanced, hard to maintain)."},
        {"title": "DFS vs BFS", "text": "Which tree traversal uses a queue data structure?", "difficulty": "easy", "options": [{"text": "Level order (BFS)", "is_correct": True}, {"text": "Preorder (DFS)", "is_correct": False}, {"text": "Inorder (DFS)", "is_correct": False}, {"text": "Postorder (DFS)", "is_correct": False}], "explanation": "Level-order traversal (BFS) uses a queue — process a node, enqueue its children. DFS traversals (pre/in/post) use a stack (implicit call stack for recursion or explicit stack for iteration)."},
        {"title": "Trie Use Case", "text": "Which data structure is most efficient for autocomplete/search suggestions?", "difficulty": "medium", "options": [{"text": "Trie (prefix tree)", "is_correct": True}, {"text": "Binary Search Tree", "is_correct": False}, {"text": "Hash table", "is_correct": False}, {"text": "Array", "is_correct": False}], "explanation": "A trie provides O(L) prefix-based lookups (L = prefix length), making it ideal for autocomplete. Hash tables can't do prefix matching efficiently. BSTs would require O(L log N) string comparisons."},
        {"title": "Diameter of Tree", "text": "The diameter of a tree is defined as the:", "difficulty": "hard", "options": [{"text": "Longest path between any two nodes", "is_correct": True}, {"text": "Height of the root node", "is_correct": False}, {"text": "Number of leaf nodes", "is_correct": False}, {"text": "Number of edges from root to deepest leaf", "is_correct": False}], "explanation": "The diameter (or width) of a tree is the longest path between any two nodes, measured by the number of edges. This path may or may not pass through the root."},
    ]

def graphs_mcq():
    return [
        {"title": "Undirected Graph Edges", "text": "What is the maximum number of edges in a simple undirected graph with N vertices?", "difficulty": "easy", "options": [{"text": "N(N-1)/2", "is_correct": True}, {"text": "N\u00b2", "is_correct": False}, {"text": "N-1", "is_correct": False}, {"text": "N(N+1)/2", "is_correct": False}], "explanation": "In a simple undirected graph, each pair of vertices has at most one edge. There are C(N,2) = N(N-1)/2 pairs. N\u00b2 would be for a directed graph with self-loops."},
        {"title": "Graph Representation", "text": "Which representation is best for a dense graph?", "difficulty": "medium", "options": [{"text": "Adjacency matrix", "is_correct": True}, {"text": "Adjacency list", "is_correct": False}, {"text": "Edge list", "is_correct": False}, {"text": "Incidence matrix", "is_correct": False}], "explanation": "Adjacency matrix (N\u00d7N) uses O(N\u00b2) space regardless of edge count. For dense graphs (edges close to N\u00b2), this is efficient. Adjacency lists are better for sparse graphs (O(V+E) space)."},
        {"title": "BFS Traversal", "text": "Which graph traversal finds the shortest path in an unweighted graph?", "difficulty": "easy", "options": [{"text": "BFS (Breadth-First Search)", "is_correct": True}, {"text": "DFS (Depth-First Search)", "is_correct": False}, {"text": "Dijkstra's algorithm", "is_correct": False}, {"text": "Prim's algorithm", "is_correct": False}], "explanation": "BFS explores vertices in order of distance from the source, so the first time it reaches a target is along the shortest path (in unweighted graphs). DFS doesn't guarantee shortest paths."},
        {"title": "Directed Acyclic Graph", "text": "What is a topological ordering of a DAG?", "difficulty": "medium", "options": [{"text": "A linear ordering where all edges go forward", "is_correct": True}, {"text": "A Hamiltonian path", "is_correct": False}, {"text": "A depth-first traversal order", "is_correct": False}, {"text": "A random permutation of vertices", "is_correct": False}], "explanation": "A topological ordering arranges vertices so that for every directed edge u\u2192v, u comes before v. This is only possible in DAGs. DFS can produce a topological ordering using finish times."},
        {"title": "Dijkstra's Limitation", "text": "Why can't Dijkstra's algorithm handle negative edge weights?", "difficulty": "hard", "options": [{"text": "It assumes visited nodes have their final shortest distance", "is_correct": True}, {"text": "It can't compute negative distances", "is_correct": False}, {"text": "It requires edge weights to be positive integers", "is_correct": False}, {"text": "It uses a min-heap for priority", "is_correct": False}], "explanation": "Dijkstra's algorithm greedily finalizes the shortest distance to visited nodes. A negative edge could later reduce a finalized distance, which Dijkstra's doesn't allow. Bellman-Ford handles negative weights."},
        {"title": "Tree as Graph", "text": "A tree with N nodes has exactly how many edges?", "difficulty": "easy", "options": [{"text": "N - 1", "is_correct": True}, {"text": "N", "is_correct": False}, {"text": "N + 1", "is_correct": False}, {"text": "N / 2", "is_correct": False}], "explanation": "A tree is a connected acyclic graph with exactly N-1 edges. This is a fundamental property: a tree on N nodes always has N-1 edges."},
        {"title": "Graph Coloring - Bipartite", "text": "Which graph is always bipartite?", "difficulty": "medium", "options": [{"text": "A graph with no odd-length cycles", "is_correct": True}, {"text": "A complete graph", "is_correct": False}, {"text": "A directed acyclic graph", "is_correct": False}, {"text": "A graph with a Hamiltonian cycle", "is_correct": False}], "explanation": "A graph is bipartite iff it has no odd-length cycles. If a graph has any odd cycle, 2-coloring is impossible."},
        {"title": "Spanning Tree", "text": "What is the minimum number of edges that must be removed from a connected graph with N nodes and E edges to make it a tree?", "difficulty": "medium", "options": [{"text": "E - N + 1", "is_correct": True}, {"text": "E - N", "is_correct": False}, {"text": "E - N - 1", "is_correct": False}, {"text": "N - 1 - E", "is_correct": False}], "explanation": "A tree needs exactly N-1 edges. If the graph has E edges, we need to remove E - (N-1) = E - N + 1 edges to get a spanning tree. This is the number of cycles (cyclomatic number)."},
        {"title": "Graph Traversal Time Complexity", "text": "What is the time complexity of BFS on a graph with V vertices and E edges (adjacency list)?", "difficulty": "easy", "options": [{"text": "O(V + E)", "is_correct": True}, {"text": "O(V\u00b2)", "is_correct": False}, {"text": "O(V)", "is_correct": False}, {"text": "O(E)", "is_correct": False}], "explanation": "BFS visits each vertex once and examines each edge once, giving O(V + E) time. O(V\u00b2) is for adjacency matrix BFS (checking all V neighbors for each vertex)."},
        {"title": "Detecting Cycles in Directed Graph", "text": "Which algorithm can detect cycles in a directed graph?", "difficulty": "medium", "options": [{"text": "DFS with a recursion stack", "is_correct": True}, {"text": "BFS with a visited set", "is_correct": False}, {"text": "Topological sort of an unmodified graph", "is_correct": False}, {"text": "Union-Find (DSU)", "is_correct": False}], "explanation": "DFS with a recursion stack detects back edges in directed graphs. A back edge from a node to an ancestor in the DFS tree indicates a cycle. Union-Find works for undirected graphs, not directed."},
    ]

def dp_mcq():
    return [
        {"title": "Optimal Substructure", "text": "What property must a problem have for dynamic programming to be applicable?", "difficulty": "medium", "options": [{"text": "Optimal substructure + overlapping subproblems", "is_correct": True}, {"text": "Only optimal substructure", "is_correct": False}, {"text": "Only overlapping subproblems", "is_correct": False}, {"text": "Greedy choice property", "is_correct": False}], "explanation": "Dynamic programming requires both optimal substructure (optimal solution contains optimal solutions to subproblems) and overlapping subproblems (same subproblems recur). Greedy choice property is for greedy algorithms."},
        {"title": "Memoization vs Tabulation", "text": "What is the key difference between memoization (top-down) and tabulation (bottom-up) DP?", "difficulty": "medium", "options": [{"text": "Tabulation iteratively fills a table; memoization uses recursion with caching", "is_correct": True}, {"text": "Memoization is always faster than tabulation", "is_correct": False}, {"text": "Tabulation uses more memory than memoization", "is_correct": False}, {"text": "Memoization can't handle recursive problems", "is_correct": False}], "explanation": "Memoization is top-down (recursive with cache), filling the table on demand. Tabulation is bottom-up (iterative), filling the entire table. Tabulation often has lower overhead but always computes all subproblems."},
        {"title": "Fibonacci with DP", "text": "Without optimization, what is the time complexity of computing the nth Fibonacci number recursively?", "difficulty": "easy", "options": [{"text": "O(2\u207f)", "is_correct": True}, {"text": "O(n)", "is_correct": False}, {"text": "O(n\u00b2)", "is_correct": False}, {"text": "O(log n)", "is_correct": False}], "explanation": "The naive recursive Fibonacci makes 2 recursive calls per node, creating a binary tree of depth n, giving O(2\u207f) time. With DP (memoization or tabulation), it becomes O(n)."},
        {"title": "0/1 Knapsack - Items",
         "text": "In the 0/1 knapsack problem, what constraint applies to each item?",
         "difficulty": "easy",
         "options": [
             {"text": "Each item can be taken at most once", "is_correct": True},
             {"text": "Each item can be taken any number of times", "is_correct": False},
             {"text": "Items must be taken in order of value", "is_correct": False},
             {"text": "Fractional items are allowed", "is_correct": False}
         ],
         "explanation": "'0/1' means each item is either taken (1) or not taken (0) — at most once. Unlimited items is the 'unbounded knapsack' variant. Fractions are the 'fractional knapsack' (greedy solution)."},
        {"title": "Coin Change - Optimal Substructure",
         "text": "The minimum number of coins to make amount A using coins {câ‚, câ‚‚, ..., câ‚™} can be expressed as:", "difficulty": "hard", "options": [{"text": "1 + min over i of minCoins(A - cáµ¢)", "is_correct": True}, {"text": "min over i of 1 + minCoins(A/cáµ¢)", "is_correct": False}, {"text": "sum over i of minCoins(A)/cáµ¢", "is_correct": False}, {"text": "A / max(cáµ¢)", "is_correct": False}], "explanation": "minCoins(A) = 1 + min(minCoins(A-câ‚), minCoins(A-câ‚‚), ..., minCoins(A-câ‚™)). This is the optimal substructure: for each coin, make the remaining amount optimally."},
        {"title": "LCS Problem", "text": "The longest common subsequence (LCS) of 'ABC' and 'ACB' is:", "difficulty": "medium", "options": [{"text": "'AB'", "is_correct": True}, {"text": "'AC'", "is_correct": False}, {"text": "'ABC'", "is_correct": False}, {"text": "'A'", "is_correct": False}], "explanation": "LCS of 'ABC' and 'ACB': The common subsequences are 'A' (length 1), 'B' (position 2 in both? No, B is at index 2 in 'ABC' and index 3 in 'ACB'), 'C' (index 3 and 2), 'AB' (indices 1,2 in first and 1,3 in second). So LCS = 'AB' or 'AC', both length 2. 'ABC' is not a subsequence of 'ACB' (the order of C and B differs)."},
        {"title": "Edit Distance", "text": "What operations does the edit distance (Levenshtein distance) typically allow?", "difficulty": "medium", "options": [{"text": "Insert, delete, substitute", "is_correct": True}, {"text": "Insert and delete only", "is_correct": False}, {"text": "Swap adjacent characters", "is_correct": False}, {"text": "Insert, delete, and transpose", "is_correct": False}], "explanation": "Levenshtein distance allows 3 operations: insert a character, delete a character, or substitute one character for another. Each operation typically costs 1."},
        {"title": "Matrix Chain Multiplication", "text": "Matrix chain multiplication is an example of:", "difficulty": "hard", "options": [{"text": "DP on intervals", "is_correct": True}, {"text": "Greedy on weights", "is_correct": False}, {"text": "Divide and conquer without overlapping", "is_correct": False}, {"text": "Linear DP on prefix", "is_correct": False}], "explanation": "Matrix chain multiplication uses DP on intervals (range-based DP), where dp[i][j] is the optimal cost for matrices i through j. The subproblem ranges overlap, requiring optimal substructure across intervals."},
        {"title": "Palindromic Subsequence", "text": "The longest palindromic subsequence (LPS) of 'BBABCBCAB' is:", "difficulty": "hard", "options": [{"text": "BABCBAB", "is_correct": True}, {"text": "BBBBB", "is_correct": False}, {"text": "ABCBA", "is_correct": False}, {"text": "BBCBB", "is_correct": False}], "explanation": "The longest palindromic subsequence of 'BBABCBCAB' is 'BABCBAB' (length 7). One way to find LPS is to compute LCS of the string with its reverse."},
        {"title": "DP vs Divide & Conquer", "text": "How does dynamic programming differ from divide and conquer?", "difficulty": "medium", "options": [{"text": "DP solves overlapping subproblems; D&C solves independent subproblems", "is_correct": True}, {"text": "D&C uses recursion; DP never uses recursion", "is_correct": False}, {"text": "DP is always faster than D&C", "is_correct": False}, {"text": "D&C requires memoization; DP doesn't", "is_correct": False}], "explanation": "Both use recursion, but D&C splits problems into independent subproblems (e.g., merge sort), while DP handles overlapping subproblems (same subproblems recur). Memoization/tabulation optimizes DP, not D&C."},
    ]

# Python MCQ generators
def basics_mcq():
    return [
        {"title": "Print Function", "text": "What is the output of print('Hello' + ' ' + 'World')?", "difficulty": "easy", "options": [{"text": "Hello World", "is_correct": True}, {"text": "HelloWorld", "is_correct": False}, {"text": "Hello World (with quotes)", "is_correct": False}, {"text": "Error", "is_correct": False}], "explanation": "The + operator concatenates strings. 'Hello' + ' ' + 'World' = 'Hello World'. The print function outputs the resulting string without quotes."},
        {"title": "Variable Assignment", "text": "What is the type of x after x = 7 / 2 in Python 3?", "difficulty": "easy", "options": [{"text": "float", "is_correct": True}, {"text": "int", "is_correct": False}, {"text": "str", "is_correct": False}, {"text": "bool", "is_correct": False}], "explanation": "In Python 3, the / operator always returns a float (3.5). The // operator performs integer division (returns 3). This differs from Python 2 where / did integer division on ints."},
        {"title": "String Indexing", "text": "What is the result of 'Python'[-3]?", "difficulty": "easy", "options": [{"text": "'h'", "is_correct": True}, {"text": "'t'", "is_correct": False}, {"text": "'o'", "is_correct": False}, {"text": "'n'", "is_correct": False}], "explanation": "Negative indices count from the end. 'Python'[-1]='n', [-2]='o', [-3]='h'. A common mistake is to start counting from 0 backwards."},
        {"title": "List Comprehension", "text": "What is the result of [x*2 for x in range(4)]?", "difficulty": "medium", "options": [{"text": "[0, 2, 4, 6]", "is_correct": True}, {"text": "[2, 4, 6, 8]", "is_correct": False}, {"text": "[0, 2, 4, 6, 8]", "is_correct": False}, {"text": "[2, 4, 6]", "is_correct": False}], "explanation": "range(4) generates 0,1,2,3. Each element is doubled: 0,2,4,6. The result is [0,2,4,6]. range(1,5) would give [2,4,6,8]."},
        {"title": "Mutable vs Immutable", "text": "Which of the following Python types is MUTABLE?", "difficulty": "easy", "options": [{"text": "list", "is_correct": True}, {"text": "tuple", "is_correct": False}, {"text": "str", "is_correct": False}, {"text": "int", "is_correct": False}], "explanation": "Lists are mutable (can be modified in-place). Tuples, strings, and integers are immutable — any 'change' creates a new object."},
        {"title": "Boolean Logic", "text": "What does (True and False) or (not False) evaluate to?", "difficulty": "medium", "options": [{"text": "True", "is_correct": True}, {"text": "False", "is_correct": False}, {"text": "None", "is_correct": False}, {"text": "Error", "is_correct": False}], "explanation": "(True and False) = False. (not False) = True. False or True = True. Order of operations: 'and' has higher precedence than 'or' in Python."},
        {"title": "For Loop with Range", "text": "How many times will this loop execute: for i in range(2, 10, 3):", "difficulty": "medium", "options": [{"text": "3", "is_correct": True}, {"text": "2", "is_correct": False}, {"text": "4", "is_correct": False}, {"text": "8", "is_correct": False}], "explanation": "range(2,10,3) generates: 2, 5, 8 (stops before 10). That's 3 iterations. The step size determines how the sequence advances."},
        {"title": "Exception Handling", "text": "Which clause in a try-except block always executes regardless of whether an exception occurred?", "difficulty": "easy", "options": [{"text": "finally", "is_correct": True}, {"text": "except", "is_correct": False}, {"text": "else", "is_correct": False}, {"text": "try", "is_correct": False}], "explanation": "The 'finally' block always executes (for cleanup), whether an exception occurs or not. 'else' runs only if no exception occurs. 'except' runs only if an exception occurs."},
        {"title": "Function Default Arguments", "text": "What is the result of: def f(x=[]): x.append(1); return x; print(f()); print(f())?", "difficulty": "hard", "options": [{"text": "[1] then [1, 1]", "is_correct": True}, {"text": "[1] then [1]", "is_correct": False}, {"text": "Error", "is_correct": False}, {"text": "[1] then []", "is_correct": False}], "explanation": "Default arguments are evaluated once at function definition, not each call. The same list is mutated across calls. First call: [1]. Second call: [1, 1]. This is a common Python pitfall."},
        {"title": "Slicing", "text": "What is the result of 'Python Programming'[7:18]?", "difficulty": "medium", "options": [{"text": "'Programming'", "is_correct": True}, {"text": "'Programmin'", "is_correct": False}, {"text": "'Python'", "is_correct": False}, {"text": "'rogramming'", "is_correct": False}], "explanation": "'Python Programming' has indices: P=0, y=1, t=2, h=3, o=4, n=5, ' '=6, P=7, r=8... [7:18] extracts from index 7 to 17: 'Programming' (length 11). 'Programmin' would be [7:17]."},
    ]

def data_types_mcq():
    return [
        {"title": "Type Function", "text": "What does type(3.14) return?", "difficulty": "easy", "options": [{"text": "&lt;class 'float'&gt;", "is_correct": True}, {"text": "&lt;class 'int'&gt;", "is_correct": False}, {"text": "&lt;class 'str'&gt;", "is_correct": False}, {"text": "&lt;class 'double'&gt;", "is_correct": False}], "explanation": "3.14 is a float literal in Python. There is no 'double' type in Python (unlike C/Java) — Python floats are double-precision under the hood but referred to as 'float'."},
        {"title": "Set Operations", "text": "What is {1, 2, 3} & {2, 3, 4}?", "difficulty": "medium", "options": [{"text": "{2, 3}", "is_correct": True}, {"text": "{1, 2, 3, 4}", "is_correct": False}, {"text": "{1, 4}", "is_correct": False}, {"text": "{2, 3, 4}", "is_correct": False}], "explanation": "The & operator is set intersection, returning elements common to both sets. {1,2,3} \u2229 {2,3,4} = {2,3}. The | operator gives union {1,2,3,4}. The - operator gives difference."},
        {"title": "Dictionary Keys", "text": "Which of the following CAN be used as a dictionary key?", "difficulty": "medium", "options": [{"text": "Tuple (1, 2)", "is_correct": True}, {"text": "List [1, 2]", "is_correct": False}, {"text": "Set {1, 2}", "is_correct": False}, {"text": "Dictionary {'a': 1}", "is_correct": False}], "explanation": "Dictionary keys must be hashable (immutable). Tuples are immutable and hashable. Lists, sets, and dicts are mutable and unhashable."},
        {"title": "String Methods", "text": "What does 'hello world'.split() return?", "difficulty": "easy", "options": [{"text": "['hello', 'world']", "is_correct": True}, {"text": "['hello world']", "is_correct": False}, {"text": "['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']", "is_correct": False}, {"text": "('hello', 'world')", "is_correct": False}], "explanation": "The split() method (without arguments) splits on whitespace and returns a list of words. split(',') would split on commas."},
        {"title": "Type Conversion", "text": "What is the result of int('101', 2)?", "difficulty": "medium", "options": [{"text": "5", "is_correct": True}, {"text": "101", "is_correct": False}, {"text": "3", "is_correct": False}, {"text": "Error", "is_correct": False}], "explanation": "int('101', 2) converts the string '101' from base 2 to decimal: 1\u00d72\u00b2 + 0\u00d72 + 1 = 4 + 0 + 1 = 5. Without the base argument, int('101') gives 101 (base 10)."},
        {"title": "None Type", "text": "What is the result of print(type(None))?", "difficulty": "easy", "options": [{"text": "&lt;class 'NoneType'&gt;", "is_correct": True}, {"text": "&lt;class 'None'&gt;", "is_correct": False}, {"text": "None", "is_correct": False}, {"text": "&lt;class 'bool'&gt;", "is_correct": False}], "explanation": "None is a singleton of type NoneType. It represents the absence of a value, similar to null in other languages."},
        {"title": "List vs Tuple", "text": "Which statement about tuples is TRUE?", "difficulty": "medium", "options": [{"text": "Tuples are immutable sequences", "is_correct": True}, {"text": "Tuples can contain only one data type", "is_correct": False}, {"text": "Tuples are faster than lists for iteration", "is_correct": False}, {"text": "Tuples don't support indexing", "is_correct": False}], "explanation": "Tuples are immutable sequences — once created, they cannot be modified. They can contain mixed types and support indexing. They may be slightly faster than lists but the main difference is immutability."},
        {"title": "Deep vs Shallow Copy", "text": "Which import is needed for deep copy in Python?", "difficulty": "medium", "options": [{"text": "import copy", "is_correct": True}, {"text": "import deepcopy", "is_correct": False}, {"text": "from sys import copy", "is_correct": False}, {"text": "import clone", "is_correct": False}], "explanation": "The built-in 'copy' module provides copy.copy() (shallow) and copy.deepcopy() (deep). There is no 'deepcopy' or 'clone' module in Python's standard library."},
        {"title": "Frozenset", "text": "What is a frozenset in Python?", "difficulty": "hard", "options": [{"text": "An immutable version of a set", "is_correct": True}, {"text": "A set of frozen objects", "is_correct": False}, {"text": "A set stored on disk", "is_correct": False}, {"text": "A set comprehension shortcut", "is_correct": False}], "explanation": "frozenset() returns an immutable set. It can be used as a dictionary key or set element (unlike a regular set). frozenset({1,2,3}) creates an immutable set {1,2,3}."},
        {"title": "Complex Numbers", "text": "What is the type of 3+4j in Python?", "difficulty": "easy", "options": [{"text": "complex", "is_correct": True}, {"text": "float", "is_correct": False}, {"text": "int", "is_correct": False}, {"text": "Error (j is not defined)", "is_correct": False}], "explanation": "Python has built-in support for complex numbers using j as the imaginary unit. 3+4j is of type 'complex'. Note: j is the standard in engineering; Python uses j (not i)."},
    ]

def oop_mcq():
    return [
        {"title": "Class Definition", "text": "Which keyword is used to define a class in Python?", "difficulty": "easy", "options": [{"text": "class", "is_correct": True}, {"text": "struct", "is_correct": False}, {"text": "def", "is_correct": False}, {"text": "object", "is_correct": False}], "explanation": "Python uses the 'class' keyword to define classes. 'def' is for functions. 'struct' is not a Python keyword. 'object' is a built-in base class."},
        {"title": "Self Parameter", "text": "In Python instance methods, what does the 'self' parameter represent?", "difficulty": "easy", "options": [{"text": "The instance of the class", "is_correct": True}, {"text": "The class itself", "is_correct": False}, {"text": "A reference to the module", "is_correct": False}, {"text": "Nothing (it's optional)", "is_correct": False}], "explanation": "'self' refers to the current instance of the class. It is passed implicitly by Python when calling instance methods. Unlike 'this' in Java/C++, self must be explicitly listed as the first parameter."},
        {"title": "Inheritance", "text": "What is the correct syntax for class B to inherit from class A?", "difficulty": "easy", "options": [{"text": "class B(A):", "is_correct": True}, {"text": "class B extends A:", "is_correct": False}, {"text": "class B inherits A:", "is_correct": False}, {"text": "class B(A):", "is_correct": False}], "explanation": "Python uses parentheses for inheritance: class Child(Parent). Multiple inheritance: class Child(Parent1, Parent2)."},
        {"title": "Dunder Methods", "text": "Which method is called when len(obj) is executed?", "difficulty": "medium", "options": [{"text": "__len__", "is_correct": True}, {"text": "__length__", "is_correct": False}, {"text": "__size__", "is_correct": False}, {"text": "__str__", "is_correct": False}], "explanation": "len(obj) internally calls obj.__len__(). This is the Pythonic way to define the length of custom objects."},
        {"title": "@staticmethod vs @classmethod", "text": "What is the key difference between @staticmethod and @classmethod?", "difficulty": "medium", "options": [{"text": "@classmethod receives cls; @staticmethod receives nothing", "is_correct": True}, {"text": "@staticmethod can access instance attributes", "is_correct": False}, {"text": "There is no difference", "is_correct": False}, {"text": "@classmethod is used only for abstract classes", "is_correct": False}], "explanation": "@classmethod receives the class as the first parameter (cls) and can access/modify class state. @staticmethod receives no special first parameter and behaves like a regular function."},
        {"title": "Encapsulation", "text": "How do you indicate a 'private' attribute in Python?", "difficulty": "medium", "options": [{"text": "Prefix with double underscore (__attr)", "is_correct": True}, {"text": "Use the private keyword", "is_correct": False}, {"text": "Prefix with single underscore (_attr)", "is_correct": False}, {"text": "Use the @private decorator", "is_correct": False}], "explanation": "Double underscore prefix triggers name mangling (_ClassName__attr), making it harder to access from outside. Single underscore is a convention for 'protected', not enforced by Python."},
        {"title": "Property Decorator", "text": "What does @property do in a Python class?", "difficulty": "medium", "options": [{"text": "Makes a method accessible as an attribute", "is_correct": True}, {"text": "Creates a class variable", "is_correct": False}, {"text": "Marks a method as abstract", "is_correct": False}, {"text": "Defines a class-level property", "is_correct": False}], "explanation": "@property allows a method to be accessed like an attribute (without parentheses). It enables getter/setter patterns with controlled access."},
        {"title": "Abstract Base Class", "text": "Which module provides abstract base class support in Python?", "difficulty": "medium", "options": [{"text": "abc", "is_correct": True}, {"text": "abstract", "is_correct": False}, {"text": "base", "is_correct": False}, {"text": "interface", "is_correct": False}], "explanation": "The 'abc' module (Abstract Base Classes) provides ABC and abstractmethod decorator. A class inheriting from ABC with abstract methods cannot be instantiated."},
        {"title": "Multiple Inheritance - MRO", "text": "What determines the method resolution order (MRO) in Python?", "difficulty": "hard", "options": [{"text": "C3 linearization (depth-first, left-to-right)", "is_correct": True}, {"text": "Depth-first, right-to-left", "is_correct": False}, {"text": "Breadth-first search", "is_correct": False}, {"text": "Alphabetical order", "is_correct": False}], "explanation": "Python uses C3 linearization for MRO: child first, then parents in order of definition, but ensuring a consistent ordering (linearization). You can check MRO with ClassName.__mro__."},
        {"title": "Slots", "text": "What does __slots__ do in a Python class?", "difficulty": "hard", "options": [{"text": "Restricts attribute creation to listed names", "is_correct": True}, {"text": "Defines class attributes", "is_correct": False}, {"text": "Reserves memory for the class", "is_correct": False}, {"text": "Creates static methods for the class", "is_correct": False}], "explanation": "__slots__ restricts a class to only the listed attribute names and prevents the creation of __dict__. This saves memory when many instances are created but prevents dynamic attribute assignment."},
    ]

def file_handling_mcq():
    return [
        {"title": "Open Function", "text": "Which statement opens 'file.txt' for writing?", "difficulty": "easy", "options": [{"text": "open('file.txt', 'w')", "is_correct": True}, {"text": "open('file.txt', 'r')", "is_correct": False}, {"text": "open('file.txt', 'a')", "is_correct": False}, {"text": "open('file.txt', 'x')", "is_correct": False}], "explanation": "'w' opens for writing (overwrites existing content). 'r' is read, 'a' is append, 'x' is exclusive creation."},
        {"title": "With Statement", "text": "What is the purpose of using 'with open() as f:'?", "difficulty": "easy", "options": [{"text": "Auto-closes the file after the block", "is_correct": True}, {"text": "Keeps the file open indefinitely", "is_correct": False}, {"text": "Improves write speed only", "is_correct": False}, {"text": "Opens the file in binary mode", "is_correct": False}], "explanation": "The 'with' statement (context manager) automatically calls f.close() when the block exits, even if an exception occurs. This prevents resource leaks."},
        {"title": "Read Methods", "text": "What does f.readlines() return?", "difficulty": "easy", "options": [{"text": "A list of strings, one per line", "is_correct": True}, {"text": "A single string of the entire file", "is_correct": False}, {"text": "An iterator over file lines", "is_correct": False}, {"text": "A tuple of file lines", "is_correct": False}], "explanation": "f.readlines() reads all lines and returns them as a list of strings (each with a trailing newline). f.read() returns a single string. Iterating over f directly yields lines one by one (memory efficient)."},
        {"title": "Binary Mode", "text": "How do you open a file in binary write mode?", "difficulty": "medium", "options": [{"text": "open('file.bin', 'wb')", "is_correct": True}, {"text": "open('file.bin', 'bw')", "is_correct": False}, {"text": "open('file.bin', 'bin')", "is_correct": False}, {"text": "open('file.bin', 'w', binary=True)", "is_correct": False}], "explanation": "Binary mode is indicated by appending 'b' to the mode string: 'wb' (write binary), 'rb' (read binary), 'ab' (append binary)."},
        {"title": "File Exists Check", "text": "Which module provides os.path.exists()?", "difficulty": "medium", "options": [{"text": "os.path", "is_correct": True}, {"text": "os", "is_correct": False}, {"text": "shutil", "is_correct": False}, {"text": "pathlib", "is_correct": False}], "explanation": "os.path.exists() is in the os.path module. pathlib.Path.exists() is the modern alternative. The 'os' module itself doesn't have exists() directly."},
        {"title": "JSON Serialization", "text": "Which function writes a Python dict to a JSON file?", "difficulty": "medium", "options": [{"text": "json.dump(data, file)", "is_correct": True}, {"text": "json.dumps(data, file)", "is_correct": False}, {"text": "json.write(data, file)", "is_correct": False}, {"text": "json.serialize(data, file)", "is_correct": False}], "explanation": "json.dump() writes to a file object. json.dumps() returns a JSON string (s = string). The 's' suffix distinguishes string output from file output."},
        {"title": "Pathlib Usage", "text": "What is the modern Python way to construct file paths?", "difficulty": "medium", "options": [{"text": "pathlib.Path('dir') / 'file.txt'", "is_correct": True}, {"text": "os.path.join('dir', 'file.txt')", "is_correct": False}, {"text": "'dir' + '/' + 'file.txt'", "is_correct": False}, {"text": "f'dir/{file.txt}'", "is_correct": False}], "explanation": "pathlib (Python 3.4+) provides an OOP path interface. The / operator joins path components. os.path.join() is the older approach. Manual string concatenation is fragile across OSes."},
        {"title": "CSV Reading", "text": "Which module is standard for CSV file handling?", "difficulty": "medium", "options": [{"text": "csv", "is_correct": True}, {"text": "pandas", "is_correct": False}, {"text": "excel", "is_correct": False}, {"text": "tablib", "is_correct": False}], "explanation": "The built-in 'csv' module handles CSV files. pandas is third-party. csv.reader() and csv.writer() provide basic CSV I/O without external dependencies."},
        {"title": "Pickle Module", "text": "What is the main limitation of pickle serialization?", "difficulty": "hard", "options": [{"text": "Not secure against malicious data", "is_correct": True}, {"text": "Only works on text files", "is_correct": False}, {"text": "Cannot serialize custom classes", "is_correct": False}, {"text": "Requires a database connection", "is_correct": False}], "explanation": "Pickle can execute arbitrary code during deserialization, making it unsafe to unpickle untrusted data. JSON is preferred for data interchange. Pickle IS designed for Python objects."},
        {"title": "Context Manager Protocol", "text": "Which methods does a class need to implement the context manager protocol (with statement)?", "difficulty": "hard", "options": [{"text": "__enter__ and __exit__", "is_correct": True}, {"text": "__open__ and __close__", "is_correct": False}, {"text": "__init__ and __del__", "is_correct": False}, {"text": "__start__ and __end__", "is_correct": False}], "explanation": "A context manager implements __enter__ (returns the resource) and __exit__ (cleanup, called when the block exits). This is what enables the 'with' statement."},
    ]

def libraries_mcq():
    return [
        {"title": "Math Module", "text": "Which math function returns the square root of a number?", "difficulty": "easy", "options": [{"text": "math.sqrt(x)", "is_correct": True}, {"text": "math.sqr(x)", "is_correct": False}, {"text": "math.root(x, 2)", "is_correct": False}, {"text": "math.pow(x, 0.5)", "is_correct": False}], "explanation": "math.sqrt(x) returns the square root. math.pow(x, 0.5) also works but returns a float, while ** 0.5 is the built-in operator."},
        {"title": "Random Module", "text": "Which function returns a random integer between 1 and 10 (inclusive)?", "difficulty": "easy", "options": [{"text": "random.randint(1, 10)", "is_correct": True}, {"text": "random.random(1, 10)", "is_correct": False}, {"text": "random.choice(1, 10)", "is_correct": False}, {"text": "random.range(1, 10)", "is_correct": False}], "explanation": "random.randint(a, b) returns a random integer N where a \u2264 N \u2264 b. random.random() returns a float in [0,1). random.choice() picks from a sequence."},
        {"title": "Datetime Module", "text": "How do you get the current date and time in Python?", "difficulty": "easy", "options": [{"text": "datetime.datetime.now()", "is_correct": True}, {"text": "datetime.today()", "is_correct": False}, {"text": "datetime.current()", "is_correct": False}, {"text": "datetime.gettime()", "is_correct": False}], "explanation": "datetime.datetime.now() returns the current local date and time. datetime.date.today() returns only the date. datetime.now() without module prefix would fail."},
        {"title": "Collections - Counter", "text": "After from collections import Counter; c = Counter('aabbc'), what is c['b']?", "difficulty": "medium", "options": [{"text": "2", "is_correct": True}, {"text": "1", "is_correct": False}, {"text": "3", "is_correct": False}, {"text": "0", "is_correct": False}], "explanation": "Counter counts hashable objects. 'aabbc' has: a=2, b=2, c=1. c['b'] returns 2. c['d'] returns 0 (no KeyError, unlike regular dict)."},
        {"title": "Itertools - Combinations", "text": "What does list(itertools.combinations('ABC', 2)) return?", "difficulty": "medium", "options": [{"text": "[('A','B'), ('A','C'), ('B','C')]", "is_correct": True}, {"text": "[('A','B'), ('B','C'), ('C','A')]", "is_correct": False}, {"text": "[('A','B'), ('B','A'), ('A','C'), ('C','A'), ('B','C'), ('C','B')]", "is_correct": False}, {"text": "[('A',), ('B',), ('C',)]", "is_correct": False}], "explanation": "combinations produces r-length tuples in lexicographic order WITHOUT replacement. permutations would include all orderings like ('B','A'). 'ABC' with 2 gives 3 pairs."},
        {"title": "OS Module - Directory Listing", "text": "Which function lists files in a directory?", "difficulty": "easy", "options": [{"text": "os.listdir(path)", "is_correct": True}, {"text": "os.ls(path)", "is_correct": False}, {"text": "os.dir(path)", "is_correct": False}, {"text": "os.files(path)", "is_correct": False}], "explanation": "os.listdir(path) returns a list of entry names in the directory. os.ls() doesn't exist in Python's os module (it's a Unix shell command)."},
        {"title": "Sys Module - Command Line Args", "text": "Which attribute of sys contains command-line arguments?", "difficulty": "medium", "options": [{"text": "sys.argv", "is_correct": True}, {"text": "sys.args", "is_correct": False}, {"text": "sys.arguments", "is_correct": False}, {"text": "sys.command_line", "is_correct": False}], "explanation": "sys.argv is a list where argv[0] is the script name and argv[1:] are the command-line arguments. sys.args doesn't exist."},
        {"title": "Regular Expressions", "text": "Which function finds all non-overlapping matches of a pattern in a string?", "difficulty": "medium", "options": [{"text": "re.findall(pattern, string)", "is_correct": True}, {"text": "re.match(pattern, string)", "is_correct": False}, {"text": "re.search(pattern, string)", "is_correct": False}, {"text": "re.extract(pattern, string)", "is_correct": False}], "explanation": "re.findall() returns all non-overlapping matches as a list. re.match() checks only at the start. re.search() finds the first match anywhere."},
        {"title": "Deque from Collections", "text": "What makes collections.deque efficient compared to a list?", "difficulty": "hard", "options": [{"text": "O(1) append and pop from both ends", "is_correct": True}, {"text": "O(1) random access by index", "is_correct": False}, {"text": "Automatically sorted order", "is_correct": False}, {"text": "Memory-efficient for large data", "is_correct": False}], "explanation": "deque provides O(1) append/pop from both ends (left and right). Lists have O(1) at the right end but O(N) at the left. Random access is O(N) for deque vs O(1) for list."},
        {"title": "Functools - LRU Cache", "text": "What does @functools.lru_cache(maxsize=128) do?", "difficulty": "hard", "options": [{"text": "Caches function return values for up to 128 calls", "is_correct": True}, {"text": "Limits the function to 128 calls total", "is_correct": False}, {"text": "Speeds up function compilation", "is_correct": False}, {"text": "Creates 128 copies of the function", "is_correct": False}], "explanation": "@lru_cache caches the return values of a function based on arguments. When the cache exceeds maxsize, least recently used entries are evicted. This is useful for DP/memoization."},
    ]

# ─── Write all remaining MCQ files ───────────────────────────

MCQ_GENERATORS = {
    "syllogisms": syllogisms,
    "direction_sense": direction_sense,
    "puzzles": puzzles_mcq,
    "arrays": arrays_mcq,
    "linked_lists": linked_lists_mcq,
    "trees": trees_mcq,
    "graphs": graphs_mcq,
    "dynamic_programming": dp_mcq,
    "basics": basics_mcq,
    "data_types": data_types_mcq,
    "oop": oop_mcq,
    "file_handling": file_handling_mcq,
    "libraries": libraries_mcq,
}

for topic_name, generator in MCQ_GENERATORS.items():
    path = os.path.join(MCQ_DIR, f"{topic_name}.json")
    questions = generator()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(questions)} MCQ to mcq/{topic_name}.json")

# ─── CODING CONTENT GENERATORS ───────────────────────────────

def linked_lists_coding():
    return [
        {
            "title": "Reverse a Linked List",
            "text": "Given a linked list (N nodes, 1 \u2264 N \u2264 10\u2075), reverse it and print the reversed list. The list is given as space-separated integers, with -1 as the end marker. Print the reversed list space-separated.\n\nInput format:\na\u2081 a\u2082 ... a\u2099 -1\n\nOutput format:\na\u2099 a\u2099\u208b\u2081 ... a\u2081\n\nExample:\nInput:\n1 2 3 4 5 -1\n\nOutput:\n5 4 3 2 1",
            "difficulty": "easy",
            "starter_code": "def solve():\n    arr = []\n    while True:\n        val = int(input())\n        if val == -1:\n            break\n        arr.append(val)\n    # Reverse and print\n\nsolve()\n",
            "test_cases": [
                {"stdin": "1 2 3 4 5 -1", "expected_output": "5 4 3 2 1", "is_hidden": False},
                {"stdin": "7 -1", "expected_output": "7", "is_hidden": False},
                {"stdin": "10 20 30 -1", "expected_output": "30 20 10", "is_hidden": True},
            ],
        },
        {
            "title": "Detect Cycle in Linked List",
            "text": "Given N space-separated integers followed by a position P (-1 if no cycle), determine if the linked list has a cycle. The position P indicates where the tail connects (0-indexed). Print 'yes' or 'no'.\n\nInput format:\na\u2081 a\u2082 ... a\u2099\nP\n\nOutput format:\nyes or no\n\nExample:\nInput:\n1 2 3 4 5\n2\n\nOutput:\nyes\n(Explanation: tail connects to node at index 2, creating a cycle 5\u21923)",
            "difficulty": "medium",
            "starter_code": "def solve():\n    arr = list(map(int, input().split()))\n    p = int(input())\n    # Detect cycle and print 'yes' or 'no'\n\nsolve()\n",
            "test_cases": [
                {"stdin": "1 2 3 4 5\n-1", "expected_output": "no", "is_hidden": False},
                {"stdin": "1 2 3 4 5\n0", "expected_output": "yes", "is_hidden": False},
                {"stdin": "7\n-1", "expected_output": "no", "is_hidden": True},
            ],
        },
    ]

def trees_coding():
    return [
        {
            "title": "Height of Binary Tree",
            "text": "Given an array representing a complete binary tree in level order (-1 for null), compute its height. The height of a tree with only the root is 1 (counting nodes).\n\nInput format:\na\u2081 a\u2082 ... a\u2099 -1 for null nodes\n\nOutput format:\nA single integer\n\nExample:\nInput:\n1 2 3 4 -1 -1 5\n\nOutput:\n3",
            "difficulty": "easy",
            "starter_code": "def solve():\n    arr = list(map(int, input().split()))\n    # Compute the height of the binary tree\n\nsolve()\n",
            "test_cases": [
                {"stdin": "1 2 3 4 -1 -1 5", "expected_output": "3", "is_hidden": False},
                {"stdin": "1", "expected_output": "1", "is_hidden": False},
                {"stdin": "1 2 -1 3 -1 4 -1", "expected_output": "4", "is_hidden": True},
            ],
        },
    ]

def graphs_coding():
    return [
        {
            "title": "DFS Traversal",
            "text": "Given N vertices (1-indexed) and E edges of an undirected graph, followed by a starting vertex S, print the DFS traversal order (visit smaller vertex first when multiple choices).\n\nInput format:\nN E\na\u2081 b\u2081\na\u2082 b\u2082\n...\na\u2091 b\u2091\nS\n\nOutput format:\nSpace-separated vertex numbers in DFS order\n\nExample:\nInput:\n4 3\n1 2\n2 3\n2 4\n1\n\nOutput:\n1 2 3 4",
            "difficulty": "medium",
            "starter_code": "def solve():\n    n, e = map(int, input().split())\n    adj = [[] for _ in range(n + 1)]\n    for _ in range(e):\n        a, b = map(int, input().split())\n        adj[a].append(b)\n        adj[b].append(a)\n    start = int(input())\n    # Perform DFS from start and print traversal\n\nsolve()\n",
            "test_cases": [
                {"stdin": "4 3\n1 2\n2 3\n2 4\n1", "expected_output": "1 2 3 4", "is_hidden": False},
                {"stdin": "3 2\n1 2\n1 3\n1", "expected_output": "1 2 3", "is_hidden": False},
                {"stdin": "5 4\n1 2\n2 3\n3 4\n4 5\n1", "expected_output": "1 2 3 4 5", "is_hidden": True},
            ],
        },
    ]

def dp_coding():
    return [
        {
            "title": "Nth Fibonacci Number",
            "text": "Given N (0 \u2264 N \u2264 10\u2075), compute the Nth Fibonacci number modulo 10\u2079+7. F(0)=0, F(1)=1, F(N)=F(N-1)+F(N-2).\n\nInput format:\nN\n\nOutput format:\nA single integer\n\nExample:\nInput:\n10\n\nOutput:\n55",
            "difficulty": "medium",
            "starter_code": "def solve():\n    n = int(input())\n    MOD = 10**9 + 7\n    # Compute F(n) % MOD\n\nsolve()\n",
            "test_cases": [
                {"stdin": "10", "expected_output": "55", "is_hidden": False},
                {"stdin": "0", "expected_output": "0", "is_hidden": False},
                {"stdin": "50", "expected_output": "12586269025", "is_hidden": True},
            ],
        },
    ]

def basics_coding():
    return [
        {
            "title": "Hello World with Input",
            "text": "Given a name as input, print 'Hello, {name}!'.\n\nInput format:\nA single line containing a name\n\nOutput format:\nHello, {name}!\n\nExample:\nInput:\nAlice\n\nOutput:\nHello, Alice!",
            "difficulty": "easy",
            "starter_code": "def solve():\n    name = input().strip()\n    # Print the greeting\n\nsolve()\n",
            "test_cases": [
                {"stdin": "Alice", "expected_output": "Hello, Alice!", "is_hidden": False},
                {"stdin": "Bob", "expected_output": "Hello, Bob!", "is_hidden": False},
                {"stdin": "", "expected_output": "Hello, !", "is_hidden": True},
            ],
        },
        {
            "title": "FizzBuzz",
            "text": "Given N (1 \u2264 N \u2264 100), print each number from 1 to N on a new line. But for multiples of 3 print 'Fizz', for multiples of 5 print 'Buzz', and for multiples of both 3 and 5 print 'FizzBuzz'.\n\nInput format:\nN\n\nOutput format:\nN lines, each with the number or the appropriate word\n\nExample:\nInput:\n5\n\nOutput:\n1\n2\nFizz\n4\nBuzz",
            "difficulty": "easy",
            "starter_code": "def solve():\n    n = int(input())\n    # Print FizzBuzz for 1 to n\n\nsolve()\n",
            "test_cases": [
                {"stdin": "5", "expected_output": "1\n2\nFizz\n4\nBuzz", "is_hidden": False},
                {"stdin": "1", "expected_output": "1", "is_hidden": False},
                {"stdin": "15", "expected_output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz", "is_hidden": True},
            ],
        },
    ]

def data_types_coding():
    return [
        {
            "title": "String Reversal",
            "text": "Given a string S (1 \u2264 |S| \u2264 1000), reverse it character by character and print the result.\n\nInput format:\nA single line containing S\n\nOutput format:\nThe reversed string\n\nExample:\nInput:\nhello\n\nOutput:\nolleh",
            "difficulty": "easy",
            "starter_code": "def solve():\n    s = input().strip()\n    # Reverse and print\n\nsolve()\n",
            "test_cases": [
                {"stdin": "hello", "expected_output": "olleh", "is_hidden": False},
                {"stdin": "a", "expected_output": "a", "is_hidden": False},
                {"stdin": "racecar", "expected_output": "racecar", "is_hidden": True},
            ],
        },
    ]

def oop_coding():
    return [
        {
            "title": "Class for Circle",
            "text": "Complete the program to define a Circle class with a constructor (radius) and an area() method. Read radius and print the area (use \u03c0 = 3.14159).\n\nInput format:\nA single float radius (0 < r \u2264 10\u2074)\n\nOutput format:\nThe area as a float (round to 2 decimal places)\n\nExample:\nInput:\n5\n\nOutput:\n78.54",
            "difficulty": "medium",
            "starter_code": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n    \n    def area(self):\n        # Compute and return the area\n        pass\n\ndef solve():\n    r = float(input())\n    c = Circle(r)\n    print(f'{c.area():.2f}')\n\nsolve()\n",
            "test_cases": [
                {"stdin": "5", "expected_output": "78.54", "is_hidden": False},
                {"stdin": "1", "expected_output": "3.14", "is_hidden": False},
                {"stdin": "10", "expected_output": "314.16", "is_hidden": True},
            ],
        },
    ]

def file_handling_coding():
    return [
        {
            "title": "Count Lines in String",
            "text": "Given a multi-line string (ending with 'END'), count the number of lines (excluding the 'END' marker). Print the count.\n\nInput format:\nMultiple lines of text ending with 'END' on its own line\n\nOutput format:\nA single integer\n\nExample:\nInput:\nHello\nWorld\nFoo\nEND\n\nOutput:\n3",
            "difficulty": "easy",
            "starter_code": "def solve():\n    count = 0\n    while True:\n        line = input()\n        if line == 'END':\n            break\n        count += 1\n    print(count)\n\nsolve()\n",
            "test_cases": [
                {"stdin": "Hello\nWorld\nEND", "expected_output": "2", "is_hidden": False},
                {"stdin": "END", "expected_output": "0", "is_hidden": False},
                {"stdin": "A\nB\nC\nD\nEND", "expected_output": "4", "is_hidden": True},
            ],
        },
    ]

def libraries_coding():
    return [
        {
            "title": "Generate Random Password",
            "text": "Given length L (4 \u2264 L \u2264 20), generate a random password of length L containing lowercase letters, uppercase letters, and digits. Print the password.\n\nInput format:\nL\n\nOutput format:\nA single line\n\nExample:\nInput:\n8\n\nOutput:\naB3dEf7g\n(Actual output will vary due to randomness)",
            "difficulty": "medium",
            "starter_code": "import random\nimport string\n\ndef solve():\n    L = int(input())\n    # Generate and print a random password of length L\n\nsolve()\n",
            "test_cases": [
                {"stdin": "8", "expected_output": "", "is_hidden": False},
            ],
        },
    ]

# ─── Write all remaining coding files ───────────────────────

CODING_GENERATORS = {
    "linked_lists": linked_lists_coding,
    "trees": trees_coding,
    "graphs": graphs_coding,
    "dynamic_programming": dp_coding,
    "basics": basics_coding,
    "data_types": data_types_coding,
    "oop": oop_coding,
    "file_handling": file_handling_coding,
    "libraries": libraries_coding,
}

for topic_name, generator in CODING_GENERATORS.items():
    path = os.path.join(CODING_DIR, f"{topic_name}.json")
    problems = generator()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(problems)} coding to coding/{topic_name}.json")
