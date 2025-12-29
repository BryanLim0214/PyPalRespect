"""
Python curriculum exercises for ADHD middle schoolers.
"""
import json

EXERCISES = [
    {
        "title": "Hello Coder",
        "description": "Write your first Python program! Make the computer say hello.",
        "difficulty": 1,
        "concept": "print",
        "grade_level": 6,
        "estimated_minutes": 5,
        "step_count": 2,
        "interest_tags": json.dumps(["games", "coding"]),
        "starter_code": "# Welcome to Python!\n# Your goal: Make the computer say 'Hello, World!'\n\n",
        "solution_code": 'print("Hello, World!")',
        "test_cases": json.dumps([{"input": "", "expected_output": "Hello, World!"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Type the magic word", "instruction": "Type: print", "checkpoint": False},
            {"number": 2, "title": "Add your message", "instruction": 'Add parentheses and quotes: print("Hello, World!")', "checkpoint": True}
        ])
    },
    {
        "title": "Math Magic",
        "description": "Use Python as a super calculator! Store numbers and do math.",
        "difficulty": 1,
        "concept": "variables",
        "grade_level": 6,
        "estimated_minutes": 10,
        "step_count": 3,
        "interest_tags": json.dumps(["games", "math"]),
        "starter_code": "# Let's do some math!\n# Goal: Calculate your score in a game\n\n",
        "solution_code": 'level1_score = 50\nlevel2_score = 75\ntotal = level1_score + level2_score\nprint("Total score:", total)',
        "test_cases": json.dumps([{"input": "", "expected_output": "Total score: 125"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Store your first score", "instruction": "Type: level1_score = 50", "checkpoint": False},
            {"number": 2, "title": "Store your second score", "instruction": "Type: level2_score = 75", "checkpoint": False},
            {"number": 3, "title": "Add them up", "instruction": 'Type: total = level1_score + level2_score', "checkpoint": True}
        ])
    },
    {
        "title": "Build Your Profile",
        "description": "Create a cool profile card using text and variables!",
        "difficulty": 1,
        "concept": "strings",
        "grade_level": 6,
        "estimated_minutes": 10,
        "step_count": 3,
        "interest_tags": json.dumps(["art", "social"]),
        "starter_code": "# Create your profile card!\n\n",
        "solution_code": 'name = "Alex"\nage = 12\nprint("=== PROFILE ===")\nprint("Name:", name)\nprint("Age:", age)',
        "test_cases": json.dumps([{"input": "", "expected_output": "=== PROFILE ===\nName: Alex\nAge: 12"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Pick your name", "instruction": 'Type: name = "Alex"', "checkpoint": False},
            {"number": 2, "title": "Add your age", "instruction": "Type: age = 12", "checkpoint": False},
            {"number": 3, "title": "Print your profile", "instruction": "Print a header and your info", "checkpoint": True}
        ])
    },
    {
        "title": "High Score Tracker",
        "description": "Check if you beat the high score using if statements!",
        "difficulty": 2,
        "concept": "conditionals",
        "grade_level": 6,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["games"]),
        "starter_code": "# High Score Checker!\nhigh_score = 100\nyour_score = 120\n\n",
        "solution_code": 'high_score = 100\nyour_score = 120\nif your_score > high_score:\n    print("NEW HIGH SCORE!")\nelse:\n    print("Try again!")',
        "test_cases": json.dumps([{"input": "", "expected_output": "NEW HIGH SCORE!"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Look at the scores", "instruction": "See the scores? We will compare them!", "checkpoint": False},
            {"number": 2, "title": "Write the if statement", "instruction": "Type: if your_score > high_score:", "checkpoint": False},
            {"number": 3, "title": "What happens if you win", "instruction": 'Press Tab, then: print("NEW HIGH SCORE!")', "checkpoint": True},
            {"number": 4, "title": "What if you dont beat it", "instruction": 'Add: else: print("Try again!")', "checkpoint": True}
        ])
    },
    {
        "title": "Grade Checker",
        "description": "Build a program that turns test scores into letter grades!",
        "difficulty": 2,
        "concept": "if-else",
        "grade_level": 6,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["school"]),
        "starter_code": "# Grade Calculator\nscore = 85\n\n",
        "solution_code": 'score = 85\nif score >= 90:\n    print("A - Excellent!")\nelif score >= 80:\n    print("B - Great job!")\nelse:\n    print("Keep practicing!")',
        "test_cases": json.dumps([{"input": "", "expected_output": "B - Great job!"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Check for an A", "instruction": "Type: if score >= 90:", "checkpoint": False},
            {"number": 2, "title": "Check for a B", "instruction": "Type: elif score >= 80:", "checkpoint": True},
            {"number": 3, "title": "Everything else", "instruction": "Type: else:", "checkpoint": False},
            {"number": 4, "title": "Test different scores", "instruction": "Change score and run again!", "checkpoint": True}
        ])
    },
    {
        "title": "Rocket Countdown",
        "description": "Use a loop to count down and launch a rocket!",
        "difficulty": 2,
        "concept": "loops",
        "grade_level": 6,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["space", "games"]),
        "starter_code": "# Rocket Launch Countdown!\n\n",
        "solution_code": 'for i in range(5, 0, -1):\n    print(i)\nprint("LIFTOFF!")',
        "test_cases": json.dumps([{"input": "", "expected_output": "5\n4\n3\n2\n1\nLIFTOFF!"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Start the loop", "instruction": "Type: for i in range(5, 0, -1):", "checkpoint": False},
            {"number": 2, "title": "Print each number", "instruction": "Press Tab, then type: print(i)", "checkpoint": True},
            {"number": 3, "title": "Add liftoff", "instruction": 'Type: print("LIFTOFF!")', "checkpoint": False},
            {"number": 4, "title": "Run it!", "instruction": "Click Run and watch the countdown!", "checkpoint": True}
        ])
    },
    {
        "title": "Favorite Songs Playlist",
        "description": "Create a playlist of your favorite songs using a list!",
        "difficulty": 2,
        "concept": "lists",
        "grade_level": 7,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["music"]),
        "starter_code": "# My Playlist\n\n",
        "solution_code": 'songs = ["Song 1", "Song 2", "Song 3"]\nprint("My Playlist:")\nfor song in songs:\n    print("  -", song)',
        "test_cases": json.dumps([{"input": "", "expected_output": "My Playlist:\n  - Song 1\n  - Song 2\n  - Song 3"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Create your playlist", "instruction": 'Type: songs = ["Song 1", "Song 2"]', "checkpoint": False},
            {"number": 2, "title": "Print a header", "instruction": 'Type: print("My Playlist:")', "checkpoint": False},
            {"number": 3, "title": "Loop through songs", "instruction": "Type: for song in songs:", "checkpoint": False},
            {"number": 4, "title": "Print each song", "instruction": 'Type: print("  -", song)', "checkpoint": True}
        ])
    },
    {
        "title": "Shopping Cart",
        "description": "Build a shopping cart and calculate the total!",
        "difficulty": 3,
        "concept": "list-methods",
        "grade_level": 7,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["games", "shopping"]),
        "starter_code": "# Shopping Cart\nprices = [5, 10, 3, 8]\n\n",
        "solution_code": 'prices = [5, 10, 3, 8]\ntotal = sum(prices)\nprint("Items:", len(prices))\nprint("Total: $" + str(total))',
        "test_cases": json.dumps([{"input": "", "expected_output": "Items: 4\nTotal: $26"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Look at the prices", "instruction": "We have a list of prices!", "checkpoint": False},
            {"number": 2, "title": "Calculate the total", "instruction": "Type: total = sum(prices)", "checkpoint": True},
            {"number": 3, "title": "Count the items", "instruction": 'Type: print("Items:", len(prices))', "checkpoint": False},
            {"number": 4, "title": "Show the total", "instruction": 'Type: print("Total: $" + str(total))', "checkpoint": True}
        ])
    },
    {
        "title": "Password Maker",
        "description": "Create a function that generates fun passwords!",
        "difficulty": 3,
        "concept": "functions",
        "grade_level": 7,
        "estimated_minutes": 20,
        "step_count": 5,
        "interest_tags": json.dumps(["security", "coding"]),
        "starter_code": "# Password Generator\nimport random\nwords = ['dragon', 'ninja', 'robot']\nnumbers = ['123', '456', '789']\n\n",
        "solution_code": 'import random\nwords = ["dragon", "ninja", "robot"]\nnumbers = ["123", "456", "789"]\ndef make_password():\n    return random.choice(words) + random.choice(numbers)\nprint("Your password:", make_password())',
        "steps": json.dumps([
            {"number": 1, "title": "Start your function", "instruction": "Type: def make_password():", "checkpoint": False},
            {"number": 2, "title": "Pick a random word", "instruction": "word = random.choice(words)", "checkpoint": False},
            {"number": 3, "title": "Pick a random number", "instruction": "num = random.choice(numbers)", "checkpoint": True},
            {"number": 4, "title": "Combine them", "instruction": "return word + num", "checkpoint": False},
            {"number": 5, "title": "Use your function", "instruction": 'print("Your password:", make_password())', "checkpoint": True}
        ])
    },
    {
        "title": "Build a Calculator",
        "description": "Create functions for add, subtract, multiply, divide!",
        "difficulty": 3,
        "concept": "functions",
        "grade_level": 7,
        "estimated_minutes": 20,
        "step_count": 5,
        "interest_tags": json.dumps(["math", "coding"]),
        "starter_code": "# My Calculator\n\n",
        "solution_code": 'def add(a, b):\n    return a + b\ndef subtract(a, b):\n    return a - b\nprint("10 + 5 =", add(10, 5))\nprint("10 - 5 =", subtract(10, 5))',
        "test_cases": json.dumps([{"input": "", "expected_output": "10 + 5 = 15\n10 - 5 = 5"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Create the add function", "instruction": "def add(a, b): return a + b", "checkpoint": True},
            {"number": 2, "title": "Create subtract function", "instruction": "def subtract(a, b): return a - b", "checkpoint": False},
            {"number": 3, "title": "Test add", "instruction": 'print("10 + 5 =", add(10, 5))', "checkpoint": False},
            {"number": 4, "title": "Test subtract", "instruction": 'print("10 - 5 =", subtract(10, 5))', "checkpoint": True},
            {"number": 5, "title": "Try your own numbers", "instruction": "Change the numbers!", "checkpoint": True}
        ])
    },
    {
        "title": "Mad Libs Story",
        "description": "Create a funny story by combining words!",
        "difficulty": 2,
        "concept": "combining",
        "grade_level": 7,
        "estimated_minutes": 15,
        "step_count": 4,
        "interest_tags": json.dumps(["games", "creative"]),
        "starter_code": "# Mad Libs!\n\n",
        "solution_code": 'name = "Alex"\nanimal = "dragon"\nfood = "pizza"\nstory = name + " saw a " + animal + " eating " + food\nprint(story)',
        "test_cases": json.dumps([{"input": "", "expected_output": "Alex saw a dragon eating pizza"}]),
        "steps": json.dumps([
            {"number": 1, "title": "Pick a name", "instruction": 'Type: name = "Alex"', "checkpoint": False},
            {"number": 2, "title": "Pick an animal", "instruction": 'Type: animal = "dragon"', "checkpoint": False},
            {"number": 3, "title": "Pick a food", "instruction": 'Type: food = "pizza"', "checkpoint": False},
            {"number": 4, "title": "Create the story", "instruction": "Combine them all together!", "checkpoint": True}
        ])
    },
    {
        "title": "Number Guessing Game",
        "description": "Build a complete game where the computer picks a number!",
        "difficulty": 3,
        "concept": "text-games",
        "grade_level": 8,
        "estimated_minutes": 25,
        "step_count": 5,
        "interest_tags": json.dumps(["games"]),
        "starter_code": "# Number Guessing Game\nimport random\nsecret = random.randint(1, 10)\nprint('I am thinking of a number 1-10...')\n\n",
        "solution_code": 'import random\nsecret = random.randint(1, 10)\nfor attempt in range(3):\n    guess = int(input("Your guess: "))\n    if guess == secret:\n        print("Correct!")\n        break\n    elif guess < secret:\n        print("Higher!")\n    else:\n        print("Lower!")',
        "steps": json.dumps([
            {"number": 1, "title": "Set up the loop", "instruction": "Type: for attempt in range(3):", "checkpoint": False},
            {"number": 2, "title": "Get the players guess", "instruction": 'guess = int(input("Your guess: "))', "checkpoint": True},
            {"number": 3, "title": "Check if correct", "instruction": "if guess == secret: print('Correct!'); break", "checkpoint": False},
            {"number": 4, "title": "Give hints", "instruction": "elif and else for Higher/Lower hints", "checkpoint": True},
            {"number": 5, "title": "Show the answer", "instruction": "Add else clause to show secret", "checkpoint": True}
        ])
    },
    {
        "title": "Choose Your Adventure",
        "description": "Create an interactive story where choices matter!",
        "difficulty": 4,
        "concept": "text-games",
        "grade_level": 8,
        "estimated_minutes": 25,
        "step_count": 5,
        "interest_tags": json.dumps(["games", "creative"]),
        "starter_code": "# Choose Your Adventure\nprint('You find a mysterious door.')\nprint('1. Open it')\nprint('2. Walk away')\n\n",
        "solution_code": 'print("You find a mysterious door.")\nchoice = input("Choose 1 or 2: ")\nif choice == "1":\n    print("You found treasure!")\nelse:\n    print("You take the safe path home.")',
        "test_cases": json.dumps([
            {"input": "1", "expected_output": "You find a mysterious door.\nChoose 1 or 2: You found treasure!"},
            {"input": "2", "expected_output": "You find a mysterious door.\nChoose 1 or 2: You take the safe path home."}
        ]),
        "steps": json.dumps([
            {"number": 1, "title": "Get the players choice", "instruction": 'choice = input("Choose 1 or 2: ")', "checkpoint": True},
            {"number": 2, "title": "Handle choice 1", "instruction": 'if choice == "1": print("You found treasure!")', "checkpoint": False},
            {"number": 3, "title": "Handle choice 2", "instruction": 'else: print("Safe path home")', "checkpoint": True},
            {"number": 4, "title": "Add more options", "instruction": "Try adding more choices with elif!", "checkpoint": False},
            {"number": 5, "title": "Make it longer", "instruction": "Add another choice after the first!", "checkpoint": True}
        ])
    },
    {
        "title": "Quiz Builder",
        "description": "Create a quiz game with questions and scoring!",
        "difficulty": 3,
        "concept": "data",
        "grade_level": 8,
        "estimated_minutes": 20,
        "step_count": 5,
        "interest_tags": json.dumps(["games", "school"]),
        "starter_code": "# Quiz Game\nquestions = [\n    ('What is 2 + 2?', '4'),\n    ('What color is the sky?', 'blue'),\n]\nscore = 0\n\n",
        "solution_code": 'questions = [("What is 2 + 2?", "4"), ("What color is the sky?", "blue")]\nscore = 0\nfor question, answer in questions:\n    guess = input(question + " ")\n    if guess.lower() == answer:\n        print("Correct!")\n        score += 1\n    else:\n        print("Nope, it was:", answer)\nprint("Score:", score)',
        "test_cases": json.dumps([
            {"input": "4\nblue", "expected_output": "What is 2 + 2? Correct!\nWhat color is the sky? Correct!\nScore: 2"},
            {"input": "5\nred", "expected_output": "What is 2 + 2? Nope, it was: 4\nWhat color is the sky? Nope, it was: blue\nScore: 0"}
        ]),
        "steps": json.dumps([
            {"number": 1, "title": "Loop through questions", "instruction": "for question, answer in questions:", "checkpoint": False},
            {"number": 2, "title": "Ask the question", "instruction": 'guess = input(question + " ")', "checkpoint": True},
            {"number": 3, "title": "Check the answer", "instruction": "if guess.lower() == answer: score += 1", "checkpoint": False},
            {"number": 4, "title": "Handle wrong answers", "instruction": 'else: print("Nope, it was:", answer)', "checkpoint": True},
            {"number": 5, "title": "Show final score", "instruction": 'print("Score:", score)', "checkpoint": True}
        ])
    },
    {
        "title": "Digital Journal",
        "description": "Write journal entries and save them!",
        "difficulty": 3,
        "concept": "files",
        "grade_level": 8,
        "estimated_minutes": 20,
        "step_count": 5,
        "interest_tags": json.dumps(["creative", "personal"]),
        "starter_code": "# Digital Journal\nfrom datetime import datetime\n\n",
        "solution_code": 'from datetime import datetime\nentry = input("Write your entry: ")\ndate = datetime.now().strftime("%Y-%m-%d")\njournal_entry = f"--- {date} ---\\n{entry}\\n"\nprint("Saved entry:")\nprint(journal_entry)',
        "steps": json.dumps([
            {"number": 1, "title": "Get the journal entry", "instruction": 'entry = input("Write your entry: ")', "checkpoint": True},
            {"number": 2, "title": "Get todays date", "instruction": 'date = datetime.now().strftime("%Y-%m-%d")', "checkpoint": False},
            {"number": 3, "title": "Format the entry", "instruction": 'journal_entry = f"--- {date} ---\\n{entry}"', "checkpoint": True},
            {"number": 4, "title": "Display it", "instruction": 'print("Saved entry:"); print(journal_entry)', "checkpoint": False},
            {"number": 5, "title": "Try it out", "instruction": "Run and write a short entry!", "checkpoint": True}
        ])
    },
]


def get_all_exercises():
    """Return all curriculum exercises."""
    return EXERCISES


def get_exercises_by_grade(grade_level: int):
    """Return exercises for a specific grade."""
    return [ex for ex in EXERCISES if ex["grade_level"] == grade_level]


def get_exercises_by_concept(concept: str):
    """Return exercises for a specific concept."""
    return [ex for ex in EXERCISES if ex["concept"] == concept]
