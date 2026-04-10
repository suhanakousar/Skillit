"""Python: Beginner-to-Pro roadmap — fully embedded curriculum.

This file materializes the Python roadmap (stages 1-6) as TechPath content:
tracks, story-mode lessons with quizzes, practice problems with test cases,
and capstone projects. Every piece of content is self-contained — no external
links, no videos, no paid resources. The student reads the story, hits the
quiz, writes the code, and ships the project, all inside the app.

Exports:
    PYTHON_ROADMAP_TRACKS     — list of (name, slug, domain, year, desc, hours, xp)
    PYTHON_ROADMAP_LESSONS    — dict[track_slug, list[lesson_dict]]
    PYTHON_ROADMAP_PROBLEMS   — list of problem dicts with `track_slug`
    PYTHON_ROADMAP_PROJECTS   — list of (year, title, slug, desc, stack, xp)
"""

# =============================================================================
# TRACKS — one per roadmap stage, plus four Stage-5 specializations
# =============================================================================
PYTHON_ROADMAP_TRACKS: list[tuple] = [
    # (name, slug, domain, year, description, hours, xp)
    (
        "Python Stage 1 — Absolute Beginner",
        "python-stage-1-beginner",
        "Programming",
        1,
        "Weeks 1-3. Your first Python. Setup, variables, strings, numbers, input, "
        "if/else, loops, lists, dicts, functions, errors. End with a working "
        "calculator, a number-guessing game, and a temperature converter.",
        30,
        500,
    ),
    (
        "Python Stage 2 — Core Fundamentals",
        "python-stage-2-core",
        "Programming",
        1,
        "Weeks 4-7. Comprehensions, file I/O, modules, exceptions, lambdas, "
        "map/filter/zip, *args/**kwargs, virtual envs, pip, regex. Build a "
        "CLI to-do app, a word-frequency counter, and a CSV data reader.",
        35,
        700,
    ),
    (
        "Python Stage 3 — Object-Oriented Python",
        "python-stage-3-oop",
        "Programming",
        2,
        "Weeks 8-11. Classes, __init__, inheritance, polymorphism, "
        "encapsulation, dunder methods, decorators, properties, abstract "
        "classes, dataclasses. Build a bank, a library, and a card game.",
        40,
        900,
    ),
    (
        "Python Stage 4 — Intermediate Python",
        "python-stage-4-intermediate",
        "Programming",
        2,
        "Weeks 12-16. Generators, context managers, threading, async/await, "
        "type hints, pytest, debugging, JSON & APIs, web scraping, SQLite. "
        "Build a weather app, a news scraper, and a SQLite expense tracker.",
        50,
        1100,
    ),
    (
        "Python Stage 5 — Web Specialization",
        "python-stage-5-web",
        "Web",
        3,
        "Weeks 17-24. Flask and Django, REST APIs, templating, sessions, "
        "authentication, and deployment. Ship a real web app.",
        45,
        1000,
    ),
    (
        "Python Stage 5 — Data Science Specialization",
        "python-stage-5-data",
        "ML",
        3,
        "Weeks 17-24. NumPy, Pandas, Matplotlib, Seaborn, Jupyter, and the art "
        "of cleaning messy real-world data.",
        45,
        1000,
    ),
    (
        "Python Stage 5 — AI / ML Specialization",
        "python-stage-5-ai",
        "ML",
        3,
        "Weeks 17-24. Scikit-learn, TensorFlow/Keras, PyTorch, NLP basics, "
        "model evaluation, and a peek at computer vision.",
        50,
        1100,
    ),
    (
        "Python Stage 5 — Automation Specialization",
        "python-stage-5-auto",
        "DevOps",
        3,
        "Weeks 17-24. OS & sys modules, Selenium, task scheduling, email "
        "automation, Excel with openpyxl, and PDF handling. Automate the "
        "boring stuff for real.",
        40,
        900,
    ),
    (
        "Python Stage 6 — Pro Level",
        "python-stage-6-pro",
        "Programming",
        4,
        "Weeks 25+. Design patterns, clean code, performance, memory, CI/CD, "
        "Docker, TDD, open source, code reviews, and publishing your own "
        "Python package to PyPI.",
        60,
        1400,
    ),
]


# =============================================================================
# LESSONS — story-mode lessons per track
# =============================================================================
# Helper to keep lesson dicts readable.
def _lesson(title, hook, aha, concept, walkthrough, mistakes, quiz, xp=10, mins=8):
    return {
        "title": title,
        "type": "story",
        "xp_reward": xp,
        "duration_minutes": mins,
        "content_json": {
            "hook_story": hook,
            "aha_moment": aha,
            "concept_explained": concept,
            "code_walkthrough": walkthrough,
            "common_mistakes": mistakes,
            "quiz": quiz,
        },
    }


PYTHON_ROADMAP_LESSONS: dict[str, list[dict]] = {
    # =========================================================================
    # STAGE 1 — Absolute Beginner
    # =========================================================================
    "python-stage-1-beginner": [
        _lesson(
            "01 · What is Python & setting it up",
            "Imagine a friendly robot that does exactly what you type. You say `print('hi')` and it prints 'hi'. You say `5 + 3` and it says 8. That robot is Python — a language designed to read like English so you spend your energy on ideas, not syntax.",
            "Python is just a program on your computer that reads text files line by line and does what they say.",
            "Python comes in two pieces: the language (the rules of what you can write) and the interpreter (the program that runs your code). Install Python from python.org, open a terminal, type `python`, and you get an interactive prompt called the REPL. Save code in a file ending with `.py` and run it with `python file.py`.",
            [
                {"step": 1, "comment": "Your very first line", "code": "print('Hello, world!')"},
                {"step": 2, "comment": "Python also does math", "code": "print(2 + 2)\nprint(10 * 7)"},
                {"step": 3, "comment": "Save this as hello.py and run python hello.py", "code": "print('I am learning Python!')"},
            ],
            [
                "Confusing Python 2 and Python 3 — always use Python 3.",
                "Forgetting the parentheses on `print(...)`.",
            ],
            [
                {
                    "question": "Which file extension does Python source code use?",
                    "options": [".py", ".pt", ".python", ".pyc"],
                    "correct": ".py",
                    "explanation": ".py is the standard source file. .pyc is compiled bytecode.",
                }
            ],
            xp=10, mins=6,
        ),
        _lesson(
            "02 · Variables & data types",
            "A variable is like a sticky note with a name on one side and a value on the other. Write `age = 21`, and you've just stuck the label `age` onto the number 21. Next time you say `age`, Python looks at the note and reads back 21.",
            "Variables aren't boxes. They're names pointing at values.",
            "Python has four core data types you'll meet on day one: `int` (whole numbers), `float` (decimals), `str` (text), and `bool` (True/False). You don't declare the type — Python figures it out from the value. Use `type(x)` to check, and `print()` to display.",
            [
                {"step": 1, "comment": "One of each basic type", "code": "age = 21            # int\nprice = 99.5        # float\nname = 'Suhana'     # str\nis_student = True   # bool"},
                {"step": 2, "comment": "Ask Python what type it is", "code": "print(type(age))    # <class 'int'>"},
                {"step": 3, "comment": "Reassigning is allowed — types can change", "code": "age = 'twenty-one'\nprint(type(age))    # <class 'str'>"},
            ],
            [
                "Starting a variable name with a number (`1name`) — that's a SyntaxError.",
                "Using Python keywords like `class` or `for` as variable names.",
            ],
            [
                {
                    "question": "What is `type(3.0)`?",
                    "options": ["int", "float", "number", "decimal"],
                    "correct": "float",
                    "explanation": "Any number with a decimal point is a float.",
                }
            ],
            xp=10, mins=7,
        ),
        _lesson(
            "03 · Strings & numbers",
            "Strings are just text in quotes, but Python treats them like tiny assembly lines you can slice, join, and reshape. And numbers? Python will happily handle integers with a thousand digits without breaking a sweat.",
            "A string is an ordered sequence of characters — think of it as a list of letters you can index into.",
            "Use single or double quotes for strings — Python doesn't care. Use `+` to join strings and `*` to repeat them. For numbers, `+ - * /` work as expected, plus `//` for integer division, `%` for remainder, and `**` for power. Mix them with f-strings: `f'Hi {name}, you are {age}'`.",
            [
                {"step": 1, "comment": "String basics", "code": "name = 'Arjun'\nprint(name[0])      # 'A'  — first character\nprint(len(name))    # 5    — how many characters"},
                {"step": 2, "comment": "String slicing", "code": "word = 'Python'\nprint(word[0:3])    # 'Pyt'\nprint(word[-1])     # 'n'  — last character"},
                {"step": 3, "comment": "Number operations and f-strings", "code": "x, y = 7, 2\nprint(x / y)        # 3.5\nprint(x // y)       # 3\nprint(x ** y)       # 49\nprint(f'{x} and {y} together: {x + y}')"},
            ],
            [
                "Dividing with `/` when you wanted integer division (use `//`).",
                "Forgetting that `str[-1]` is the last character, not the one before the last.",
            ],
            [
                {
                    "question": "What does `'ab' * 3` produce?",
                    "options": ["'ababab'", "'ab3'", "'ab ab ab'", "Error"],
                    "correct": "'ababab'",
                    "explanation": "`*` on a string repeats it.",
                }
            ],
            xp=10, mins=8,
        ),
        _lesson(
            "04 · Input & print",
            "A program that can't talk to the user is a monologue. Python gives you two microphones: `input()` listens, and `print()` speaks.",
            "`input()` always returns a string — even if the user types a number. If you want a number, you must convert it.",
            "`input(prompt)` stops the program, shows the prompt, and waits for the user to press Enter. Whatever they typed comes back as a string. `print()` can take many arguments separated by commas and a `sep=` / `end=` to control spacing and line endings.",
            [
                {"step": 1, "comment": "Get a name", "code": "name = input('What is your name? ')\nprint('Hello,', name)"},
                {"step": 2, "comment": "Numbers need conversion", "code": "age = int(input('Your age? '))\nprint(f'Next year you will be {age + 1}')"},
                {"step": 3, "comment": "Fancy print", "code": "print('a', 'b', 'c', sep='-')  # a-b-c\nprint('no newline', end=' ')\nprint('same line')"},
            ],
            [
                "Forgetting to cast input with `int()` or `float()` and then doing math on a string.",
                "Expecting a space after the prompt in `input()` — you must include it in the prompt string.",
            ],
            [
                {
                    "question": "What does `input()` return when the user types `42`?",
                    "options": ["The int 42", "The float 42.0", "The string '42'", "None"],
                    "correct": "The string '42'",
                    "explanation": "`input()` always returns str; you must cast it to use as a number.",
                }
            ],
            xp=10, mins=6,
        ),
        _lesson(
            "05 · If / elif / else",
            "Imagine a bouncer at a club. Over 18? You're in. Exactly 18? Still in, but check the ID twice. Under 18? Go home. That cascading decision is exactly what if/elif/else does in code.",
            "An `if` ladder runs at most one branch — Python stops at the first True condition.",
            "Conditions use `==`, `!=`, `<`, `<=`, `>`, `>=`, and combinators `and`, `or`, `not`. Indentation (4 spaces) defines what's inside the branch. `elif` means 'else if' and you can have as many as you like. `else` is the fallback.",
            [
                {"step": 1, "comment": "Classic ladder", "code": "age = int(input('Age? '))\nif age >= 18:\n    print('Adult')\nelif age >= 13:\n    print('Teen')\nelse:\n    print('Kid')"},
                {"step": 2, "comment": "Combining conditions", "code": "score = 85\nif score >= 90 and score <= 100:\n    print('A')\nelif score >= 75:\n    print('B')\nelse:\n    print('Keep trying')"},
            ],
            [
                "Using `=` (assignment) instead of `==` (comparison).",
                "Forgetting the colon at the end of `if`, `elif`, or `else`.",
                "Mixing tabs and spaces for indentation.",
            ],
            [
                {
                    "question": "Which runs when `x = 10`: `if x > 5: print('A')\\nelif x > 0: print('B')`?",
                    "options": ["Only A", "Only B", "Both", "Neither"],
                    "correct": "Only A",
                    "explanation": "Python exits the ladder after the first True branch.",
                }
            ],
            xp=10, mins=8,
        ),
        _lesson(
            "06 · Loops: for & while",
            "You wouldn't write 'Happy Birthday' fifty times by hand. You'd say 'print it fifty times'. That's a loop.",
            "Use `for` when you know what you're walking over. Use `while` when you're waiting for a condition to flip.",
            "`for x in something:` iterates over lists, strings, ranges, files — anything Python can walk through. `while condition:` keeps running as long as the condition is True. `break` exits early, `continue` skips to the next iteration.",
            [
                {"step": 1, "comment": "For over a range", "code": "for i in range(5):\n    print(i)        # 0,1,2,3,4"},
                {"step": 2, "comment": "For over a list", "code": "for fruit in ['apple', 'mango', 'kiwi']:\n    print(fruit)"},
                {"step": 3, "comment": "While loop with break", "code": "n = 0\nwhile True:\n    n += 1\n    if n > 3:\n        break\n    print(n)"},
            ],
            [
                "Infinite while loop — forgetting to update the loop variable.",
                "Off-by-one: `range(1, 10)` stops at 9, not 10.",
            ],
            [
                {
                    "question": "How many numbers does `range(2, 8)` produce?",
                    "options": ["5", "6", "7", "8"],
                    "correct": "6",
                    "explanation": "range(a, b) gives a, a+1, ..., b-1 — that's b - a = 6 numbers.",
                }
            ],
            xp=10, mins=9,
        ),
        _lesson(
            "07 · Lists & tuples",
            "A list is a row of numbered slots you can fill, swap, and reorder. A tuple is the same row bolted to the floor — you can look at things but you can't move them.",
            "Lists are mutable (changeable), tuples are immutable (frozen). Pick based on whether the data should be allowed to change.",
            "Create lists with `[]`, tuples with `()`. Both support indexing with `[i]`, slicing with `[a:b]`, `len()`, and `in`. Lists add methods like `append`, `pop`, `sort`, `reverse`. Tuples can be unpacked: `x, y = (1, 2)`.",
            [
                {"step": 1, "comment": "Build and mutate a list", "code": "nums = [3, 1, 4]\nnums.append(1)        # [3,1,4,1]\nnums.sort()           # [1,1,3,4]\nprint(nums[-1])       # 4"},
                {"step": 2, "comment": "Tuples and unpacking", "code": "point = (10, 20)\nx, y = point\nprint(x + y)          # 30"},
                {"step": 3, "comment": "Slicing reviewed", "code": "nums = [10, 20, 30, 40, 50]\nprint(nums[1:4])      # [20, 30, 40]\nprint(nums[::-1])     # reversed"},
            ],
            [
                "Trying to `tuple[0] = x` — immutable, raises TypeError.",
                "Confusing `append(x)` (adds one item) with `extend(list)` (adds each item).",
            ],
            [
                {
                    "question": "Which is immutable?",
                    "options": ["list", "tuple", "dict", "set"],
                    "correct": "tuple",
                    "explanation": "Tuples cannot be changed after creation.",
                }
            ],
            xp=10, mins=9,
        ),
        _lesson(
            "08 · Dictionaries & sets",
            "A dictionary is a phone book — you look up a name (key) and get a number (value). A set is the guest list at a party — order doesn't matter but duplicates are forbidden.",
            "Dicts give you O(1) lookup by key. Sets give you O(1) 'is this in here?' checks.",
            "`dict` uses `{key: value, ...}`. Access with `d[key]` or safely with `d.get(key, default)`. `set` uses `{a, b, c}` (but `set()` for empty — `{}` is an empty dict!). Sets support union `|`, intersection `&`, and difference `-`.",
            [
                {"step": 1, "comment": "Dict basics", "code": "student = {'name': 'Arjun', 'age': 20}\nstudent['college'] = 'KLU'\nprint(student.get('phone', 'unknown'))"},
                {"step": 2, "comment": "Walking a dict", "code": "for key, value in student.items():\n    print(key, '=', value)"},
                {"step": 3, "comment": "Set operations", "code": "a = {1, 2, 3}\nb = {3, 4, 5}\nprint(a | b)          # union {1,2,3,4,5}\nprint(a & b)          # intersection {3}"},
            ],
            [
                "Using `d[key]` for a missing key — raises KeyError. Prefer `d.get(key, default)`.",
                "Writing `{}` to make an empty set — that creates an empty dict. Use `set()`.",
            ],
            [
                {
                    "question": "What does `{1, 2, 2, 3, 3, 3}` evaluate to?",
                    "options": ["{1, 2, 3}", "{1, 2, 2, 3, 3, 3}", "[1,2,3]", "Error"],
                    "correct": "{1, 2, 3}",
                    "explanation": "Sets drop duplicates automatically.",
                }
            ],
            xp=10, mins=10,
        ),
        _lesson(
            "09 · Functions & scope",
            "You're tired of writing the same five lines every time you greet someone. You want to teach Python a new verb called `greet`. That's what `def` does.",
            "A function bundles logic under a name. Call the name, get the result — the caller doesn't need to know how it works inside.",
            "`def name(params): ... return value`. Variables created inside a function are local — they vanish when the function ends. To read an outer variable, just use it. To modify one, you need `global` or `nonlocal`.",
            [
                {"step": 1, "comment": "Define and call", "code": "def greet(name):\n    return f'Hi {name}!'\n\nprint(greet('Suhana'))"},
                {"step": 2, "comment": "Default argument", "code": "def power(base, exp=2):\n    return base ** exp\n\nprint(power(5))       # 25\nprint(power(5, 3))    # 125"},
                {"step": 3, "comment": "Scope in action", "code": "x = 10\ndef show():\n    x = 99            # new local x\n    print('inside:', x)\nshow()\nprint('outside:', x)  # still 10"},
            ],
            [
                "Forgetting `return` — the caller gets None.",
                "Shadowing built-ins like `list`, `sum`, `id` as parameter names.",
            ],
            [
                {
                    "question": "`def f(x): x + 1` — what does `f(5)` return?",
                    "options": ["6", "5", "None", "Error"],
                    "correct": "None",
                    "explanation": "No return statement means the function returns None.",
                }
            ],
            xp=10, mins=10,
        ),
        _lesson(
            "10 · Error handling basics",
            "Every program you write will eventually meet a user who types `abc` when asked for a number. Without protection, your program crashes. With `try/except`, it apologises politely and continues.",
            "`try` attempts something risky; `except` catches the specific failure you expected.",
            "Wrap risky code in `try:`. Catch specific exceptions with `except ErrorType:`. Add `else:` for the 'no error' path and `finally:` for cleanup that runs either way. Never catch bare `except:` — it hides real bugs.",
            [
                {"step": 1, "comment": "Handle bad input", "code": "try:\n    n = int(input('Number? '))\n    print('Square:', n * n)\nexcept ValueError:\n    print('That was not a number.')"},
                {"step": 2, "comment": "Multiple excepts", "code": "try:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('No dividing by zero!')\nexcept TypeError:\n    print('Wrong type.')"},
            ],
            [
                "Bare `except:` swallows every error, including KeyboardInterrupt.",
                "Catching `Exception` as the first line of defence — be as specific as you can.",
            ],
            [
                {
                    "question": "Which runs even if an exception happens?",
                    "options": ["try", "except", "else", "finally"],
                    "correct": "finally",
                    "explanation": "`finally` always runs — that's its whole job.",
                }
            ],
            xp=10, mins=9,
        ),
    ],

    # =========================================================================
    # STAGE 2 — Core Fundamentals
    # =========================================================================
    "python-stage-2-core": [
        _lesson(
            "11 · List comprehensions",
            "You want the squares of numbers 1 to 10. Option A: four lines with a for loop. Option B: one line that reads almost like English. Python prefers Option B.",
            "A comprehension is a for-loop collapsed into an expression.",
            "Syntax: `[expr for item in iterable if condition]`. You can use them for lists `[]`, sets `{}`, dicts `{k:v for ...}`, and generators `(...)`. Rule of thumb: if the loop would have nested 3+ levels, fall back to a regular for.",
            [
                {"step": 1, "comment": "Squares", "code": "squares = [x * x for x in range(1, 11)]\nprint(squares)"},
                {"step": 2, "comment": "With a filter", "code": "evens = [x for x in range(20) if x % 2 == 0]"},
                {"step": 3, "comment": "Dict comprehension", "code": "words = ['apple', 'kiwi']\nlens = {w: len(w) for w in words}"},
            ],
            [
                "Abusing comprehensions for side effects (printing inside).",
                "Hard-to-read triple-nested comprehensions — when it hurts to read, go back to for.",
            ],
            [
                {
                    "question": "What does `[x*2 for x in [1,2,3]]` give?",
                    "options": ["[2,4,6]", "[1,2,3,1,2,3]", "[1,4,9]", "Error"],
                    "correct": "[2,4,6]",
                    "explanation": "Each element is doubled.",
                }
            ],
            xp=15, mins=8,
        ),
        _lesson(
            "12 · File I/O",
            "Your program forgets everything the moment it ends — unless you write to a file. Files are how programs remember.",
            "`with open(...) as f:` auto-closes the file, even if your code explodes halfway.",
            "`open(path, mode)` returns a file object. Modes: `'r'` read, `'w'` write (truncates!), `'a'` append, add `'b'` for binary. Use `with` so the file closes cleanly. `f.read()`, `f.readlines()`, `f.write()`, or iterate line by line.",
            [
                {"step": 1, "comment": "Write and read", "code": "with open('notes.txt', 'w') as f:\n    f.write('Hello, file!\\n')\n\nwith open('notes.txt') as f:\n    print(f.read())"},
                {"step": 2, "comment": "Line by line (memory-friendly)", "code": "with open('notes.txt') as f:\n    for line in f:\n        print(line.strip())"},
            ],
            [
                "Opening `'w'` when you meant `'a'` — `'w'` truncates the file!",
                "Forgetting to close the file — always prefer `with`.",
            ],
            [
                {
                    "question": "Which mode erases the file before writing?",
                    "options": ["'r'", "'w'", "'a'", "'x'"],
                    "correct": "'w'",
                    "explanation": "'w' truncates. Use 'a' to append without deleting.",
                }
            ],
            xp=15, mins=9,
        ),
        _lesson(
            "13 · Modules & imports",
            "A module is a `.py` file you can borrow from. Instead of rewriting math functions, you write `import math` and use `math.sqrt(16)`. Python ships with hundreds of modules already installed.",
            "Every `.py` file is a module. Importing it runs its top-level code once and gives you its names.",
            "Three import styles: `import math`, `from math import sqrt`, `from math import sqrt as s`. Avoid `from math import *` — it pollutes your namespace. Your own files become modules the moment they sit next to each other.",
            [
                {"step": 1, "comment": "Standard library", "code": "import math\nprint(math.pi)\nprint(math.sqrt(16))"},
                {"step": 2, "comment": "Aliased import", "code": "import datetime as dt\nprint(dt.date.today())"},
                {"step": 3, "comment": "Your own module", "code": "# mymath.py\ndef double(x): return x * 2\n\n# main.py\nfrom mymath import double\nprint(double(21))"},
            ],
            [
                "Circular imports — two files importing each other.",
                "Running scripts from the wrong directory and getting ModuleNotFoundError.",
            ],
            [
                {
                    "question": "What does `from math import *` do that people dislike?",
                    "options": ["Imports only one name", "Pollutes your namespace", "Imports nothing", "Errors"],
                    "correct": "Pollutes your namespace",
                    "explanation": "It imports every public name, risking collisions.",
                }
            ],
            xp=15, mins=9,
        ),
        _lesson(
            "14 · Exception handling (deeper)",
            "Basic try/except handles one mistake at a time. Real programs need to talk about errors: log them, raise custom ones, chain them together.",
            "Exceptions are just objects. You can create your own by subclassing `Exception`.",
            "Use `raise` to throw, `raise ... from e` to chain, and `class MyError(Exception): pass` to create custom types. A common pattern: validate inputs at the top of a function and raise early with a clear message.",
            [
                {"step": 1, "comment": "Custom exception", "code": "class InvalidAge(Exception):\n    pass\n\ndef set_age(a):\n    if a < 0:\n        raise InvalidAge(f'Age cannot be {a}')\n    return a"},
                {"step": 2, "comment": "Catching it", "code": "try:\n    set_age(-1)\nexcept InvalidAge as e:\n    print('Oops:', e)"},
            ],
            [
                "Raising `Exception('...')` instead of a descriptive subclass.",
                "Silently swallowing errors with `except: pass`.",
            ],
            [
                {
                    "question": "How do you create a custom exception?",
                    "options": ["def MyError", "class MyError(Exception): pass", "raise 'MyError'", "error = new()"],
                    "correct": "class MyError(Exception): pass",
                    "explanation": "Subclass Exception (or a more specific type).",
                }
            ],
            xp=15, mins=9,
        ),
        _lesson(
            "15 · Lambda functions",
            "Sometimes you need a tiny, throwaway function that only lives for one line. Writing `def` for that feels ceremonial. Lambdas are the shortcut.",
            "`lambda args: expr` is an anonymous one-line function. Pass it where a function is expected.",
            "Lambdas are perfect for `sorted(key=...)`, `map`, `filter`, and tiny callbacks. They're limited to a single expression — if you need a statement or multiple lines, use `def`.",
            [
                {"step": 1, "comment": "Basic lambda", "code": "square = lambda x: x * x\nprint(square(7))"},
                {"step": 2, "comment": "With sorted", "code": "words = ['kiwi', 'apple', 'banana']\nwords.sort(key=lambda w: len(w))\nprint(words)  # shortest first"},
            ],
            [
                "Assigning lambdas to names — at that point just use `def`.",
                "Trying to put multiple statements in a lambda (impossible).",
            ],
            [
                {
                    "question": "Which is valid inside a lambda?",
                    "options": ["a print statement", "an if/elif ladder", "a single expression", "a for loop"],
                    "correct": "a single expression",
                    "explanation": "Lambdas are restricted to one expression.",
                }
            ],
            xp=15, mins=7,
        ),
        _lesson(
            "16 · map, filter, zip",
            "You have a list of prices in dollars. You want them in rupees. You could write a for loop — or you could say 'map every price through this function'.",
            "`map` transforms, `filter` keeps only the ones you want, `zip` stitches two lists into one.",
            "`map(f, iter)` applies `f` to each element. `filter(pred, iter)` keeps elements where `pred` is True. `zip(a, b)` pairs them position-by-position. All three return iterators — wrap with `list()` to materialize.",
            [
                {"step": 1, "comment": "map", "code": "prices = [10, 20, 30]\nrupees = list(map(lambda d: d * 83, prices))\nprint(rupees)"},
                {"step": 2, "comment": "filter", "code": "ages = [12, 18, 25, 7]\nadults = list(filter(lambda a: a >= 18, ages))"},
                {"step": 3, "comment": "zip", "code": "names = ['A', 'B', 'C']\nmarks = [80, 95, 70]\nfor n, m in zip(names, marks):\n    print(n, m)"},
            ],
            [
                "Forgetting `list()` and printing a `<map object>` instead of contents.",
                "`zip` stops at the shortest iterable — losing data silently.",
            ],
            [
                {
                    "question": "What does `list(zip([1,2,3], ['a','b']))` produce?",
                    "options": ["[(1,'a'),(2,'b')]", "[(1,'a'),(2,'b'),(3,None)]", "Error", "[1,2,3,'a','b']"],
                    "correct": "[(1,'a'),(2,'b')]",
                    "explanation": "zip stops at the shortest iterable.",
                }
            ],
            xp=15, mins=8,
        ),
        _lesson(
            "17 · *args & **kwargs",
            "Some functions need to accept 'any number of things'. `print` accepts 1 or 20 arguments. How? It uses *args under the hood.",
            "`*args` catches extra positional arguments as a tuple. `**kwargs` catches extra keyword arguments as a dict.",
            "Use `*args` when the caller might pass 0, 1, or many positional items. Use `**kwargs` for flexible keyword arguments — great for wrappers and decorators. You can also unpack with `*` and `**` at the call site.",
            [
                {"step": 1, "comment": "Variable positional args", "code": "def total(*nums):\n    return sum(nums)\n\nprint(total(1, 2, 3, 4))   # 10"},
                {"step": 2, "comment": "Variable keyword args", "code": "def profile(**info):\n    for k, v in info.items():\n        print(f'{k}: {v}')\n\nprofile(name='A', age=20)"},
                {"step": 3, "comment": "Unpacking at call site", "code": "args = (1, 2, 3)\nkwargs = {'sep': '-'}\nprint(*args, **kwargs)     # 1-2-3"},
            ],
            [
                "Mixing the order — must be `def f(pos, *args, kw, **kwargs)`.",
                "Using `**kwargs` as a data blob when a real dict argument would be cleaner.",
            ],
            [
                {
                    "question": "Inside `def f(*args)`, what type is `args`?",
                    "options": ["list", "dict", "tuple", "set"],
                    "correct": "tuple",
                    "explanation": "`*args` collects positional arguments into a tuple.",
                }
            ],
            xp=15, mins=9,
        ),
        _lesson(
            "18 · Virtual environments",
            "Two projects on your laptop. Project A needs Django 3. Project B needs Django 5. If you install globally, they fight. Virtual environments give each project its own sandbox.",
            "A venv is just a folder with its own Python interpreter and its own packages, isolated from the system.",
            "`python -m venv .venv` creates one. Activate with `.venv/Scripts/activate` (Windows) or `source .venv/bin/activate` (Linux/Mac). While activated, `pip install` and `python` use the venv's copies. `deactivate` returns to normal.",
            [
                {"step": 1, "comment": "Create and activate (terminal)", "code": "# Run in your terminal:\npython -m venv .venv\n# Windows\n.venv\\Scripts\\activate\n# Mac/Linux\nsource .venv/bin/activate"},
                {"step": 2, "comment": "Freeze and reproduce", "code": "pip freeze > requirements.txt\n# later, on another machine:\npip install -r requirements.txt"},
            ],
            [
                "Committing the `.venv/` folder to git — always add it to `.gitignore`.",
                "Forgetting to activate before installing — packages land globally.",
            ],
            [
                {
                    "question": "Why use venv?",
                    "options": ["Faster Python", "Per-project isolated dependencies", "Security", "Encryption"],
                    "correct": "Per-project isolated dependencies",
                    "explanation": "Each project gets its own package versions.",
                }
            ],
            xp=15, mins=7,
        ),
        _lesson(
            "19 · pip & packages",
            "You don't have to build the wheel every time. Someone already wrote a library for weather, for PDFs, for plotting charts — and `pip` is the delivery truck.",
            "`pip install name` downloads from PyPI and wires it into your current Python (or venv).",
            "`pip install X`, `pip uninstall X`, `pip list`, `pip show X`. Pin exact versions in `requirements.txt`. Prefer `pip install -r requirements.txt` so teammates reproduce your environment.",
            [
                {"step": 1, "comment": "Install and use", "code": "# terminal\npip install requests\n\n# code\nimport requests\nr = requests.get('https://api.github.com')\nprint(r.status_code)"},
                {"step": 2, "comment": "Pin versions", "code": "# requirements.txt\nrequests==2.31.0\nrich>=13"},
            ],
            [
                "Installing globally instead of inside a venv.",
                "Using `pip install` without pinning — reproducibility dies.",
            ],
            [
                {
                    "question": "Where does pip download packages from by default?",
                    "options": ["GitHub", "PyPI", "npm", "Maven"],
                    "correct": "PyPI",
                    "explanation": "The Python Package Index (pypi.org).",
                }
            ],
            xp=15, mins=7,
        ),
        _lesson(
            "20 · Regular expressions",
            "You have 10,000 lines of text and you want every phone number. You could write a parser — or write a pattern that says 'three digits, a dash, four digits' and let regex find them all.",
            "Regex is a mini-language for describing patterns in text.",
            "Use the `re` module. Key tools: `re.search(pattern, text)`, `re.findall`, `re.sub`. Patterns: `\\d` digit, `\\w` word char, `.` any char, `+` one or more, `*` zero or more, `()` capture group, `^ $` anchors.",
            [
                {"step": 1, "comment": "Find all phone numbers", "code": "import re\ntext = 'call 9876543210 or 123-456-7890'\nfound = re.findall(r'\\d{3}[- ]?\\d{3}[- ]?\\d{4}', text)\nprint(found)"},
                {"step": 2, "comment": "Replace", "code": "clean = re.sub(r'\\s+', ' ', 'too   much    space')\nprint(clean)"},
            ],
            [
                "Using regex to parse HTML — please don't. Use a parser like BeautifulSoup.",
                "Forgetting to use raw strings `r'...'` — backslashes get eaten otherwise.",
            ],
            [
                {
                    "question": "What does `\\d+` match?",
                    "options": ["one letter", "any character", "one or more digits", "whitespace"],
                    "correct": "one or more digits",
                    "explanation": "\\d = digit, + = one or more.",
                }
            ],
            xp=15, mins=10,
        ),
    ],

    # =========================================================================
    # STAGE 3 — Object-Oriented Python
    # =========================================================================
    "python-stage-3-oop": [
        _lesson(
            "21 · Classes & objects",
            "Imagine you're building a game with dozens of dogs. Each dog has a name, an age, and the ability to bark. Copy-pasting the same three variables for every dog is madness. You want a blueprint — a class — and to stamp out dogs from it.",
            "A class is the blueprint. An object is an instance — a real thing built from the blueprint.",
            "Define with `class Name:`. Attributes live on instances. Methods are functions inside the class whose first argument is always `self` (the current instance).",
            [
                {"step": 1, "comment": "Blueprint", "code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        print(f'{self.name} says woof!')"},
                {"step": 2, "comment": "Stamp out instances", "code": "d1 = Dog('Bruno')\nd2 = Dog('Luna')\nd1.bark()\nd2.bark()"},
            ],
            [
                "Forgetting `self` on the first parameter.",
                "Defining attributes outside `__init__` and reusing them across instances by accident.",
            ],
            [
                {
                    "question": "What is `self` in a method?",
                    "options": ["The class itself", "The current instance", "A keyword", "A module"],
                    "correct": "The current instance",
                    "explanation": "`self` is the object the method was called on.",
                }
            ],
            xp=20, mins=9,
        ),
        _lesson(
            "22 · __init__ & self",
            "When you write `Dog('Bruno')`, Python does two invisible things: it creates a new empty object, then it hands that object to `__init__` as `self` and lets you set it up.",
            "`__init__` isn't the constructor — it's the *initializer*. Python constructs the object first, then calls `__init__` to fill it in.",
            "`__init__(self, ...)` runs automatically on creation. Use it to set up every attribute the object needs. Default values are OK. Never `return` from `__init__` — it must return None.",
            [
                {"step": 1, "comment": "Initializer with defaults", "code": "class Book:\n    def __init__(self, title, author='Unknown'):\n        self.title = title\n        self.author = author"},
                {"step": 2, "comment": "Create two ways", "code": "b1 = Book('1984', 'Orwell')\nb2 = Book('Untitled')\nprint(b2.author)  # Unknown"},
            ],
            [
                "Putting a `return` value in `__init__` — it's ignored and confusing.",
                "Mutable default arguments (`def __init__(self, items=[])`) — everyone shares the same list!",
            ],
            [
                {
                    "question": "When does `__init__` run?",
                    "options": ["Manually", "Before every method", "Once at object creation", "Never"],
                    "correct": "Once at object creation",
                    "explanation": "Python calls it automatically when you construct the object.",
                }
            ],
            xp=20, mins=8,
        ),
        _lesson(
            "23 · Inheritance",
            "You have a `Dog` class and a `Cat` class. Both eat, sleep, and have a name. Instead of duplicating those three into each, create an `Animal` parent and have Dog and Cat inherit from it.",
            "Inheritance lets a child class reuse everything from its parent and add or override as needed.",
            "`class Child(Parent):`. Inside methods, call the parent with `super().method(...)`. Children override by defining a method with the same name. Multiple inheritance exists but use it sparingly.",
            [
                {"step": 1, "comment": "Parent", "code": "class Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        print(f'{self.name} makes a sound')"},
                {"step": 2, "comment": "Child overrides + extends", "code": "class Dog(Animal):\n    def speak(self):\n        print(f'{self.name} says woof!')"},
                {"step": 3, "comment": "Super call", "code": "class Puppy(Dog):\n    def __init__(self, name, age):\n        super().__init__(name)\n        self.age = age"},
            ],
            [
                "Forgetting to call `super().__init__()` in the child — parent setup never runs.",
                "Deep inheritance trees — usually composition is clearer.",
            ],
            [
                {
                    "question": "What does `super().__init__(name)` do?",
                    "options": ["Calls the child init", "Calls the parent init", "Creates a new object", "Nothing"],
                    "correct": "Calls the parent init",
                    "explanation": "super() refers to the parent class.",
                }
            ],
            xp=20, mins=10,
        ),
        _lesson(
            "24 · Polymorphism",
            "You have a list of shapes: circles, squares, triangles. You want to compute the area of each. You'd hate to `if isinstance(s, Circle)` everywhere. Instead, every shape has an `area()` method and you just call it.",
            "Polymorphism means 'same interface, different behaviour'. Python trusts that if it has the method, it works.",
            "Python's polymorphism is duck-typed: 'if it walks like a duck'. You don't need a common parent class — just a common method name. Overriding a parent method is one way to achieve it.",
            [
                {"step": 1, "comment": "Shapes", "code": "class Circle:\n    def __init__(self, r): self.r = r\n    def area(self): return 3.14 * self.r ** 2\n\nclass Square:\n    def __init__(self, s): self.s = s\n    def area(self): return self.s * self.s"},
                {"step": 2, "comment": "Uniform treatment", "code": "shapes = [Circle(5), Square(4)]\nfor s in shapes:\n    print(s.area())"},
            ],
            [
                "Adding isinstance checks instead of relying on duck typing.",
                "Forgetting to implement the method on one of the subtypes — AttributeError at runtime.",
            ],
            [
                {
                    "question": "In Python, polymorphism needs a common...",
                    "options": ["parent class", "method name", "module", "interface keyword"],
                    "correct": "method name",
                    "explanation": "Duck typing: the method name is the contract.",
                }
            ],
            xp=20, mins=9,
        ),
        _lesson(
            "25 · Encapsulation",
            "You've built a bank account class. Any outside code can set `account.balance = -99999`. That's a disaster waiting to happen. You want to say 'balance is private; use the deposit method'.",
            "Python uses naming conventions, not strict keywords: `_name` means 'please don't touch', `__name` triggers name mangling.",
            "`_private` is a hint to callers. `__name` (double underscore) mangles to `_ClassName__name`, making accidental access harder. Expose controlled methods for reading/writing — see properties next lesson.",
            [
                {"step": 1, "comment": "Private by convention", "code": "class Account:\n    def __init__(self):\n        self._balance = 0\n    def deposit(self, amt):\n        if amt < 0: raise ValueError('negative')\n        self._balance += amt"},
            ],
            [
                "Assuming `_var` gives real privacy — it doesn't, it's a promise.",
                "Using `__var` just for style — only use it when you actually need mangling.",
            ],
            [
                {
                    "question": "What does `_name` mean by convention?",
                    "options": ["Public", "Private (hint)", "Deleted", "Protected by keyword"],
                    "correct": "Private (hint)",
                    "explanation": "It's a gentleman's agreement — Python won't stop you.",
                }
            ],
            xp=20, mins=8,
        ),
        _lesson(
            "26 · Dunder methods",
            "You want `print(my_point)` to show `Point(3,4)` and `p1 + p2` to add two points. Python has hooks for every operator — they're called 'dunder' (double-underscore) methods.",
            "Dunders are how your class plugs into Python's built-in operators and functions.",
            "Common ones: `__init__` (init), `__repr__` (developer string), `__str__` (friendly string), `__eq__` (==), `__lt__` (<), `__add__` (+), `__len__` (len()), `__iter__` (for loops).",
            [
                {"step": 1, "comment": "String and add", "code": "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __repr__(self):\n        return f'Point({self.x},{self.y})'\n    def __add__(self, other):\n        return Point(self.x + other.x, self.y + other.y)\n\np = Point(1,2) + Point(3,4)\nprint(p)  # Point(4,6)"},
            ],
            [
                "Defining `__str__` but forgetting `__repr__` — debugging gets painful.",
                "Implementing `__eq__` without `__hash__` when you need set/dict support.",
            ],
            [
                {
                    "question": "Which dunder makes `len(obj)` work?",
                    "options": ["__size__", "__len__", "__count__", "__length__"],
                    "correct": "__len__",
                    "explanation": "`len()` calls `obj.__len__()`.",
                }
            ],
            xp=20, mins=10,
        ),
        _lesson(
            "27 · Decorators",
            "You wrote ten functions and now you want every one of them to print how long it took to run. Adding timer code to each is tedious. A decorator wraps the function invisibly and adds the behaviour.",
            "A decorator is a function that takes a function and returns a new function.",
            "`@my_decorator` above a `def` is shorthand for `func = my_decorator(func)`. Decorators can add logging, timing, auth checks, caching — anything you want to wrap around existing logic.",
            [
                {"step": 1, "comment": "Build a timer", "code": "import time\ndef timer(fn):\n    def wrap(*a, **kw):\n        t = time.time()\n        r = fn(*a, **kw)\n        print(f'{fn.__name__} took {time.time()-t:.3f}s')\n        return r\n    return wrap"},
                {"step": 2, "comment": "Apply it", "code": "@timer\ndef slow():\n    time.sleep(0.2)\n\nslow()"},
            ],
            [
                "Forgetting `*args, **kwargs` in the wrapper — breaks functions with arguments.",
                "Losing the original function's name — use `functools.wraps` to preserve metadata.",
            ],
            [
                {
                    "question": "`@deco` above `def f` is the same as what?",
                    "options": ["f = deco", "f = deco(f)", "deco(f)", "deco.f"],
                    "correct": "f = deco(f)",
                    "explanation": "It's syntactic sugar for reassigning the name.",
                }
            ],
            xp=20, mins=10,
        ),
        _lesson(
            "28 · Properties",
            "You want `account.balance` to look like a plain attribute but actually run validation whenever someone sets it. Properties let you have methods that pretend to be attributes.",
            "`@property` turns a method into a read-only attribute. `@name.setter` lets you hook writes.",
            "Define the getter with `@property`, optionally add a `@x.setter` for writes. Callers just say `obj.x` and `obj.x = 5`, but your code controls what actually happens.",
            [
                {"step": 1, "comment": "Validated setter", "code": "class Account:\n    def __init__(self):\n        self._balance = 0\n    @property\n    def balance(self):\n        return self._balance\n    @balance.setter\n    def balance(self, value):\n        if value < 0: raise ValueError\n        self._balance = value"},
                {"step": 2, "comment": "Use as attribute", "code": "a = Account()\na.balance = 500\nprint(a.balance)"},
            ],
            [
                "Storing the public and private names as the same attribute (infinite recursion).",
                "Using properties when a simple attribute would do.",
            ],
            [
                {
                    "question": "What decorator makes a method act like an attribute?",
                    "options": ["@attr", "@property", "@field", "@getter"],
                    "correct": "@property",
                    "explanation": "It's the built-in for this.",
                }
            ],
            xp=20, mins=9,
        ),
        _lesson(
            "29 · Abstract classes",
            "You want to enforce that every subclass of `Shape` must implement `area()`. Without enforcement, a lazy subclass might forget — and you'd only find out at runtime.",
            "Abstract base classes (ABCs) let you define 'you must implement this' contracts that fail loudly at construction time.",
            "Inherit from `ABC` and mark methods with `@abstractmethod`. You can't instantiate a class with unimplemented abstract methods — Python raises TypeError immediately.",
            [
                {"step": 1, "comment": "Abstract base", "code": "from abc import ABC, abstractmethod\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        ...\n\nclass Square(Shape):\n    def __init__(self, s): self.s = s\n    def area(self): return self.s * self.s"},
                {"step": 2, "comment": "Attempt without area", "code": "class BadShape(Shape):\n    pass\n# BadShape()  → TypeError at construction"},
            ],
            [
                "Forgetting to import from `abc`.",
                "Treating abstract classes as interfaces alone — they can still have concrete helper methods.",
            ],
            [
                {
                    "question": "What happens if you instantiate a class with an unimplemented abstract method?",
                    "options": ["Nothing", "TypeError", "RuntimeError", "It works"],
                    "correct": "TypeError",
                    "explanation": "Python refuses to construct it.",
                }
            ],
            xp=20, mins=9,
        ),
        _lesson(
            "30 · Data classes",
            "For every simple 'data container' class you wrote `__init__`, `__repr__`, and `__eq__` by hand. `@dataclass` writes them all for you from the type hints.",
            "One decorator, zero boilerplate, fully-working class.",
            "`@dataclass` reads the type-annotated class body and generates `__init__`, `__repr__`, and `__eq__`. Add `frozen=True` for immutability. Defaults and field factories use `field(default_factory=list)`.",
            [
                {"step": 1, "comment": "Plain data class", "code": "from dataclasses import dataclass\n\n@dataclass\nclass Point:\n    x: int\n    y: int\n\np = Point(3, 4)\nprint(p)            # Point(x=3, y=4)\nprint(p == Point(3, 4))  # True"},
                {"step": 2, "comment": "Frozen (immutable)", "code": "@dataclass(frozen=True)\nclass Color:\n    r: int\n    g: int\n    b: int"},
            ],
            [
                "Using mutable defaults directly (`items: list = []`) — must use `field(default_factory=list)`.",
                "Over-using for classes that have real behaviour beyond being data containers.",
            ],
            [
                {
                    "question": "What does @dataclass auto-generate?",
                    "options": ["__init__, __repr__, __eq__", "Only __init__", "Methods at random", "Nothing"],
                    "correct": "__init__, __repr__, __eq__",
                    "explanation": "Those three by default, plus others if you ask.",
                }
            ],
            xp=20, mins=8,
        ),
    ],

    # =========================================================================
    # STAGE 4 — Intermediate Python
    # =========================================================================
    "python-stage-4-intermediate": [
        _lesson(
            "31 · Generators & iterators",
            "You want to read a 10 GB log file line by line. Loading it all into a list would crash your laptop. Generators produce one value at a time, keeping memory tiny.",
            "`yield` turns a function into a generator: it pauses and resumes, producing values lazily.",
            "Use `yield` instead of `return`. Each call to `next(gen)` runs until the next `yield`. Generator expressions look like list comprehensions but with `()` — `sum(x*x for x in range(10**7))` is memory-efficient.",
            [
                {"step": 1, "comment": "Generator function", "code": "def counter(n):\n    i = 0\n    while i < n:\n        yield i\n        i += 1\n\nfor x in counter(5):\n    print(x)"},
                {"step": 2, "comment": "Generator expression", "code": "squares = (x*x for x in range(10))\nprint(sum(squares))"},
            ],
            [
                "Iterating a generator twice — it's consumed after the first pass.",
                "Using `return` where `yield` was intended — you'll get a plain function.",
            ],
            [
                {
                    "question": "What keyword makes a generator?",
                    "options": ["return", "yield", "gen", "produce"],
                    "correct": "yield",
                    "explanation": "`yield` pauses execution and returns a value.",
                }
            ],
            xp=25, mins=10,
        ),
        _lesson(
            "32 · Context managers",
            "Every resource (file, socket, DB connection) needs to be cleaned up. Forgetting is costly. `with` makes cleanup automatic, even if your code explodes inside the block.",
            "A context manager is an object with `__enter__` and `__exit__` — `with` calls them around your block.",
            "Most cleanup is done with `with open(...)`. Build your own with `contextlib.contextmanager`: a generator that yields once. Everything before yield is setup; everything after is teardown.",
            [
                {"step": 1, "comment": "Built-in", "code": "with open('data.txt') as f:\n    content = f.read()\n# file auto-closes here"},
                {"step": 2, "comment": "Custom context manager", "code": "from contextlib import contextmanager\n\n@contextmanager\ndef timer():\n    import time; start = time.time()\n    yield\n    print(f'{time.time()-start:.3f}s')\n\nwith timer():\n    sum(range(10**6))"},
            ],
            [
                "Manually calling `.close()` when you could use `with`.",
                "Skipping teardown after an exception — that's exactly what context managers prevent.",
            ],
            [
                {
                    "question": "Which method runs when a `with` block ends?",
                    "options": ["__exit__", "__close__", "__end__", "__del__"],
                    "correct": "__exit__",
                    "explanation": "`__exit__` is the teardown hook.",
                }
            ],
            xp=25, mins=9,
        ),
        _lesson(
            "33 · Threading & multiprocessing",
            "Downloading 100 files sequentially takes forever because 99% of the time you're waiting on the network. Threads let you wait on many files in parallel. For CPU-heavy work, you need processes instead.",
            "Threads share memory — great for I/O waits. Processes don't — use them when work is CPU-bound.",
            "Python's GIL limits true parallelism for CPU-bound threads, but I/O release the GIL so threading still helps there. Use `threading.Thread` for I/O and `multiprocessing.Process` or `concurrent.futures` for CPU.",
            [
                {"step": 1, "comment": "Simple thread pool", "code": "from concurrent.futures import ThreadPoolExecutor\nimport requests\n\nurls = ['https://example.com'] * 5\nwith ThreadPoolExecutor(max_workers=5) as ex:\n    results = list(ex.map(requests.get, urls))"},
                {"step": 2, "comment": "CPU work with a process pool", "code": "from concurrent.futures import ProcessPoolExecutor\n\ndef heavy(n):\n    return sum(i*i for i in range(n))\n\nwith ProcessPoolExecutor() as ex:\n    print(list(ex.map(heavy, [10**6]*4)))"},
            ],
            [
                "Using threads for CPU work and expecting a speedup (GIL!).",
                "Sharing unsynchronized state between threads — race conditions.",
            ],
            [
                {
                    "question": "For CPU-bound work, prefer...",
                    "options": ["threads", "processes", "generators", "asyncio"],
                    "correct": "processes",
                    "explanation": "Processes bypass the GIL and use multiple cores.",
                }
            ],
            xp=25, mins=11,
        ),
        _lesson(
            "34 · Async / await",
            "Threads are one way to handle many waits. Async is another — single-threaded, cooperative, and lighter. A web scraper that fetches 1000 URLs can fit in one process with async.",
            "`async def` functions return coroutines. `await` pauses the coroutine, letting the event loop run other tasks until the result is ready.",
            "Use `asyncio.run(main())` to bootstrap. `asyncio.gather(*coros)` runs many at once. Only `await` things that are async — plain `time.sleep` blocks the whole loop.",
            [
                {"step": 1, "comment": "Two awaits running concurrently", "code": "import asyncio\n\nasync def say(msg, delay):\n    await asyncio.sleep(delay)\n    print(msg)\n\nasync def main():\n    await asyncio.gather(say('hi', 1), say('bye', 1))\n\nasyncio.run(main())"},
            ],
            [
                "Calling blocking functions inside async code — freezes the loop.",
                "Forgetting `await` — you get a coroutine object instead of the result.",
            ],
            [
                {
                    "question": "What does `await` do?",
                    "options": ["Blocks the thread", "Pauses the coroutine", "Cancels it", "Starts a new thread"],
                    "correct": "Pauses the coroutine",
                    "explanation": "It yields control back to the event loop until the awaitable finishes.",
                }
            ],
            xp=25, mins=11,
        ),
        _lesson(
            "35 · Type hints",
            "You read old code and wonder: does this function take a list or a dict? Is it returning a string or None? Type hints answer at a glance.",
            "Hints don't change runtime behaviour, but they make code self-documenting and enable tools like mypy to catch bugs.",
            "Annotate parameters and returns with `name: type`. Use `list[int]`, `dict[str, Any]`, `Optional[X]` (= `X | None`), and `Callable[[int], int]`. Run `mypy` to typecheck.",
            [
                {"step": 1, "comment": "Hinted function", "code": "def average(nums: list[float]) -> float:\n    return sum(nums) / len(nums)"},
                {"step": 2, "comment": "Optional and union", "code": "def find_user(uid: int) -> str | None:\n    ...\n    return None"},
            ],
            [
                "Assuming hints enforce types at runtime — they don't.",
                "Hinting everything even trivial loop counters — becomes noise.",
            ],
            [
                {
                    "question": "Do type hints change how Python runs your code?",
                    "options": ["Yes, they enforce types", "No, they're ignored at runtime", "Only in tests", "Only in classes"],
                    "correct": "No, they're ignored at runtime",
                    "explanation": "They're metadata for tools like mypy and IDEs.",
                }
            ],
            xp=25, mins=9,
        ),
        _lesson(
            "36 · Unit testing with pytest",
            "You change one line and break three features elsewhere. You only find out when a user reports the bug. Tests are how you catch regressions before they ship.",
            "A test is a tiny program that calls your code with known inputs and asserts the outputs.",
            "pytest auto-discovers `test_*.py` files and `test_*` functions. Use plain `assert` statements — pytest rewrites them to give nice error messages. Fixtures handle setup/teardown.",
            [
                {"step": 1, "comment": "Function under test", "code": "# mathx.py\ndef add(a, b):\n    return a + b"},
                {"step": 2, "comment": "Test file", "code": "# test_mathx.py\nfrom mathx import add\n\ndef test_add_positive():\n    assert add(2, 3) == 5\n\ndef test_add_zero():\n    assert add(0, 0) == 0"},
                {"step": 3, "comment": "Run it", "code": "# terminal\npytest -v"},
            ],
            [
                "Writing one giant test for everything — keep them small and focused.",
                "Testing implementation details instead of behaviour.",
            ],
            [
                {
                    "question": "How does pytest find tests?",
                    "options": ["By name prefix", "By decorator", "By class inheritance", "Manually"],
                    "correct": "By name prefix",
                    "explanation": "`test_*.py` files, `test_*` functions.",
                }
            ],
            xp=25, mins=10,
        ),
        _lesson(
            "37 · Debugging techniques",
            "Print statements work, but they're noisy. A real debugger lets you pause at any line, inspect variables, and step through code like a time machine.",
            "`breakpoint()` (Python 3.7+) drops you into the debugger wherever you write it.",
            "In the debugger: `n` next line, `s` step into, `c` continue, `p var` print, `l` list source, `q` quit. For bigger projects, use your IDE's debugger — same commands, better UI.",
            [
                {"step": 1, "comment": "Drop into pdb", "code": "def f(x):\n    y = x + 1\n    breakpoint()   # pauses here\n    return y * 2\n\nf(5)"},
                {"step": 2, "comment": "A few pdb commands", "code": "# (Pdb) p y    → prints y\n# (Pdb) n      → next line\n# (Pdb) c      → continue"},
            ],
            [
                "Sprinkling print() everywhere and forgetting to remove them.",
                "Debugging locally while the bug only happens in production — read the logs.",
            ],
            [
                {
                    "question": "Which built-in drops into the debugger?",
                    "options": ["debug()", "breakpoint()", "pause()", "pdb()"],
                    "correct": "breakpoint()",
                    "explanation": "Built into Python 3.7+.",
                }
            ],
            xp=25, mins=8,
        ),
        _lesson(
            "38 · Working with JSON & APIs",
            "Talking to the internet is 90% of real Python. A weather API, a currency API, a chat API — they all speak JSON over HTTP. Learn this once and half the world opens up.",
            "JSON is just a string format that maps cleanly to Python dicts and lists.",
            "Use `requests` to make HTTP calls. Use `r.json()` to parse the body. Use `json.dumps` / `json.loads` for file/string conversion. Always check `r.status_code` and wrap calls in try/except.",
            [
                {"step": 1, "comment": "GET a JSON API", "code": "import requests\nr = requests.get('https://api.github.com/users/python')\nr.raise_for_status()\ndata = r.json()\nprint(data['name'], data['public_repos'])"},
                {"step": 2, "comment": "POST JSON", "code": "payload = {'name': 'Arjun', 'age': 20}\nr = requests.post('https://example.com/api', json=payload)\nprint(r.status_code)"},
            ],
            [
                "Parsing JSON with `eval()` — never do that, use `json.loads`.",
                "Ignoring HTTP error codes and blindly trusting `r.json()`.",
            ],
            [
                {
                    "question": "Which method parses the response body as JSON?",
                    "options": ["r.parse()", "r.json()", "r.body", "r.text()"],
                    "correct": "r.json()",
                    "explanation": "`requests` adds `.json()` as a shortcut.",
                }
            ],
            xp=25, mins=10,
        ),
        _lesson(
            "39 · Web scraping (BeautifulSoup)",
            "Not every site has an API. Sometimes you need to grab the HTML and extract the data yourself. BeautifulSoup turns a page of tag soup into a walkable tree.",
            "Treat HTML as a tree of tags. Query it with CSS selectors or find methods.",
            "Fetch with `requests`, parse with `BeautifulSoup(html, 'html.parser')`. Use `soup.find`, `soup.find_all`, `soup.select` (CSS). Always respect robots.txt and rate limits.",
            [
                {"step": 1, "comment": "Scrape headlines", "code": "import requests\nfrom bs4 import BeautifulSoup\n\nhtml = requests.get('https://example.com').text\nsoup = BeautifulSoup(html, 'html.parser')\nfor h in soup.select('h2'):\n    print(h.get_text(strip=True))"},
            ],
            [
                "Hammering a site with a tight loop — add `time.sleep` and be polite.",
                "Scraping behind a login without permission — it's probably against TOS.",
            ],
            [
                {
                    "question": "Which function extracts text from a BS4 tag?",
                    "options": [".text()", ".get_text()", ".string_of()", ".value()"],
                    "correct": ".get_text()",
                    "explanation": "It strips child tags and returns plain text.",
                }
            ],
            xp=25, mins=10,
        ),
        _lesson(
            "40 · Database with SQLite",
            "Storing data in JSON files is fine until you want to query, index, or update from two places at once. SQLite is a tiny SQL database that lives in one file — zero setup.",
            "Python ships with `sqlite3`. No server, no config — just a `.db` file.",
            "Open a connection, create a cursor, execute SQL with `?` placeholders (never format strings — SQL injection!), commit, close. Or use a `with` block to auto-commit.",
            [
                {"step": 1, "comment": "Create table and insert", "code": "import sqlite3\nwith sqlite3.connect('expenses.db') as con:\n    con.execute('CREATE TABLE IF NOT EXISTS items(name TEXT, amount REAL)')\n    con.execute('INSERT INTO items VALUES (?, ?)', ('chai', 20))"},
                {"step": 2, "comment": "Query", "code": "with sqlite3.connect('expenses.db') as con:\n    for row in con.execute('SELECT * FROM items WHERE amount > ?', (10,)):\n        print(row)"},
            ],
            [
                "Building SQL with f-strings — opens you to SQL injection.",
                "Forgetting to commit (in manual mode) — your writes vanish.",
            ],
            [
                {
                    "question": "Why use `?` placeholders?",
                    "options": ["Readability", "Speed", "SQL injection safety", "Standard convention"],
                    "correct": "SQL injection safety",
                    "explanation": "The driver escapes values safely.",
                }
            ],
            xp=25, mins=10,
        ),
    ],

    # =========================================================================
    # STAGE 5 — Web Specialization
    # =========================================================================
    "python-stage-5-web": [
        _lesson(
            "41 · Flask — your first web app",
            "A 'web server' sounds intimidating, but it's just a program that listens on a port and answers HTTP requests. Flask makes it a few lines of Python.",
            "A route is a URL pattern mapped to a Python function. The return value becomes the HTTP response.",
            "Install `flask`, create `app = Flask(__name__)`, decorate functions with `@app.route('/path')`, run with `app.run()`. Return strings, dicts (auto-JSON), or `render_template` for HTML pages.",
            [
                {"step": 1, "comment": "Minimal Flask app", "code": "from flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello, Web!'\n\n@app.route('/hi/<name>')\ndef hi(name):\n    return f'Hello, {name}!'\n\nif __name__ == '__main__':\n    app.run(debug=True)"},
            ],
            [
                "Running production with `debug=True` — major security hole.",
                "Storing state in module globals — breaks when you add workers.",
            ],
            [
                {
                    "question": "What does `@app.route('/')` do?",
                    "options": ["Runs on start", "Maps a URL to a function", "Defines a class", "Imports Flask"],
                    "correct": "Maps a URL to a function",
                    "explanation": "It registers the function as a handler for that path.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "42 · Django — the batteries-included framework",
            "Flask hands you bricks. Django hands you a pre-assembled house: ORM, admin panel, auth, forms, templates — all wired up.",
            "Django prefers convention over configuration. The cost is a steeper start; the reward is fewer decisions later.",
            "`django-admin startproject mysite` → `python manage.py startapp blog`. Models in `models.py`, views in `views.py`, URLs in `urls.py`. The ORM turns Python classes into SQL tables automatically.",
            [
                {"step": 1, "comment": "A model", "code": "# blog/models.py\nfrom django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    body = models.TextField()\n    created = models.DateTimeField(auto_now_add=True)"},
                {"step": 2, "comment": "A view", "code": "# blog/views.py\nfrom django.shortcuts import render\nfrom .models import Post\n\ndef index(request):\n    return render(request, 'blog/index.html', {'posts': Post.objects.all()})"},
            ],
            [
                "Skipping migrations after changing models — the DB and code drift.",
                "Fighting Django conventions instead of learning them.",
            ],
            [
                {
                    "question": "What command creates a new Django app inside a project?",
                    "options": ["django new", "manage.py startapp name", "django-admin app", "pip new app"],
                    "correct": "manage.py startapp name",
                    "explanation": "That's the canonical command.",
                }
            ],
            xp=30, mins=11,
        ),
        _lesson(
            "43 · REST APIs",
            "A REST API is how backends and frontends talk. You agree on URLs and methods: GET to read, POST to create, PUT to update, DELETE to remove. Requests carry JSON; responses carry JSON.",
            "Design resources (nouns), not actions (verbs). `/users/42` GET gets user 42. `/users/42` DELETE deletes it. Simple and predictable.",
            "Build JSON endpoints in Flask (`jsonify`) or Django REST Framework. Return clear status codes: 200 OK, 201 Created, 400 Bad Request, 404 Not Found. Version your API: `/api/v1/...`.",
            [
                {"step": 1, "comment": "Flask JSON API", "code": "from flask import Flask, jsonify, request\napp = Flask(__name__)\nnotes = []\n\n@app.post('/api/notes')\ndef create():\n    data = request.get_json()\n    notes.append(data)\n    return jsonify(data), 201\n\n@app.get('/api/notes')\ndef listall():\n    return jsonify(notes)"},
            ],
            [
                "Mixing verbs into URLs (`/getUsers`) — use HTTP methods instead.",
                "Returning 200 for errors — use the proper 4xx/5xx code.",
            ],
            [
                {
                    "question": "Which HTTP method creates a new resource?",
                    "options": ["GET", "POST", "PUT", "DELETE"],
                    "correct": "POST",
                    "explanation": "POST is the convention for creation.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "44 · HTML templating",
            "Returning HTML strings from Python is painful. Templates let you write HTML files with tiny Python-like holes for dynamic content.",
            "Templates separate structure (HTML) from data (Python). The engine fills the holes.",
            "Flask uses Jinja2 by default: `{{ var }}` for output, `{% for %}` / `{% if %}` for logic. Create a `templates/` folder next to your app and call `render_template('page.html', ...)`.",
            [
                {"step": 1, "comment": "templates/index.html", "code": "<h1>Hello {{ name }}</h1>\n<ul>\n{% for item in items %}\n  <li>{{ item }}</li>\n{% endfor %}\n</ul>"},
                {"step": 2, "comment": "Python side", "code": "from flask import render_template\n@app.route('/')\ndef home():\n    return render_template('index.html', name='Arjun', items=['a','b'])"},
            ],
            [
                "Building HTML by string concat — invites injection bugs.",
                "Putting real business logic inside templates.",
            ],
            [
                {
                    "question": "What does `{{ x }}` do in Jinja2?",
                    "options": ["Comments", "Outputs x", "Imports x", "Loops over x"],
                    "correct": "Outputs x",
                    "explanation": "Double braces render a value.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "45 · Authentication",
            "You need to know who's logged in. Passwords must be hashed, sessions must be stored, tokens must expire. Auth is where most small apps leak.",
            "Never store plain passwords. Hash with a slow algorithm (bcrypt/argon2). Use signed cookies or JWTs for sessions.",
            "Flask-Login and Django's built-in auth handle sessions for you. For APIs, issue JWTs after login; clients send them in the `Authorization: Bearer ...` header. Always HTTPS in production.",
            [
                {"step": 1, "comment": "Hashing a password", "code": "from werkzeug.security import generate_password_hash, check_password_hash\n\nhashed = generate_password_hash('my-secret')\nassert check_password_hash(hashed, 'my-secret')"},
            ],
            [
                "Storing plain passwords or using SHA-256 (too fast, brute-forceable).",
                "Rolling your own JWT library instead of using a well-tested one.",
            ],
            [
                {
                    "question": "Why use bcrypt or argon2 instead of SHA-256 for passwords?",
                    "options": ["They're newer", "They're intentionally slow", "They're shorter", "No reason"],
                    "correct": "They're intentionally slow",
                    "explanation": "Slow hashing makes brute force attacks infeasible.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "46 · Deploying to production",
            "Your app runs on your laptop. That's not useful. You need it on the internet, on a real server, with HTTPS, logs, and auto-restart on crash.",
            "In production, never use the dev server. Put gunicorn (or uvicorn for async) behind nginx, and keep it alive with systemd or docker.",
            "Platforms like Railway, Render, or Fly.io take your Dockerfile and give you a URL in minutes. For bare servers: nginx proxies to gunicorn, gunicorn runs your Flask/Django app.",
            [
                {"step": 1, "comment": "gunicorn command", "code": "# terminal\npip install gunicorn\ngunicorn app:app --workers 4 --bind 0.0.0.0:8000"},
                {"step": 2, "comment": "Minimal Dockerfile", "code": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"gunicorn\", \"app:app\", \"--bind\", \"0.0.0.0:8000\"]"},
            ],
            [
                "Shipping `debug=True` to prod.",
                "Not using environment variables for secrets — committing them to git.",
            ],
            [
                {
                    "question": "Which is a production-grade WSGI server?",
                    "options": ["flask run", "gunicorn", "python app.py", "node"],
                    "correct": "gunicorn",
                    "explanation": "It handles multiple workers, crashes, and load.",
                }
            ],
            xp=30, mins=11,
        ),
    ],

    # =========================================================================
    # STAGE 5 — Data Science Specialization
    # =========================================================================
    "python-stage-5-data": [
        _lesson(
            "47 · NumPy — arrays on steroids",
            "Python lists are flexible but slow. NumPy arrays are typed, contiguous, and hundreds of times faster for numeric work. Every data library builds on NumPy.",
            "A NumPy array is a fixed-type grid of numbers. Operations on it run in C, not Python.",
            "`import numpy as np`. Create with `np.array([...])`, `np.zeros`, `np.arange`. Element-wise math just works: `a * 2`, `a + b`. Reshape, slice, and broadcast across dimensions.",
            [
                {"step": 1, "comment": "Create and do math", "code": "import numpy as np\na = np.array([1, 2, 3, 4])\nprint(a * 2)          # [2 4 6 8]\nprint(a.mean())       # 2.5"},
                {"step": 2, "comment": "2D array", "code": "m = np.arange(12).reshape(3, 4)\nprint(m.shape)        # (3, 4)\nprint(m[:, 1])        # column 1"},
            ],
            [
                "Looping over numpy arrays with `for` — kills the speed. Use vectorized ops.",
                "Mixing Python lists and arrays in arithmetic — you usually want full arrays.",
            ],
            [
                {
                    "question": "Why are numpy arrays fast?",
                    "options": ["Written in C", "Parallel", "Compiled JIT", "Lazy eval"],
                    "correct": "Written in C",
                    "explanation": "The inner loops run in C, not Python.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "48 · Pandas — tables that think",
            "A spreadsheet is just rows and columns. Pandas is that, in Python, with superpowers: filter, group, join, pivot.",
            "A `DataFrame` is a labelled table. A `Series` is a single column.",
            "`pd.read_csv`, `df.head`, `df.info`, `df['col']`, `df[df.age > 18]`, `df.groupby('city').mean()`. Think of it as SQL you can script.",
            [
                {"step": 1, "comment": "Load a CSV", "code": "import pandas as pd\ndf = pd.read_csv('students.csv')\nprint(df.head())\nprint(df.describe())"},
                {"step": 2, "comment": "Filter and group", "code": "adults = df[df['age'] >= 18]\nby_city = df.groupby('city')['score'].mean()"},
            ],
            [
                "Chained indexing (`df[col][row] = value`) — use `.loc` instead.",
                "Treating a DataFrame like a list — use vectorized ops.",
            ],
            [
                {
                    "question": "What does `df.head()` do?",
                    "options": ["First rows", "Last rows", "Schema", "Summary stats"],
                    "correct": "First rows",
                    "explanation": "Default is the first 5 rows.",
                }
            ],
            xp=30, mins=11,
        ),
        _lesson(
            "49 · Matplotlib — the plotting workhorse",
            "You have data. Staring at numbers won't show you the story. A chart will.",
            "Matplotlib's API looks old, but it's in every data-science stack and it can draw anything.",
            "`import matplotlib.pyplot as plt`. `plt.plot(x, y)`, `plt.scatter`, `plt.bar`, `plt.hist`. Add labels: `plt.title`, `plt.xlabel`. Show with `plt.show()`.",
            [
                {"step": 1, "comment": "Line plot", "code": "import matplotlib.pyplot as plt\nx = [1, 2, 3, 4]\ny = [10, 20, 15, 25]\nplt.plot(x, y, marker='o')\nplt.title('Growth')\nplt.xlabel('day'); plt.ylabel('visits')\nplt.show()"},
            ],
            [
                "Hundreds of overlapping charts in one cell — one focused chart beats ten noisy ones.",
                "Forgetting axis labels and title.",
            ],
            [
                {
                    "question": "Which function draws a line plot?",
                    "options": ["plt.line", "plt.plot", "plt.draw", "plt.linegraph"],
                    "correct": "plt.plot",
                    "explanation": "Surprisingly, `plot` defaults to a line.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "50 · Seaborn — beautiful statistical plots",
            "Matplotlib gives you pixels. Seaborn gives you opinion: sensible defaults, statistical plots ready to go.",
            "Built on matplotlib, but with a friendlier API for the charts you actually want.",
            "`sns.histplot`, `sns.boxplot`, `sns.scatterplot`, `sns.heatmap`. Pass DataFrames directly with `data=df, x='col', y='col'`. Themes: `sns.set_theme()`.",
            [
                {"step": 1, "comment": "Boxplot from a DataFrame", "code": "import seaborn as sns\nimport pandas as pd\ndf = pd.DataFrame({'grade': ['A','A','B','B','C'], 'score': [95,88,75,70,60]})\nsns.boxplot(data=df, x='grade', y='score')"},
            ],
            [
                "Treating seaborn as a total replacement for matplotlib — it layers on top.",
                "Forgetting `import matplotlib.pyplot as plt; plt.show()` in scripts.",
            ],
            [
                {
                    "question": "Seaborn is built on top of...",
                    "options": ["Plotly", "matplotlib", "numpy", "pandas"],
                    "correct": "matplotlib",
                    "explanation": "It's a higher-level wrapper around matplotlib.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "51 · Jupyter notebooks",
            "A notebook mixes code, text, charts, and outputs into one document you can run cell by cell. It's the lab notebook of data science.",
            "Each cell is a tiny script. State is shared across cells, so the order you run them matters.",
            "Install with `pip install jupyter`, start with `jupyter notebook` or use VS Code's built-in support. Markdown cells for notes, code cells for work. Restart-and-run-all to verify reproducibility.",
            [
                {"step": 1, "comment": "Typical notebook cell 1", "code": "import pandas as pd\nimport matplotlib.pyplot as plt\ndf = pd.read_csv('data.csv')\ndf.head()"},
                {"step": 2, "comment": "Cell 2 — a plot", "code": "df['age'].hist()\nplt.show()"},
            ],
            [
                "Running cells out of order and shipping a notebook that won't re-execute top to bottom.",
                "Dropping huge outputs into the notebook and then committing it to git.",
            ],
            [
                {
                    "question": "Why restart-and-run-all before sharing a notebook?",
                    "options": ["Memory cleanup", "Verify reproducibility", "Faster execution", "Required by Jupyter"],
                    "correct": "Verify reproducibility",
                    "explanation": "It proves the notebook runs top to bottom without stale state.",
                }
            ],
            xp=30, mins=8,
        ),
        _lesson(
            "52 · Data cleaning",
            "Real data is ugly: missing values, duplicated rows, wrong types, extra whitespace, typos. 80% of a data scientist's time goes to cleaning. Master this and everything downstream gets easier.",
            "Cleaning is iterative: inspect → fix one issue → inspect again.",
            "Common moves: `df.isna().sum()`, `df.dropna()`, `df.fillna(value)`, `df.drop_duplicates()`, `df['col'].astype(int)`, `df['col'].str.strip()`.",
            [
                {"step": 1, "comment": "Inspect", "code": "print(df.isna().sum())\nprint(df.dtypes)"},
                {"step": 2, "comment": "Fix", "code": "df = df.drop_duplicates()\ndf['age'] = df['age'].fillna(df['age'].median())\ndf['name'] = df['name'].str.strip()"},
            ],
            [
                "Dropping rows with missing values before understanding what's missing and why.",
                "Overwriting the original dataframe without making a copy — hard to rerun.",
            ],
            [
                {
                    "question": "What does `df.dropna()` do?",
                    "options": ["Drops columns", "Drops rows with any NaN", "Fills NaN", "Counts NaN"],
                    "correct": "Drops rows with any NaN",
                    "explanation": "Default axis is 0 (rows).",
                }
            ],
            xp=30, mins=10,
        ),
    ],

    # =========================================================================
    # STAGE 5 — AI / ML Specialization
    # =========================================================================
    "python-stage-5-ai": [
        _lesson(
            "53 · Scikit-learn — your first model",
            "ML sounds scary, but the API for most classical models is the same: `model.fit(X, y)`, `model.predict(X)`. Scikit-learn makes that consistent across 50 algorithms.",
            "Every sklearn estimator has `fit` and `predict`. Once you learn one, you've learned them all.",
            "Steps: load data → split train/test → create model → fit on train → predict on test → evaluate. Start with `LinearRegression` or `LogisticRegression` before jumping to fancier things.",
            [
                {"step": 1, "comment": "Train a regressor", "code": "from sklearn.linear_model import LinearRegression\nfrom sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = LinearRegression().fit(X_train, y_train)\nprint(model.score(X_test, y_test))  # R²"},
            ],
            [
                "Fitting on all data and evaluating on all data — leaks test into train.",
                "Ignoring feature scaling for distance-based models like KNN or SVM.",
            ],
            [
                {
                    "question": "What does `train_test_split` do?",
                    "options": ["Trains the model", "Splits data into train/test", "Predicts", "Evaluates"],
                    "correct": "Splits data into train/test",
                    "explanation": "Usually 80/20 or 70/30.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "54 · TensorFlow / Keras basics",
            "Neural nets used to require writing every gradient by hand. Keras reduces it to: stack layers, compile, fit.",
            "A sequential model is a pile of layers data flows through top to bottom.",
            "`tf.keras.Sequential([...])`, `.compile(optimizer, loss)`, `.fit(x, y, epochs)`. Start with `Dense` for tabular, `Conv2D` for images, `LSTM` for sequences.",
            [
                {"step": 1, "comment": "A tiny classifier", "code": "import tensorflow as tf\nmodel = tf.keras.Sequential([\n    tf.keras.layers.Dense(16, activation='relu', input_shape=(4,)),\n    tf.keras.layers.Dense(3, activation='softmax'),\n])\nmodel.compile('adam', 'sparse_categorical_crossentropy', ['accuracy'])\nmodel.fit(X_train, y_train, epochs=10)"},
            ],
            [
                "Forgetting `input_shape` on the first layer.",
                "Over-training without early stopping — model memorizes instead of learns.",
            ],
            [
                {
                    "question": "Which layer is typical for image input?",
                    "options": ["Dense", "Conv2D", "LSTM", "Embedding"],
                    "correct": "Conv2D",
                    "explanation": "Convolutional layers are designed for spatial data.",
                }
            ],
            xp=30, mins=11,
        ),
        _lesson(
            "55 · PyTorch basics",
            "TensorFlow is declarative; PyTorch feels more like regular Python. Write a forward pass like you'd write any function, and autograd figures out the gradients.",
            "A Tensor is NumPy with GPU support and automatic gradients.",
            "`torch.tensor`, `nn.Module` for models, `nn.CrossEntropyLoss`, `torch.optim`. Training loop: forward → loss → `loss.backward()` → `optimizer.step()` → `optimizer.zero_grad()`.",
            [
                {"step": 1, "comment": "A tiny model", "code": "import torch\nimport torch.nn as nn\n\nmodel = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 3))\nopt = torch.optim.Adam(model.parameters())\nloss_fn = nn.CrossEntropyLoss()"},
                {"step": 2, "comment": "One step", "code": "pred = model(X)\nloss = loss_fn(pred, y)\nloss.backward()\nopt.step()\nopt.zero_grad()"},
            ],
            [
                "Forgetting `optimizer.zero_grad()` — gradients accumulate forever.",
                "Doing math on tensors on different devices (CPU vs GPU).",
            ],
            [
                {
                    "question": "What does `.backward()` do?",
                    "options": ["Reverses the tensor", "Computes gradients", "Goes to previous layer", "Saves model"],
                    "correct": "Computes gradients",
                    "explanation": "It walks the autograd graph backward and fills in `.grad`.",
                }
            ],
            xp=30, mins=11,
        ),
        _lesson(
            "56 · NLP basics",
            "Natural Language Processing turns messy text into numbers a model can chew on. Tokenize, vectorize, train.",
            "Bag-of-words / TF-IDF is still a great baseline before reaching for transformers.",
            "`TfidfVectorizer` from sklearn turns documents into sparse vectors. Train a classifier on top (LogisticRegression works well). For harder tasks, move to embeddings and transformers.",
            [
                {"step": 1, "comment": "Sentiment baseline", "code": "from sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\n\nvec = TfidfVectorizer(ngram_range=(1,2))\nX = vec.fit_transform(docs)\nclf = LogisticRegression().fit(X, labels)"},
            ],
            [
                "Skipping basic text cleaning (lowercase, remove punctuation) for traditional models.",
                "Jumping to huge LLMs for tiny problems — start simple.",
            ],
            [
                {
                    "question": "What does TF-IDF capture?",
                    "options": ["Word order", "Word frequency weighted by rarity", "Sentence length", "Language"],
                    "correct": "Word frequency weighted by rarity",
                    "explanation": "Common words get low weight, rare informative ones get high.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "57 · Model evaluation",
            "A 99% accurate spam detector sounds great — until you realize 99% of emails aren't spam, and it's classifying everything as 'not spam'. Accuracy lies.",
            "Use the metric that matches the question: accuracy, precision, recall, F1, ROC AUC, MAE, MSE, RMSE, R².",
            "For classification: confusion matrix → precision (of predicted positives, how many right) and recall (of actual positives, how many caught). F1 balances both. For regression: MAE is robust, RMSE penalizes big errors.",
            [
                {"step": 1, "comment": "Full report", "code": "from sklearn.metrics import classification_report, confusion_matrix\nprint(confusion_matrix(y_true, y_pred))\nprint(classification_report(y_true, y_pred))"},
            ],
            [
                "Reporting only accuracy on imbalanced datasets.",
                "Tuning on the test set — now your 'test' score is optimistic.",
            ],
            [
                {
                    "question": "Which metric is misleading on imbalanced data?",
                    "options": ["Recall", "Accuracy", "F1", "AUC"],
                    "correct": "Accuracy",
                    "explanation": "You can score high by always predicting the majority class.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "58 · Computer vision first touch",
            "Teaching a computer to recognize a cat used to require hand-coded features. Deep nets do it automatically — but the pipeline (load images → augment → feed to CNN) is a skill.",
            "A CNN learns spatial features layer by layer. Early layers detect edges; deep layers detect objects.",
            "Use `torchvision` or `tf.keras.datasets` for benchmarks (MNIST, CIFAR). Build a small CNN with Conv → ReLU → Pool → Dense. Augment images (flip, crop, rotate) for free extra data.",
            [
                {"step": 1, "comment": "Keras CNN skeleton", "code": "import tensorflow as tf\nmodel = tf.keras.Sequential([\n    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28,28,1)),\n    tf.keras.layers.MaxPool2D(),\n    tf.keras.layers.Flatten(),\n    tf.keras.layers.Dense(10, activation='softmax'),\n])"},
            ],
            [
                "Training with unnormalized pixel values (0-255) — always divide by 255.",
                "Ignoring augmentation and overfitting on tiny datasets.",
            ],
            [
                {
                    "question": "What does a pooling layer do?",
                    "options": ["Adds parameters", "Downsamples the feature map", "Upsamples", "Randomizes"],
                    "correct": "Downsamples the feature map",
                    "explanation": "Pooling shrinks the spatial dimensions, keeping dominant features.",
                }
            ],
            xp=30, mins=11,
        ),
    ],

    # =========================================================================
    # STAGE 5 — Automation Specialization
    # =========================================================================
    "python-stage-5-auto": [
        _lesson(
            "59 · The os and sys modules",
            "Python can walk your filesystem, read environment variables, and launch other programs. That's the starting gun for automation.",
            "`os` is for the filesystem and environment; `sys` is for the running interpreter.",
            "`os.listdir`, `os.walk`, `os.path.join`, `os.environ['KEY']`, `sys.argv` (command-line args), `sys.exit(code)`. Prefer `pathlib.Path` for new code — it's nicer.",
            [
                {"step": 1, "comment": "Walk a directory", "code": "import os\nfor root, dirs, files in os.walk('.'):\n    for f in files:\n        print(os.path.join(root, f))"},
                {"step": 2, "comment": "Args and env", "code": "import sys, os\nprint('script:', sys.argv[0])\nprint('api key:', os.environ.get('API_KEY', 'not set'))"},
            ],
            [
                "Hard-coding paths with backslashes — use `os.path.join` or `pathlib`.",
                "Reading secrets from code instead of env vars.",
            ],
            [
                {
                    "question": "Which reads an environment variable safely?",
                    "options": ["os.env['KEY']", "os.environ.get('KEY')", "sys.env('KEY')", "env('KEY')"],
                    "correct": "os.environ.get('KEY')",
                    "explanation": "`.get` avoids KeyError if the var is missing.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "60 · Selenium — browser automation",
            "Some sites are only usable through a browser (complex JavaScript, logins, dynamic content). Selenium drives a real browser from Python.",
            "You're writing a robot user: open browser, click here, type there, read this.",
            "Install `selenium` and a matching driver (ChromeDriver/Geckodriver). `driver.get(url)`, `driver.find_element(By.ID, '...')`, `.click()`, `.send_keys('text')`. Always `driver.quit()` at the end.",
            [
                {"step": 1, "comment": "Basic flow", "code": "from selenium import webdriver\nfrom selenium.webdriver.common.by import By\n\ndriver = webdriver.Chrome()\ntry:\n    driver.get('https://example.com')\n    heading = driver.find_element(By.TAG_NAME, 'h1').text\n    print(heading)\nfinally:\n    driver.quit()"},
            ],
            [
                "Not quitting the driver on error — leaves zombie browser processes.",
                "Hard-coded `time.sleep` everywhere instead of explicit waits.",
            ],
            [
                {
                    "question": "Why do you need a driver binary for Selenium?",
                    "options": ["Faster JS", "It's the bridge between Python and the real browser", "Stores cookies", "Required by law"],
                    "correct": "It's the bridge between Python and the real browser",
                    "explanation": "Selenium talks to ChromeDriver, which talks to Chrome.",
                }
            ],
            xp=30, mins=10,
        ),
        _lesson(
            "61 · Task scheduling",
            "You've written a daily report script. You'd rather not wake up at 6am to run it. Schedulers make Python run on a timer.",
            "For long-running Python-only scripts, use the `schedule` library. For the OS to run your script on a cron-like schedule, use cron (Linux/Mac) or Task Scheduler (Windows).",
            "`schedule.every().day.at('06:00').do(job)` and loop forever with `schedule.run_pending()`. For robustness, prefer OS schedulers — they survive reboots.",
            [
                {"step": 1, "comment": "schedule library", "code": "import schedule, time\n\ndef job():\n    print('running')\n\nschedule.every(10).seconds.do(job)\nwhile True:\n    schedule.run_pending()\n    time.sleep(1)"},
            ],
            [
                "Keeping the process alive with a while True loop on a laptop — use a server or cron.",
                "No logging — when the job fails silently you have no idea.",
            ],
            [
                {
                    "question": "On Linux, what's the classic scheduler?",
                    "options": ["schedule", "cron", "timer", "run"],
                    "correct": "cron",
                    "explanation": "`crontab -e` lets you define recurring jobs.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "62 · Email automation",
            "Send a daily summary, invoice, or alert without opening your inbox. Python speaks SMTP natively.",
            "SMTP is how email travels. Python's `smtplib` plus a real provider (Gmail app password, SendGrid, Mailgun) sends it.",
            "Build the message with `email.message.EmailMessage`, attach files with `add_attachment`, then `smtplib.SMTP_SSL(host).send_message(msg)`. Never hard-code the password — use env vars.",
            [
                {"step": 1, "comment": "Send a plain mail", "code": "import os, smtplib\nfrom email.message import EmailMessage\n\nmsg = EmailMessage()\nmsg['From'] = 'me@example.com'\nmsg['To'] = 'friend@example.com'\nmsg['Subject'] = 'Daily report'\nmsg.set_content('Today was good.')\n\nwith smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:\n    s.login('me@example.com', os.environ['APP_PASS'])\n    s.send_message(msg)"},
            ],
            [
                "Using your main Gmail password instead of an app password.",
                "No retry/backoff if the SMTP server is temporarily down.",
            ],
            [
                {
                    "question": "Which protocol sends email?",
                    "options": ["SMTP", "IMAP", "POP3", "HTTP"],
                    "correct": "SMTP",
                    "explanation": "SMTP = Simple Mail Transfer Protocol.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "63 · Excel with openpyxl",
            "Your boss lives in Excel. Reading and writing .xlsx from Python means you can automate reports the rest of the office will actually open.",
            "openpyxl treats a workbook as a dict of sheets, each sheet as a grid of cells.",
            "`load_workbook(path)`, `wb['Sheet1']`, `sheet['A1'] = value`, `wb.save(path)`. For large data, iterate with `sheet.iter_rows()`. Styles and formulas are supported.",
            [
                {"step": 1, "comment": "Write a report", "code": "from openpyxl import Workbook\nwb = Workbook()\nws = wb.active\nws.title = 'Report'\nws.append(['Name', 'Score'])\nws.append(['Arjun', 95])\nws.append(['Suhana', 88])\nwb.save('report.xlsx')"},
            ],
            [
                "Loading massive files into memory — use `read_only=True` for speed.",
                "Overwriting the original file without a backup.",
            ],
            [
                {
                    "question": "Which file format does openpyxl handle?",
                    "options": [".xls", ".xlsx", ".csv", ".ods"],
                    "correct": ".xlsx",
                    "explanation": "Modern Excel only. Use pandas+xlrd for legacy .xls.",
                }
            ],
            xp=30, mins=9,
        ),
        _lesson(
            "64 · PDF handling",
            "PDFs are the annoying cousins of the file world: hard to edit, harder to extract text from. Python has libraries for reading, splitting, merging, and writing.",
            "Use `pypdf` to read/split/merge and `reportlab` or `fpdf2` to generate from scratch.",
            "`PdfReader(path)` gives you pages and text. `PdfWriter` assembles new PDFs. For pixel-perfect generated reports, `reportlab` draws at the coordinate level.",
            [
                {"step": 1, "comment": "Read and extract", "code": "from pypdf import PdfReader\nreader = PdfReader('doc.pdf')\nfor page in reader.pages:\n    print(page.extract_text())"},
                {"step": 2, "comment": "Merge", "code": "from pypdf import PdfWriter\nwriter = PdfWriter()\nfor p in ['a.pdf', 'b.pdf']:\n    writer.append(p)\nwith open('merged.pdf', 'wb') as f:\n    writer.write(f)"},
            ],
            [
                "Trying to extract text from scanned PDFs without OCR — you need Tesseract for that.",
                "Assuming `extract_text` is perfect; PDF text extraction is famously messy.",
            ],
            [
                {
                    "question": "Which library reads modern PDF text?",
                    "options": ["pypdf", "openpyxl", "PyInstaller", "beautifulsoup4"],
                    "correct": "pypdf",
                    "explanation": "pypdf is the modern maintained fork of PyPDF2.",
                }
            ],
            xp=30, mins=9,
        ),
    ],

    # =========================================================================
    # STAGE 6 — Pro Level
    # =========================================================================
    "python-stage-6-pro": [
        _lesson(
            "65 · Design patterns — the common ones",
            "Every experienced developer has seen the same problems in different clothes. Design patterns are the named solutions the community keeps rediscovering.",
            "Patterns aren't recipes; they're vocabulary. You don't 'apply' them — you recognize when one fits.",
            "The essentials for Python: Strategy (swap behaviour at runtime), Factory (hide construction), Observer (pub/sub), Singleton (one instance — often avoidable), Adapter (bridge APIs). Most Python uses are simpler than the Java originals.",
            [
                {"step": 1, "comment": "Strategy via first-class functions", "code": "def process(items, strategy):\n    return sorted(items, key=strategy)\n\nprint(process(['kiwi','apple'], len))\nprint(process(['kiwi','apple'], str.lower))"},
            ],
            [
                "Applying a pattern before you have the problem — YAGNI.",
                "Porting Java-style class hierarchies to Python — functions are often enough.",
            ],
            [
                {
                    "question": "Which pattern swaps behaviour at runtime?",
                    "options": ["Singleton", "Strategy", "Factory", "Decorator"],
                    "correct": "Strategy",
                    "explanation": "Pass in the algorithm as a parameter.",
                }
            ],
            xp=40, mins=11,
        ),
        _lesson(
            "66 · Clean code principles",
            "Code is read ten times more than it's written. Spend effort making it boring, obvious, and small — not clever.",
            "Name things well, keep functions tiny, delete duplication, and write the code for the next person.",
            "Rules of thumb: functions do one thing, fit on a screen, and have ≤ 3 parameters. Names describe intent (`days_to_expiry`, not `d`). Comments explain *why*, not *what*. If it's hard to test, it's hard to change.",
            [
                {"step": 1, "comment": "Before", "code": "def p(d):\n    r = 0\n    for i in d:\n        if i > 0: r += i\n    return r"},
                {"step": 2, "comment": "After", "code": "def sum_positive(nums):\n    return sum(n for n in nums if n > 0)"},
            ],
            [
                "Premature abstraction — three copies is OK before extracting.",
                "Comments that describe what the code does instead of why it does it.",
            ],
            [
                {
                    "question": "What should comments explain?",
                    "options": ["What", "Why", "Who", "When"],
                    "correct": "Why",
                    "explanation": "The code shows the what; comments should explain the why.",
                }
            ],
            xp=40, mins=10,
        ),
        _lesson(
            "67 · Performance optimization",
            "Your script takes 12 minutes. Your boss wants it in under 30 seconds. You don't guess — you measure, find the hotspot, and fix that one thing.",
            "Profile first, optimize second. Most of the slowdown is in a tiny fraction of the code.",
            "Use `cProfile` for CPU profiles. Swap Python loops for NumPy/Pandas vector ops. Use `lru_cache` for expensive pure functions. Avoid global lookups in hot loops.",
            [
                {"step": 1, "comment": "Profile", "code": "import cProfile\ncProfile.run('my_func()', sort='cumulative')"},
                {"step": 2, "comment": "Cache", "code": "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n-1) + fib(n-2)"},
            ],
            [
                "Micro-optimizing before profiling — you fix the wrong thing.",
                "Pre-allocating in ways that hurt readability without measurable gain.",
            ],
            [
                {
                    "question": "What does `cProfile` do?",
                    "options": ["Tests code", "Shows where time is spent", "Compiles to C", "Formats code"],
                    "correct": "Shows where time is spent",
                    "explanation": "It reports function call counts and cumulative time.",
                }
            ],
            xp=40, mins=10,
        ),
        _lesson(
            "68 · Memory management",
            "Python has a garbage collector, but you can still leak memory — hold a reference and the GC leaves it alone.",
            "Memory usually grows because something is holding on: caches, global lists, closures, long-lived objects.",
            "Use `sys.getsizeof` for small checks, `tracemalloc` for real leak hunts. Generators beat lists for streaming. Use `__slots__` on classes with millions of instances.",
            [
                {"step": 1, "comment": "tracemalloc snapshot", "code": "import tracemalloc\ntracemalloc.start()\n# ... run your code ...\nsnap = tracemalloc.take_snapshot()\nfor stat in snap.statistics('lineno')[:10]:\n    print(stat)"},
            ],
            [
                "Keeping huge objects alive in a global cache.",
                "Using lists where a generator or iterator would stream.",
            ],
            [
                {
                    "question": "Which helps trace memory leaks?",
                    "options": ["cProfile", "tracemalloc", "timeit", "pdb"],
                    "correct": "tracemalloc",
                    "explanation": "It tracks object allocations line by line.",
                }
            ],
            xp=40, mins=9,
        ),
        _lesson(
            "69 · CI/CD pipelines",
            "You push code. A robot runs your tests. If they pass, another robot deploys to staging. That's CI/CD — and it's how real teams ship without fear.",
            "CI = continuous integration (run tests on every push). CD = continuous delivery/deployment (auto-ship what passes).",
            "GitHub Actions is the easy on-ramp: a YAML file in `.github/workflows/` describes the jobs. Typical steps: checkout → setup Python → install deps → run `pytest` → upload coverage.",
            [
                {"step": 1, "comment": ".github/workflows/test.yml", "code": "name: Test\non: [push, pull_request]\njobs:\n  pytest:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.11'\n      - run: pip install -r requirements.txt\n      - run: pytest -v"},
            ],
            [
                "No tests before setting up CI — you'll just be running nothing.",
                "Skipping the pipeline 'just this once' and committing broken code.",
            ],
            [
                {
                    "question": "What runs on every push?",
                    "options": ["CD", "CI", "QA", "PR"],
                    "correct": "CI",
                    "explanation": "Continuous Integration = run checks on each change.",
                }
            ],
            xp=40, mins=10,
        ),
        _lesson(
            "70 · Docker + Python",
            "'Works on my machine' is a meme for a reason. Docker packs your app + Python + OS libs into one reproducible box that runs anywhere.",
            "An image is a frozen filesystem. A container is a running instance of that image.",
            "Write a `Dockerfile`, build with `docker build -t name .`, run with `docker run -p 8000:8000 name`. Use slim/alpine base images, pin versions, and layer smartly (COPY requirements.txt before the rest for cache hits).",
            [
                {"step": 1, "comment": "Dockerfile", "code": "FROM python:3.11-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"python\", \"main.py\"]"},
            ],
            [
                "Installing everything on every build because you COPY first.",
                "Running as root inside the container.",
            ],
            [
                {
                    "question": "Why COPY `requirements.txt` separately before the rest?",
                    "options": ["Smaller image", "Layer cache hits on code changes", "Security", "Tradition"],
                    "correct": "Layer cache hits on code changes",
                    "explanation": "Code changes don't invalidate the dependency layer.",
                }
            ],
            xp=40, mins=11,
        ),
        _lesson(
            "71 · Test-driven development (TDD)",
            "TDD flips the loop: write a failing test first, then just enough code to pass, then refactor. It feels slow at first and spoils you forever.",
            "Red → Green → Refactor. Each cycle is tiny — minutes, not hours.",
            "Start with the simplest failing test. Write the obvious code to pass it. Clean up. Repeat. You end with a test suite, a clean design, and confidence to change anything later.",
            [
                {"step": 1, "comment": "Failing test first", "code": "# test_math.py\ndef test_add():\n    from mymath import add\n    assert add(2, 3) == 5\n# running pytest → red (no add)"},
                {"step": 2, "comment": "Minimal code", "code": "# mymath.py\ndef add(a, b):\n    return a + b\n# green"},
                {"step": 3, "comment": "Refactor if needed", "code": "# keep green, tidy names/signatures"},
            ],
            [
                "Writing the implementation first, then back-filling tests — easier to fool yourself.",
                "Huge tests that require huge implementations — keep steps tiny.",
            ],
            [
                {
                    "question": "TDD order?",
                    "options": ["Test → Code → Refactor", "Code → Test → Refactor", "Refactor → Code → Test", "Any order"],
                    "correct": "Test → Code → Refactor",
                    "explanation": "Red, green, refactor.",
                }
            ],
            xp=40, mins=10,
        ),
        _lesson(
            "72 · Contributing to open source",
            "Most of the code you use is free because strangers maintain it. Contributing back teaches you more than any tutorial — and it looks great on your resume.",
            "Start small: fix a typo in docs, improve an error message, add a missing test. You don't need to rewrite the core.",
            "Find a good-first-issue on GitHub. Fork → clone → create a branch → make a change → add tests → run the project's tests → push → open a PR. Be patient; expect review feedback.",
            [
                {"step": 1, "comment": "The standard PR flow", "code": "# terminal\ngit clone https://github.com/fork/project\ngit checkout -b fix-typo\n# edit, commit\ngit push origin fix-typo\n# open PR on GitHub"},
            ],
            [
                "Opening a PR without reading CONTRIBUTING.md.",
                "Getting discouraged by the first round of review comments.",
            ],
            [
                {
                    "question": "Which label marks issues newcomers can tackle?",
                    "options": ["newbie", "good-first-issue", "easy", "starter"],
                    "correct": "good-first-issue",
                    "explanation": "GitHub's convention — often filterable from the issues tab.",
                }
            ],
            xp=40, mins=9,
        ),
        _lesson(
            "73 · Code reviews",
            "The best engineers aren't the ones who write flawless code. They're the ones whose code is easy to review and who review others' code generously.",
            "Be the reviewer you'd want: kind, specific, and focused on the code, not the author.",
            "When reviewing: ask questions before prescribing fixes, praise clear code, flag one thing at a time, and approve when it's 'good enough' — not 'perfect'. When being reviewed: assume good intent and explain your thinking.",
            [
                {"step": 1, "comment": "A constructive comment template", "code": "# Instead of: 'This is wrong'\n# Try:\n# 'I think this can raise when list is empty. Should we add a guard, or\n#  is the caller expected to never pass an empty list?'"},
            ],
            [
                "Bike-shedding on style that a linter could enforce.",
                "Rubber-stamping PRs without reading them.",
            ],
            [
                {
                    "question": "What's the goal of a good review comment?",
                    "options": ["Criticism", "Clarify and improve the code", "Show expertise", "Slow the author"],
                    "correct": "Clarify and improve the code",
                    "explanation": "Reviews are a conversation about the code, not judgment on the author.",
                }
            ],
            xp=40, mins=8,
        ),
        _lesson(
            "74 · Build and publish your own package",
            "You wrote a useful tool. Instead of copy-pasting it into five projects, turn it into a pip-installable package. Ten lines of pyproject.toml and you're in PyPI.",
            "A package is just a folder with an `__init__.py` plus metadata. Modern Python packaging is surprisingly simple.",
            "Use a `pyproject.toml` with `[project]` metadata. Build with `python -m build`. Upload to PyPI with `twine upload dist/*`. Test on TestPyPI first.",
            [
                {"step": 1, "comment": "pyproject.toml", "code": "[project]\nname = \"myutil\"\nversion = \"0.1.0\"\ndescription = \"A useful utility\"\nauthors = [{name = \"Your Name\"}]\nrequires-python = \">=3.9\"\n\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\""},
                {"step": 2, "comment": "Build and upload", "code": "# terminal\npip install build twine\npython -m build\ntwine upload dist/*"},
            ],
            [
                "Using someone else's package name — always check PyPI first.",
                "Publishing without a README — users will pass.",
            ],
            [
                {
                    "question": "Where is the canonical Python package registry?",
                    "options": ["GitHub", "PyPI", "npm", "Maven"],
                    "correct": "PyPI",
                    "explanation": "pypi.org is where `pip install` pulls from.",
                }
            ],
            xp=40, mins=11,
        ),
    ],
}


# =============================================================================
# PRACTICE PROBLEMS — coding challenges linked to roadmap stages
# =============================================================================
# Each problem has a `track_slug` field so the seeder can route it to the right
# track. All use simple stdin/stdout that the local Python runner can validate.
PYTHON_ROADMAP_PROBLEMS: list[dict] = [
    # ---------- STAGE 1 ----------
    {
        "track_slug": "python-stage-1-beginner",
        "title": "Hello, Name!",
        "slug": "py-hello-name",
        "description": "Read a name from input and print `Hello, <name>!`.",
        "difficulty": 1,
        "tags": ["python", "beginner", "input"],
        "xp_reward": 15,
        "examples_json": [{"input": "Suhana", "output": "Hello, Suhana!"}],
        "test_cases_json": [
            {"input": "Suhana\n", "output": "Hello, Suhana!"},
            {"input": "Arjun\n", "output": "Hello, Arjun!"},
        ],
        "starter_code_json": {"python": "name = input()\n# Print the greeting\n"},
        "hints_json": [{"level": 1, "text": "Use f-strings: f'Hello, {name}!'"}],
    },
    {
        "track_slug": "python-stage-1-beginner",
        "title": "Sum of Two Numbers",
        "slug": "py-sum-two",
        "description": "Read two integers on separate lines and print their sum.",
        "difficulty": 1,
        "tags": ["python", "beginner", "math"],
        "xp_reward": 15,
        "examples_json": [{"input": "3\n4\n", "output": "7"}],
        "test_cases_json": [
            {"input": "3\n4\n", "output": "7"},
            {"input": "-5\n10\n", "output": "5"},
            {"input": "0\n0\n", "output": "0"},
        ],
        "starter_code_json": {"python": "a = int(input())\nb = int(input())\n# print the sum\n"},
        "hints_json": [{"level": 1, "text": "Don't forget int() — input() returns a string."}],
    },
    {
        "track_slug": "python-stage-1-beginner",
        "title": "FizzBuzz",
        "slug": "py-fizzbuzz",
        "description": "For each number from 1 to N, print 'Fizz' if divisible by 3, 'Buzz' if by 5, 'FizzBuzz' if by both, else the number itself. One per line.",
        "difficulty": 2,
        "tags": ["python", "beginner", "loops"],
        "xp_reward": 25,
        "examples_json": [{"input": "5", "output": "1\n2\nFizz\n4\nBuzz"}],
        "test_cases_json": [
            {"input": "5\n", "output": "1\n2\nFizz\n4\nBuzz"},
            {"input": "15\n", "output": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"},
        ],
        "starter_code_json": {"python": "n = int(input())\n# Print 1..n with Fizz/Buzz rules\n"},
        "hints_json": [
            {"level": 1, "text": "Check divisible-by-15 first, then 3, then 5."},
            {"level": 2, "text": "Use `%` for remainder."},
        ],
    },
    {
        "track_slug": "python-stage-1-beginner",
        "title": "Count Vowels",
        "slug": "py-count-vowels",
        "description": "Read a line of text. Print the number of vowels (a, e, i, o, u) — case-insensitive.",
        "difficulty": 1,
        "tags": ["python", "beginner", "strings"],
        "xp_reward": 20,
        "examples_json": [{"input": "Hello World", "output": "3"}],
        "test_cases_json": [
            {"input": "Hello World\n", "output": "3"},
            {"input": "PYTHON\n", "output": "1"},
            {"input": "bcdfg\n", "output": "0"},
        ],
        "starter_code_json": {"python": "s = input()\n# count the vowels\n"},
        "hints_json": [{"level": 1, "text": "Lowercase first, then check membership in a set of vowels."}],
    },

    # ---------- STAGE 2 ----------
    {
        "track_slug": "python-stage-2-core",
        "title": "Word Frequency",
        "slug": "py-word-freq",
        "description": "Read a line of text and print the most frequent word (lowercased). Ties broken by first appearance.",
        "difficulty": 2,
        "tags": ["python", "core", "dicts"],
        "xp_reward": 30,
        "examples_json": [{"input": "the cat sat on the mat the", "output": "the"}],
        "test_cases_json": [
            {"input": "the cat sat on the mat the\n", "output": "the"},
            {"input": "apple kiwi apple mango kiwi apple\n", "output": "apple"},
        ],
        "starter_code_json": {"python": "text = input().lower()\n# find the most frequent word\n"},
        "hints_json": [{"level": 1, "text": "Use a dict of counts, or collections.Counter."}],
    },
    {
        "track_slug": "python-stage-2-core",
        "title": "Squares Under N",
        "slug": "py-squares-under-n",
        "description": "Given N, print all perfect squares less than N, space-separated. Use a list comprehension.",
        "difficulty": 2,
        "tags": ["python", "core", "comprehensions"],
        "xp_reward": 25,
        "examples_json": [{"input": "30", "output": "1 4 9 16 25"}],
        "test_cases_json": [
            {"input": "30\n", "output": "1 4 9 16 25"},
            {"input": "10\n", "output": "1 4 9"},
            {"input": "1\n", "output": ""},
        ],
        "starter_code_json": {"python": "n = int(input())\n# one-line comprehension for squares\n"},
        "hints_json": [{"level": 1, "text": "`[i*i for i in range(1, n) if i*i < n]`."}],
    },
    {
        "track_slug": "python-stage-2-core",
        "title": "Safe Divide",
        "slug": "py-safe-divide",
        "description": "Read two integers a and b. Print `a / b` as float with two decimals, or `error` if b == 0 or input is not numeric.",
        "difficulty": 2,
        "tags": ["python", "core", "exceptions"],
        "xp_reward": 30,
        "examples_json": [{"input": "10\n4", "output": "2.50"}],
        "test_cases_json": [
            {"input": "10\n4\n", "output": "2.50"},
            {"input": "7\n0\n", "output": "error"},
            {"input": "abc\n4\n", "output": "error"},
        ],
        "starter_code_json": {"python": "try:\n    a = int(input())\n    b = int(input())\n    # compute and print\nexcept Exception:\n    print('error')\n"},
        "hints_json": [{"level": 1, "text": "Format with f'{x:.2f}'."}],
    },

    # ---------- STAGE 3 ----------
    {
        "track_slug": "python-stage-3-oop",
        "title": "Bank Account",
        "slug": "py-bank-account",
        "description": "Implement a `BankAccount` class with `deposit(amt)` and `withdraw(amt)` methods. Raise ValueError if withdraw exceeds balance. Print the final balance after a sequence of commands read from input: first line is N, then N lines of `d 100` or `w 50`.",
        "difficulty": 3,
        "tags": ["python", "oop", "classes"],
        "xp_reward": 40,
        "examples_json": [{"input": "3\nd 100\nd 50\nw 30", "output": "120"}],
        "test_cases_json": [
            {"input": "3\nd 100\nd 50\nw 30\n", "output": "120"},
            {"input": "2\nd 200\nw 50\n", "output": "150"},
        ],
        "starter_code_json": {"python": "class BankAccount:\n    def __init__(self):\n        self.balance = 0\n    def deposit(self, amt):\n        pass\n    def withdraw(self, amt):\n        pass\n\nn = int(input())\nacc = BankAccount()\nfor _ in range(n):\n    cmd, amt = input().split()\n    # dispatch\nprint(acc.balance)\n"},
        "hints_json": [{"level": 1, "text": "Split the line, convert amt to int, call the right method."}],
    },
    {
        "track_slug": "python-stage-3-oop",
        "title": "Shape Area",
        "slug": "py-shape-area",
        "description": "Create `Circle` and `Square` classes, both with an `area()` method. Read a shape type and a size, then print its area (circle uses pi=3.14, two decimals).",
        "difficulty": 2,
        "tags": ["python", "oop", "polymorphism"],
        "xp_reward": 30,
        "examples_json": [{"input": "circle\n5", "output": "78.50"}, {"input": "square\n4", "output": "16.00"}],
        "test_cases_json": [
            {"input": "circle\n5\n", "output": "78.50"},
            {"input": "square\n4\n", "output": "16.00"},
        ],
        "starter_code_json": {"python": "class Circle:\n    def __init__(self, r): self.r = r\n    def area(self): return 3.14 * self.r * self.r\n\nclass Square:\n    def __init__(self, s): self.s = s\n    def area(self): return self.s * self.s\n\nkind = input().strip()\nsize = float(input())\n# build and print\n"},
        "hints_json": [{"level": 1, "text": "Use `:.2f` formatting."}],
    },

    # ---------- STAGE 4 ----------
    {
        "track_slug": "python-stage-4-intermediate",
        "title": "JSON Picker",
        "slug": "py-json-picker",
        "description": "Read a JSON object on one line and a key on the next. Print the value for that key, or `null` if missing.",
        "difficulty": 2,
        "tags": ["python", "intermediate", "json"],
        "xp_reward": 30,
        "examples_json": [{"input": '{"a": 1, "b": 2}\na', "output": "1"}],
        "test_cases_json": [
            {"input": '{"a": 1, "b": 2}\na\n', "output": "1"},
            {"input": '{"name": "Arjun"}\nage\n', "output": "null"},
        ],
        "starter_code_json": {"python": "import json\ndata = json.loads(input())\nkey = input().strip()\n# print value or 'null'\n"},
        "hints_json": [{"level": 1, "text": "Use dict.get with a default."}],
    },
    {
        "track_slug": "python-stage-4-intermediate",
        "title": "Running Average (Generator)",
        "slug": "py-running-avg",
        "description": "Read N integers (first line is N, second line is space-separated values). Using a generator function `running_avg(nums)` that yields the running average after each element, print all averages space-separated, rounded to 2 decimals.",
        "difficulty": 3,
        "tags": ["python", "intermediate", "generators"],
        "xp_reward": 40,
        "examples_json": [{"input": "4\n1 2 3 4", "output": "1.00 1.50 2.00 2.50"}],
        "test_cases_json": [
            {"input": "4\n1 2 3 4\n", "output": "1.00 1.50 2.00 2.50"},
            {"input": "3\n10 20 30\n", "output": "10.00 15.00 20.00"},
        ],
        "starter_code_json": {"python": "def running_avg(nums):\n    total = 0\n    for i, n in enumerate(nums, 1):\n        total += n\n        yield total / i\n\nn = int(input())\nnums = list(map(int, input().split()))\nprint(' '.join(f'{a:.2f}' for a in running_avg(nums)))\n"},
        "hints_json": [{"level": 1, "text": "The starter already shows the pattern — tweak and submit."}],
    },
    {
        "track_slug": "python-stage-4-intermediate",
        "title": "Unique Lines (Context Manager simulated)",
        "slug": "py-unique-lines",
        "description": "Read N lines of text. Print only unique lines, preserving first-seen order.",
        "difficulty": 2,
        "tags": ["python", "intermediate", "sets"],
        "xp_reward": 30,
        "examples_json": [{"input": "4\nhi\nok\nhi\nbye", "output": "hi\nok\nbye"}],
        "test_cases_json": [
            {"input": "4\nhi\nok\nhi\nbye\n", "output": "hi\nok\nbye"},
            {"input": "3\na\nb\na\n", "output": "a\nb"},
        ],
        "starter_code_json": {"python": "n = int(input())\nseen = set()\n# read and print unique lines in order\n"},
        "hints_json": [{"level": 1, "text": "Use a set to track seen, list or direct print for order."}],
    },

    # ---------- STAGE 5 (Web/Data/AI/Auto) ----------
    {
        "track_slug": "python-stage-5-data",
        "title": "Column Mean",
        "slug": "py-column-mean",
        "description": "You are given N rows of M space-separated integers. Print the mean of each column, rounded to 2 decimals, space-separated.",
        "difficulty": 2,
        "tags": ["python", "data", "numpy"],
        "xp_reward": 35,
        "examples_json": [{"input": "2\n1 2 3\n4 5 6", "output": "2.50 3.50 4.50"}],
        "test_cases_json": [
            {"input": "2\n1 2 3\n4 5 6\n", "output": "2.50 3.50 4.50"},
            {"input": "3\n10 0\n20 0\n30 0\n", "output": "20.00 0.00"},
        ],
        "starter_code_json": {"python": "n = int(input())\nrows = [list(map(int, input().split())) for _ in range(n)]\n# compute column means\n"},
        "hints_json": [{"level": 1, "text": "Transpose with zip(*rows), average each column."}],
    },
    {
        "track_slug": "python-stage-5-ai",
        "title": "Accuracy Metric",
        "slug": "py-accuracy",
        "description": "Read a line of predicted labels and a line of true labels (space-separated). Print accuracy as a percentage rounded to 2 decimals (e.g. `80.00`).",
        "difficulty": 2,
        "tags": ["python", "ai", "metrics"],
        "xp_reward": 35,
        "examples_json": [{"input": "1 0 1 1 0\n1 0 0 1 0", "output": "80.00"}],
        "test_cases_json": [
            {"input": "1 0 1 1 0\n1 0 0 1 0\n", "output": "80.00"},
            {"input": "1 1 1\n1 1 1\n", "output": "100.00"},
        ],
        "starter_code_json": {"python": "pred = input().split()\ntrue = input().split()\n# compute accuracy\n"},
        "hints_json": [{"level": 1, "text": "Count matches with sum(p == t for p, t in zip(pred, true))."}],
    },
    {
        "track_slug": "python-stage-5-auto",
        "title": "Rename by Pattern",
        "slug": "py-rename-pattern",
        "description": "Read N filenames and print them after normalizing: lowercase, spaces → underscores, strip leading/trailing whitespace.",
        "difficulty": 1,
        "tags": ["python", "automation", "strings"],
        "xp_reward": 25,
        "examples_json": [{"input": "2\n My Photo.JPG\nReport Final.PDF", "output": "my_photo.jpg\nreport_final.pdf"}],
        "test_cases_json": [
            {"input": "2\n My Photo.JPG\nReport Final.PDF\n", "output": "my_photo.jpg\nreport_final.pdf"},
            {"input": "1\nHELLO WORLD.TXT\n", "output": "hello_world.txt"},
        ],
        "starter_code_json": {"python": "n = int(input())\nfor _ in range(n):\n    name = input()\n    # normalize and print\n"},
        "hints_json": [{"level": 1, "text": "`.strip().lower().replace(' ', '_')`"}],
    },
    {
        "track_slug": "python-stage-5-web",
        "title": "Build a URL Path",
        "slug": "py-build-url",
        "description": "Read a base URL on line 1 and N path segments on the following N lines (first line after base is N). Print the full URL joined by single slashes, no trailing slash.",
        "difficulty": 1,
        "tags": ["python", "web", "strings"],
        "xp_reward": 25,
        "examples_json": [{"input": "https://api.example.com\n2\nusers\n42", "output": "https://api.example.com/users/42"}],
        "test_cases_json": [
            {"input": "https://api.example.com\n2\nusers\n42\n", "output": "https://api.example.com/users/42"},
            {"input": "http://x.com/\n1\nhello\n", "output": "http://x.com/hello"},
        ],
        "starter_code_json": {"python": "base = input().rstrip('/')\nn = int(input())\nsegs = [input().strip('/') for _ in range(n)]\n# print the joined URL\n"},
        "hints_json": [{"level": 1, "text": "Join segments with '/' and prepend the base."}],
    },

    # ---------- STAGE 6 ----------
    {
        "track_slug": "python-stage-6-pro",
        "title": "LRU Cache with @lru_cache",
        "slug": "py-lru-fib",
        "description": "Compute the Nth Fibonacci number (N up to 100) using `@functools.lru_cache`.",
        "difficulty": 3,
        "tags": ["python", "pro", "performance"],
        "xp_reward": 50,
        "examples_json": [{"input": "10", "output": "55"}, {"input": "50", "output": "12586269025"}],
        "test_cases_json": [
            {"input": "10\n", "output": "55"},
            {"input": "50\n", "output": "12586269025"},
            {"input": "1\n", "output": "1"},
        ],
        "starter_code_json": {"python": "from functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)\n\nn = int(input())\nprint(fib(n))\n"},
        "hints_json": [{"level": 1, "text": "The starter is ready — just submit."}],
    },
    {
        "track_slug": "python-stage-6-pro",
        "title": "Log Parser",
        "slug": "py-log-parser",
        "description": "Read N lines like `LEVEL:message`. Print only the ERROR messages (without the `ERROR:` prefix), one per line.",
        "difficulty": 2,
        "tags": ["python", "pro", "strings"],
        "xp_reward": 40,
        "examples_json": [{"input": "3\nINFO:started\nERROR:bad input\nERROR:timeout", "output": "bad input\ntimeout"}],
        "test_cases_json": [
            {"input": "3\nINFO:started\nERROR:bad input\nERROR:timeout\n", "output": "bad input\ntimeout"},
            {"input": "2\nINFO:ok\nINFO:done\n", "output": ""},
        ],
        "starter_code_json": {"python": "n = int(input())\nfor _ in range(n):\n    line = input()\n    # filter and print\n"},
        "hints_json": [{"level": 1, "text": "`if line.startswith('ERROR:'): print(line[6:])`"}],
    },
]


# =============================================================================
# PROJECTS — roadmap stage builds
# =============================================================================
PYTHON_ROADMAP_PROJECTS: list[tuple] = [
    # (year, title, slug, description, stack, xp_total)
    (1, "Calculator App", "py-calculator",
     "A console calculator with +, -, *, /, %, power. Handles bad input gracefully with try/except.",
     ["python"], 120),
    (1, "Number Guessing Game", "py-number-guess",
     "Pick a random number 1-100. Let the user guess with warmer/colder feedback. Track tries and best score.",
     ["python"], 120),
    (1, "Temperature Converter", "py-temp-converter",
     "Convert between Celsius, Fahrenheit, and Kelvin with a menu-driven CLI.",
     ["python"], 100),
    (1, "To-Do CLI App", "py-todo-cli",
     "Add/list/complete/delete tasks from a terminal. Persist to a JSON file between runs.",
     ["python"], 150),
    (1, "Word Frequency Counter", "py-word-counter",
     "Read a text file, rank the most common words, and print the top 10. Ignore common stopwords.",
     ["python"], 130),
    (1, "CSV Data Reader", "py-csv-reader",
     "Parse a CSV of students, compute class average, top-3, and write a summary CSV.",
     ["python", "csv"], 150),
    (2, "Bank Account System", "py-bank-system",
     "OOP bank with Account, SavingsAccount, and CurrentAccount classes. Supports deposit, withdraw, interest, and transaction history.",
     ["python", "oop"], 200),
    (2, "Library Management", "py-library",
     "Books, members, borrow/return, late fines. Full OOP design with file persistence.",
     ["python", "oop"], 220),
    (2, "Card Game (OOP)", "py-card-game",
     "Deck, Card, Player, Dealer classes. Play a simplified blackjack in the terminal.",
     ["python", "oop"], 200),
    (2, "Weather App (REST)", "py-weather-app",
     "Fetch live weather from a public API, cache results, and display a styled terminal report.",
     ["python", "requests"], 230),
    (2, "News Headline Scraper", "py-news-scraper",
     "Scrape a news site's front page, extract headlines, and save to a dated JSON file.",
     ["python", "beautifulsoup4"], 220),
    (2, "SQLite Expense Tracker", "py-expense-tracker",
     "CLI-based expense tracker backed by SQLite: add, list by category, monthly totals.",
     ["python", "sqlite"], 240),
    (3, "Flask Blog", "py-flask-blog",
     "A real Flask web app: posts, comments, auth, and deployment instructions. Everything from scratch.",
     ["python", "flask", "sqlite"], 350),
    (3, "Pandas Data Report", "py-pandas-report",
     "Load a messy CSV, clean it, compute a report, and export charts with matplotlib/seaborn.",
     ["python", "pandas", "matplotlib"], 320),
    (3, "ML Iris Classifier", "py-iris-classifier",
     "Train a scikit-learn classifier on the iris dataset and expose it as a tiny Flask API.",
     ["python", "sklearn", "flask"], 350),
    (3, "Email Digest Automator", "py-email-digest",
     "A scheduled script that scrapes news, composes a HTML digest, and emails it via SMTP every morning.",
     ["python", "smtplib", "schedule"], 340),
    (4, "Full-stack Django + React", "py-django-react",
     "Capstone: Django REST backend with JWT auth + a React frontend. Deployed with Docker.",
     ["python", "django", "react", "docker"], 600),
    (4, "ML Model as an API", "py-ml-api",
     "Train any sklearn/torch model, wrap it in FastAPI, deploy, and call it from a tiny web page.",
     ["python", "fastapi", "sklearn"], 550),
    (4, "Open-source Contribution", "py-oss-contrib",
     "Find a real Python open-source project, fix a good-first-issue, and merge a PR. Document the process.",
     ["python", "git"], 500),
    (4, "Publish a PyPI Package", "py-pypi-package",
     "Turn one of your utilities into a proper Python package with pyproject.toml, tests, and a published release on PyPI.",
     ["python", "pypi"], 550),
]
