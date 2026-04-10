"""Real story-mode lessons for multiple tracks.

Each lesson has hook_story, aha_moment, concept_explained, code_walkthrough,
common_mistakes, and quiz — the same shape the frontend LessonStory component
renders. Grouped by track slug.
"""

LESSONS_BY_TRACK: dict[str, list[dict]] = {
    # =========================================================================
    # PYTHON BASICS (Year 1)
    # =========================================================================
    "python-basics": [
        {
            "title": "Variables: boxes with labels",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 6,
            "content_json": {
                "hook_story": (
                    "Imagine a shelf of labeled boxes. Each box can hold one thing — "
                    "a number, a name, a list. The label is how you remember which "
                    "box holds what. In Python, variables are exactly that: labels "
                    "attached to values in memory."
                ),
                "aha_moment": "Variables aren't containers — they're names pointing at values.",
                "concept_explained": (
                    "When you write `age = 21`, Python creates the integer 21 somewhere "
                    "in memory and then sticks the label `age` onto it. Reassigning "
                    "`age = 22` doesn't modify the 21 — it just moves the label."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "Create a variable", "code": "age = 21"},
                    {"step": 2, "comment": "Use it", "code": "print(f'Hi, I am {age}')"},
                    {"step": 3, "comment": "Reassign", "code": "age = age + 1\nprint(age)  # 22"},
                ],
                "common_mistakes": [
                    "Using a variable before assigning it (NameError).",
                    "Thinking `=` means equality — it means assignment.",
                ],
                "quiz": [
                    {
                        "question": "What does `x = 5; y = x; x = 10` print for y?",
                        "options": ["5", "10", "None", "Error"],
                        "correct": "5",
                        "explanation": "y was bound to the value 5. Rebinding x doesn't affect y.",
                    }
                ],
            },
        },
        {
            "title": "Loops: the 'do it again' instruction",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "You're making 30 cups of chai. You don't write 30 identical "
                    "instructions — you write one, then tell yourself 'do this 30 times'. "
                    "That's a loop."
                ),
                "aha_moment": "A loop is just 'do the same thing, but with a changing input.'",
                "concept_explained": (
                    "Python has two main loops: `for` when you know how many times "
                    "or have something to walk over, and `while` when you're waiting "
                    "for a condition to flip."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "For loop over a range", "code": "for i in range(5):\n    print(i)"},
                    {"step": 2, "comment": "For loop over a list", "code": "names = ['Suhana', 'Arjun']\nfor name in names:\n    print(f'Hi {name}')"},
                    {"step": 3, "comment": "While loop", "code": "count = 10\nwhile count > 0:\n    print(count)\n    count -= 1"},
                ],
                "common_mistakes": [
                    "Forgetting to update the loop variable → infinite while loop.",
                    "Off-by-one: `range(1, 10)` goes 1..9, not 1..10.",
                ],
                "quiz": [
                    {
                        "question": "How many times does `for i in range(3, 7): pass` run?",
                        "options": ["3", "4", "5", "7"],
                        "correct": "4",
                        "explanation": "range(3, 7) yields 3, 4, 5, 6 — four values.",
                    }
                ],
            },
        },
        {
            "title": "Functions: teach Python a verb",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "You're tired of writing the same greeting 20 times. What if you "
                    "could teach Python a new verb like `greet(name)` — and it just "
                    "works? That's a function."
                ),
                "aha_moment": "Functions let you name a recipe once and run it anywhere.",
                "concept_explained": (
                    "A function has a name, takes inputs (parameters), runs some code, "
                    "and optionally returns a value. If you don't return anything, "
                    "Python silently returns None."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "Define", "code": "def greet(name):\n    return f'Hi {name}!'"},
                    {"step": 2, "comment": "Call", "code": "msg = greet('Suhana')\nprint(msg)"},
                ],
                "common_mistakes": [
                    "Forgetting `return` — the caller gets None.",
                    "Reusing a built-in name like `list` or `sum` as a parameter name.",
                ],
                "quiz": [
                    {
                        "question": "What does `def f(x): x + 1` return when called with 5?",
                        "options": ["6", "5", "None", "Error"],
                        "correct": "None",
                        "explanation": "No return statement means Python returns None.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # DSA FOUNDATIONS (Year 1)
    # =========================================================================
    "dsa-foundations": [
        {
            "title": "What is an Array, really?",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": "Imagine a row of lockers at a gym — each locker has a number, each holds one item. That's an array.",
                "aha_moment": "An array trades flexibility for speed: you can reach any element in O(1) if you know its index.",
                "concept_explained": "Arrays store elements in contiguous memory. Index = direct offset from the base address.",
                "code_walkthrough": [
                    {"step": 1, "comment": "Declare an array", "code": "nums = [3, 1, 4, 1, 5, 9]"},
                    {"step": 2, "comment": "Access by index", "code": "print(nums[2])  # 4"},
                    {"step": 3, "comment": "Update", "code": "nums[0] = 99"},
                ],
                "common_mistakes": [
                    "Confusing size (len) with last index (len - 1).",
                    "Modifying a list while iterating over it.",
                ],
                "quiz": [
                    {
                        "question": "Time complexity of accessing nums[i]?",
                        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                        "correct": "O(1)",
                        "explanation": "Direct memory offset.",
                    }
                ],
            },
        },
        {
            "title": "Two Pointers: the secret weapon",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": "Two kids start at opposite ends of a rope and walk toward each other. Where do they meet?",
                "aha_moment": "Instead of nested loops (O(n²)), two pointers walk the array once — O(n).",
                "concept_explained": "Use left and right pointers. Move them based on a condition. Perfect for sorted arrays and palindrome checks.",
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Classic: find two numbers that sum to target",
                        "code": (
                            "l, r = 0, len(nums) - 1\n"
                            "while l < r:\n"
                            "    s = nums[l] + nums[r]\n"
                            "    if s == target: return [l, r]\n"
                            "    if s < target: l += 1\n"
                            "    else: r -= 1"
                        ),
                    }
                ],
                "common_mistakes": ["Forgetting `l < r` (infinite loop)."],
                "quiz": [
                    {
                        "question": "Two-pointer works best on which kind of array?",
                        "options": ["Unsorted", "Sorted", "Empty", "Nested"],
                        "correct": "Sorted",
                        "explanation": "Sorted order lets you shrink the search space correctly.",
                    }
                ],
            },
        },
        {
            "title": "Sliding Window: one pass, many answers",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": "You're reading a 500-page book but only care about 20 consecutive pages at a time. Slide your bookmark — never reread.",
                "aha_moment": "Expand the right, shrink the left, track the best window seen so far.",
                "concept_explained": "Sliding window avoids recomputing overlapping subarrays. Maintain a running state as the window moves.",
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Longest substring without repeating chars",
                        "code": (
                            "seen = {}\n"
                            "left = best = 0\n"
                            "for right, c in enumerate(s):\n"
                            "    if c in seen and seen[c] >= left:\n"
                            "        left = seen[c] + 1\n"
                            "    seen[c] = right\n"
                            "    best = max(best, right - left + 1)"
                        ),
                    }
                ],
                "common_mistakes": ["Forgetting to shrink the window when the constraint breaks."],
                "quiz": [
                    {
                        "question": "Sliding window runs in what time?",
                        "options": ["O(n²)", "O(n log n)", "O(n)", "O(1)"],
                        "correct": "O(n)",
                        "explanation": "Each element enters and leaves the window at most once.",
                    }
                ],
            },
        },
        {
            "title": "Binary Search: cut it in half",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "You're looking for the word 'python' in a physical dictionary. "
                    "You don't start at 'A'. You open roughly to the middle — 'M' — "
                    "and realize you went too far. You jump back half. Then half again. "
                    "Six jumps later, you're there."
                ),
                "aha_moment": "Every comparison eliminates half the remaining choices.",
                "concept_explained": (
                    "Binary search requires a sorted array. At each step, compare the "
                    "middle element to the target; move low or high accordingly. "
                    "O(log n) because the search space halves each iteration."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Classic iterative binary search",
                        "code": (
                            "def bs(nums, target):\n"
                            "    lo, hi = 0, len(nums) - 1\n"
                            "    while lo <= hi:\n"
                            "        mid = (lo + hi) // 2\n"
                            "        if nums[mid] == target:\n"
                            "            return mid\n"
                            "        if nums[mid] < target:\n"
                            "            lo = mid + 1\n"
                            "        else:\n"
                            "            hi = mid - 1\n"
                            "    return -1"
                        ),
                    }
                ],
                "common_mistakes": [
                    "Using `while lo < hi` when you meant `<=` — off by one.",
                    "Computing mid as `(lo + hi) // 2` in languages with overflow — prefer `lo + (hi - lo) // 2`.",
                ],
                "quiz": [
                    {
                        "question": "Binary search on n elements takes at most how many comparisons?",
                        "options": ["n", "n/2", "log₂(n)", "√n"],
                        "correct": "log₂(n)",
                        "explanation": "The search space halves each step.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # FULL STACK REACT (Year 2)
    # =========================================================================
    "full-stack-react": [
        {
            "title": "Components: LEGO blocks for UIs",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "You build a LEGO castle by snapping together smaller blocks — "
                    "wall pieces, turret pieces, windows. React works the same way: "
                    "every screen is built by nesting small, reusable components."
                ),
                "aha_moment": "A component is a function that returns UI. That's it.",
                "concept_explained": (
                    "React components are JavaScript functions that return JSX "
                    "(HTML-like syntax). Props are how you pass data into a component — "
                    "think of them as the component's function arguments."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "A tiny component",
                        "code": "function Greeting({ name }) {\n  return <h1>Hi {name}</h1>;\n}",
                    },
                    {
                        "step": 2,
                        "comment": "Use it",
                        "code": "<Greeting name='Suhana' />",
                    },
                ],
                "common_mistakes": [
                    "Lowercase component names — React treats those as HTML tags.",
                    "Mutating props inside a child component.",
                ],
                "quiz": [
                    {
                        "question": "What does a React component return?",
                        "options": ["HTML string", "JSX", "JSON", "CSS"],
                        "correct": "JSX",
                        "explanation": "JSX compiles to React.createElement() calls.",
                    }
                ],
            },
        },
        {
            "title": "useState: React's memory",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "A vending machine needs to remember how many coins you've put in "
                    "between clicks. Without memory, every click starts over. "
                    "useState gives your component that memory."
                ),
                "aha_moment": "useState survives between renders. Regular variables don't.",
                "concept_explained": (
                    "useState returns a pair: the current value and a setter. "
                    "Calling the setter tells React: 'something changed — re-render me.' "
                    "React then calls your component function again with the new value."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Import",
                        "code": "import { useState } from 'react';",
                    },
                    {
                        "step": 2,
                        "comment": "Counter",
                        "code": (
                            "function Counter() {\n"
                            "  const [count, setCount] = useState(0);\n"
                            "  return <button onClick={() => setCount(count + 1)}>{count}</button>;\n"
                            "}"
                        ),
                    },
                ],
                "common_mistakes": [
                    "Mutating state directly (e.g. `arr.push(x)`) — always create a new array.",
                    "Reading state immediately after setting — setters are async.",
                ],
                "quiz": [
                    {
                        "question": "What does useState(0) return?",
                        "options": ["0", "[0, setter]", "{value:0}", "undefined"],
                        "correct": "[0, setter]",
                        "explanation": "An array: [currentValue, setterFunction].",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # DBMS + SQL (Year 2)
    # =========================================================================
    "dbms-sql": [
        {
            "title": "SELECT: asking a question in SQL",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "Imagine walking into a library with a billion books. Instead of "
                    "finding each one manually, you tell a librarian exactly what you "
                    "want: 'Give me every book by Kalki Krishnamurthy, sorted by year.' "
                    "SELECT is that sentence, in SQL."
                ),
                "aha_moment": "SQL is declarative: you say WHAT you want, not HOW to find it.",
                "concept_explained": (
                    "Every query has a shape: SELECT columns FROM table WHERE condition "
                    "ORDER BY column. The database's query planner figures out the fastest "
                    "way to get you those rows."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Basic select",
                        "code": "SELECT name, year FROM students WHERE branch = 'CSE';",
                    },
                    {
                        "step": 2,
                        "comment": "Sort and limit",
                        "code": "SELECT name FROM students ORDER BY xp DESC LIMIT 10;",
                    },
                ],
                "common_mistakes": [
                    "Using `*` everywhere — slower, and fragile to schema changes.",
                    "Forgetting that string comparisons are case-sensitive in some databases.",
                ],
                "quiz": [
                    {
                        "question": "What does LIMIT 5 do?",
                        "options": ["Skips 5 rows", "Returns at most 5 rows", "Groups by 5", "Errors"],
                        "correct": "Returns at most 5 rows",
                        "explanation": "LIMIT caps the number of rows returned.",
                    }
                ],
            },
        },
        {
            "title": "JOIN: stitching tables together",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": (
                    "You have one file of students and another of grades. Neither alone "
                    "tells you 'who scored what'. You need to match them by student_id. "
                    "That's a JOIN."
                ),
                "aha_moment": "A JOIN lets you ask questions across tables that share a key.",
                "concept_explained": (
                    "INNER JOIN keeps only rows that match on both sides. LEFT JOIN keeps "
                    "every row from the left table even if there's no match. The 'ON' "
                    "clause tells SQL which column connects them."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Inner join",
                        "code": (
                            "SELECT s.name, g.marks\n"
                            "FROM students s\n"
                            "INNER JOIN grades g ON s.id = g.student_id;"
                        ),
                    }
                ],
                "common_mistakes": [
                    "Forgetting the ON clause — you get a Cartesian product (billions of rows).",
                    "Mixing up INNER vs LEFT when you want to include students with no grades.",
                ],
                "quiz": [
                    {
                        "question": "What happens with an INNER JOIN when a student has no grade row?",
                        "options": [
                            "The student still appears",
                            "The student is excluded",
                            "NULL fills in",
                            "Error",
                        ],
                        "correct": "The student is excluded",
                        "explanation": "INNER JOIN only keeps rows with matches on both sides.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # OPERATING SYSTEMS (Year 2)
    # =========================================================================
    "operating-systems": [
        {
            "title": "Process vs Thread: the restaurant analogy",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "A restaurant is a process: it has its own kitchen, own staff, own "
                    "cash register. Two restaurants are isolated — one running out of "
                    "tomatoes doesn't affect the other. Threads are the cooks inside one "
                    "restaurant: they share the same kitchen (memory) but work on "
                    "different orders in parallel."
                ),
                "aha_moment": "Threads share memory; processes don't.",
                "concept_explained": (
                    "A process has its own address space, file descriptors, and resources. "
                    "Creating one is expensive. Threads live inside a process and share its "
                    "memory — cheaper to create and faster to communicate, but "
                    "synchronization becomes your problem."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Spawning a thread (Python)",
                        "code": (
                            "import threading\n"
                            "def work(): print('hi from thread')\n"
                            "t = threading.Thread(target=work)\n"
                            "t.start()\n"
                            "t.join()"
                        ),
                    }
                ],
                "common_mistakes": [
                    "Assuming thread-safe = lock-free. It's not.",
                    "Forgetting that Python's GIL limits true CPU parallelism in threads.",
                ],
                "quiz": [
                    {
                        "question": "Which statement is true?",
                        "options": [
                            "Threads have separate memory spaces",
                            "Processes share memory by default",
                            "Threads share the same memory space within a process",
                            "Processes are always faster than threads",
                        ],
                        "correct": "Threads share the same memory space within a process",
                        "explanation": "That's the defining difference.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # C FUNDAMENTALS (Year 1)
    # =========================================================================
    "c-fundamentals": [
        {
            "title": "Pointers: addresses, not values",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": (
                    "Imagine you want to tell a friend where you keep your house key. "
                    "You could move the key to their pocket (copy the value), or you "
                    "could just tell them 'it's in the third drawer of the kitchen cabinet' "
                    "(give them the address). A pointer is the second option."
                ),
                "aha_moment": "A pointer stores the address of a value, not the value itself.",
                "concept_explained": (
                    "In C, every variable lives at some memory address. `&x` gives you "
                    "that address. A pointer variable (`int *p`) is a box designed to "
                    "hold an address. `*p` means 'go look at whatever this address points to'."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "Declare and take address", "code": "int x = 42;\nint *p = &x;"},
                    {"step": 2, "comment": "Dereference", "code": "printf(\"%d\", *p);  // 42"},
                    {"step": 3, "comment": "Modify through pointer", "code": "*p = 99;\nprintf(\"%d\", x);  // 99"},
                ],
                "common_mistakes": [
                    "Dereferencing a NULL or uninitialized pointer — segfault.",
                    "Confusing `int *p, q;` — only `p` is a pointer here, `q` is an int.",
                ],
                "quiz": [
                    {
                        "question": "What does `*p = 10` do if `p` points to x?",
                        "options": ["Sets p to 10", "Sets x to 10", "Error", "Nothing"],
                        "correct": "Sets x to 10",
                        "explanation": "Dereferencing then assigning modifies the pointed-to variable.",
                    }
                ],
            },
        },
        {
            "title": "malloc and free: you own the memory now",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": (
                    "Local variables live on the stack — they vanish when the function "
                    "returns. If you want something to outlive its creator, you ask the "
                    "heap: 'give me 100 bytes.' That's malloc. And since C has no garbage "
                    "collector, when you're done, you clean up yourself with free."
                ),
                "aha_moment": "Every malloc needs exactly one matching free — otherwise, memory leak.",
                "concept_explained": (
                    "malloc returns a void pointer to a chunk of uninitialized heap memory. "
                    "Cast it to the type you need. When you're done, call free() on that "
                    "same pointer. Double-free or use-after-free are undefined behavior."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Allocate an array of 10 ints",
                        "code": "int *arr = (int*)malloc(10 * sizeof(int));\nif (!arr) return -1;",
                    },
                    {"step": 2, "comment": "Use it", "code": "for (int i = 0; i < 10; i++) arr[i] = i * i;"},
                    {"step": 3, "comment": "Clean up", "code": "free(arr);\narr = NULL;"},
                ],
                "common_mistakes": [
                    "Forgetting to check if malloc returned NULL.",
                    "Freeing the same pointer twice.",
                    "Returning a pointer to a local stack variable.",
                ],
                "quiz": [
                    {
                        "question": "What happens if you free(ptr) twice?",
                        "options": ["Nothing", "Undefined behavior", "It errors cleanly", "Memory is freed twice"],
                        "correct": "Undefined behavior",
                        "explanation": "Double-free is a classic source of crashes and security bugs.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # MATH FOR CS (Year 1)
    # =========================================================================
    "math-for-cs": [
        {
            "title": "Big-O: counting without counting",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "You have two routes to your cousin's wedding: one takes exactly 3 hours, "
                    "the other takes 'about 3 hours, plus a little for traffic, plus 10 minutes "
                    "for lunch'. For planning, both are 'roughly 3 hours'. Big-O is that 'roughly' "
                    "for algorithms."
                ),
                "aha_moment": "Big-O ignores constants and lower-order terms — only the dominant growth matters.",
                "concept_explained": (
                    "Big-O notation describes how an algorithm's runtime grows as input size grows. "
                    "O(1) = constant, O(log n) = halving, O(n) = proportional, O(n log n) = sorting, "
                    "O(n^2) = nested loops, O(2^n) = exponential (brute force)."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "O(1) direct access", "code": "return arr[5]"},
                    {"step": 2, "comment": "O(n) linear scan", "code": "for x in arr: print(x)"},
                    {"step": 3, "comment": "O(n^2) nested loop", "code": "for i in arr:\n  for j in arr:\n    ..."},
                ],
                "common_mistakes": [
                    "Thinking O(2n) is different from O(n). It's not — constants drop.",
                    "Mixing up O(log n) and O(n log n).",
                ],
                "quiz": [
                    {
                        "question": "What's the Big-O of accessing a hash map by key?",
                        "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                        "correct": "O(1)",
                        "explanation": "Average-case constant time — that's hash maps' superpower.",
                    }
                ],
            },
        },
        {
            "title": "Modular arithmetic: clock math",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "If it's 10 o'clock and you wait 5 hours, it's 3 — not 15. The clock "
                    "wraps around at 12. That's modular arithmetic. It shows up everywhere "
                    "in CS: hashing, cryptography, cyclic buffers, random number generators."
                ),
                "aha_moment": "Mod is just the remainder after dividing.",
                "concept_explained": (
                    "a mod n gives the remainder when a is divided by n. It's how you map "
                    "infinite integers to a finite set {0, 1, ..., n-1}. Hash tables use it "
                    "to pick a bucket. Clock arithmetic is mod 12 (or mod 24)."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "Python's mod", "code": "print(17 % 5)  # 2"},
                    {"step": 2, "comment": "Wrap a circular buffer", "code": "next_idx = (idx + 1) % size"},
                    {"step": 3, "comment": "Even or odd", "code": "if n % 2 == 0: print('even')"},
                ],
                "common_mistakes": [
                    "Forgetting a % b can be negative in C/Java when a is negative.",
                ],
                "quiz": [
                    {
                        "question": "What is (7 + 5) mod 10?",
                        "options": ["12", "2", "5", "7"],
                        "correct": "2",
                        "explanation": "12 % 10 = 2.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # LINUX & TERMINAL (Year 1)
    # =========================================================================
    "linux-terminal": [
        {
            "title": "The shell: your first superpower",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "Clicking through folders is fine for 10 files. But when a server has "
                    "100,000 log entries to search or 500 files to rename, mousing around "
                    "would take all day. The shell is how you tell the computer 'just do this "
                    "to all of them, now.'"
                ),
                "aha_moment": "Commands chain. Small tools do one thing well; pipes let you combine them.",
                "concept_explained": (
                    "The shell is a text interface to the operating system. Every command "
                    "is a program. The Unix philosophy: write programs that do one thing "
                    "well and compose them with pipes (|) and redirections (>, <)."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "List files", "code": "ls -la"},
                    {"step": 2, "comment": "Find Python files", "code": "find . -name '*.py'"},
                    {"step": 3, "comment": "Count lines", "code": "find . -name '*.py' | xargs wc -l"},
                    {"step": 4, "comment": "Search inside files", "code": "grep -r 'TODO' ."},
                ],
                "common_mistakes": [
                    "rm -rf / — never. Always double-check the path before destructive commands.",
                    "Forgetting quotes around filenames with spaces.",
                ],
                "quiz": [
                    {
                        "question": "What does `cat file.txt | grep 'error' | wc -l` do?",
                        "options": [
                            "Counts all lines",
                            "Counts lines containing 'error'",
                            "Prints errors",
                            "Deletes errors",
                        ],
                        "correct": "Counts lines containing 'error'",
                        "explanation": "cat reads, grep filters, wc -l counts.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # WEB BASICS (Year 1)
    # =========================================================================
    "web-basics": [
        {
            "title": "Semantic HTML: give your tags meaning",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 8,
            "content_json": {
                "hook_story": (
                    "Imagine reading a book where every paragraph, chapter title, and footnote "
                    "looks identical — same font, same size. You'd be lost. HTML tags are how "
                    "you tell the browser, screen readers, and Google what each piece of "
                    "text means: a heading, a navigation link, the main content."
                ),
                "aha_moment": "Use the right tag for the right meaning. <div> is the last resort.",
                "concept_explained": (
                    "Semantic tags like header, nav, main, article, section, footer, button "
                    "communicate structure. Screen readers depend on this. SEO depends on this. "
                    "Future maintenance depends on this."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Bad: divs everywhere",
                        "code": "<div class='header'>\n  <div class='nav'>...</div>\n</div>",
                    },
                    {
                        "step": 2,
                        "comment": "Good: semantic",
                        "code": "<header>\n  <nav>...</nav>\n</header>",
                    },
                ],
                "common_mistakes": [
                    "Using a div with onClick instead of a button — inaccessible.",
                    "Multiple h1 tags on one page.",
                ],
                "quiz": [
                    {
                        "question": "Which is best for a clickable UI element?",
                        "options": ["div onclick", "span onclick", "button", "a href='#'"],
                        "correct": "button",
                        "explanation": "Buttons are keyboard-accessible and screen-reader friendly by default.",
                    }
                ],
            },
        },
        {
            "title": "Flexbox: one axis, infinite layouts",
            "type": "story",
            "xp_reward": 10,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "Before flexbox, centering a div vertically was a meme — you needed "
                    "hacks with negative margins, absolute positioning, and prayer. Flexbox "
                    "turned it into a one-liner: display: flex; justify-content: center; "
                    "align-items: center. The CSS gods finally heard us."
                ),
                "aha_moment": "Flexbox lays things out along one axis and distributes space.",
                "concept_explained": (
                    "Set display: flex on a parent, then use justify-content (main axis) "
                    "and align-items (cross axis) to position children. flex-direction picks "
                    "row or column. gap adds space between items."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Center both axes",
                        "code": ".parent {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}",
                    },
                    {
                        "step": 2,
                        "comment": "Space-between for a nav bar",
                        "code": "nav { display: flex; justify-content: space-between; }",
                    },
                ],
                "common_mistakes": [
                    "Forgetting to set flex on the parent — properties don't do anything on non-flex items.",
                ],
                "quiz": [
                    {
                        "question": "Which property centers items horizontally in a flex row?",
                        "options": ["align-items: center", "justify-content: center", "text-align: center", "margin: auto"],
                        "correct": "justify-content: center",
                        "explanation": "In a row, justify-content controls the main (horizontal) axis.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # COMPUTER NETWORKS (Year 2)
    # =========================================================================
    "computer-networks": [
        {
            "title": "TCP vs UDP: delivery vs speed",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": (
                    "Sending a package by registered post: slower, but guaranteed to arrive "
                    "and with proof of delivery. Sending a postcard: faster, cheaper, but "
                    "might get lost. TCP is registered post. UDP is the postcard."
                ),
                "aha_moment": "TCP guarantees ordered, reliable delivery. UDP is fire-and-forget.",
                "concept_explained": (
                    "TCP: connection-oriented, three-way handshake (SYN, SYN-ACK, ACK), "
                    "retransmits lost packets, keeps them in order. Used by HTTP, SSH, FTP. "
                    "UDP: no handshake, no ordering, no retransmission. Used by video calls, "
                    "DNS queries, online games — where speed matters more than perfect delivery."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Python TCP server",
                        "code": "import socket\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.bind(('0.0.0.0', 8000))\ns.listen()",
                    },
                    {
                        "step": 2,
                        "comment": "Python UDP server",
                        "code": "s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)\ns.bind(('0.0.0.0', 8000))\ndata, addr = s.recvfrom(1024)",
                    },
                ],
                "common_mistakes": [
                    "Assuming UDP delivery order matches send order — it doesn't.",
                    "Using TCP for a real-time game — latency spikes from retransmissions.",
                ],
                "quiz": [
                    {
                        "question": "Which protocol would you pick for a video call?",
                        "options": ["TCP", "UDP", "HTTP", "FTP"],
                        "correct": "UDP",
                        "explanation": "A dropped video frame is fine; a 500ms TCP retransmit is not.",
                    }
                ],
            },
        },
        {
            "title": "HTTP: the web's vocabulary",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "Every time you load a webpage, your browser is having a tiny conversation "
                    "with a server. 'GET /index.html please.' 'Here you go. 200 OK.' HTTP is "
                    "the language that conversation happens in."
                ),
                "aha_moment": "HTTP is stateless: every request stands on its own, the server remembers nothing between requests.",
                "concept_explained": (
                    "HTTP is a request/response protocol. A request has a method (GET, POST, "
                    "PUT, DELETE), a path, headers, and optionally a body. A response has a "
                    "status code (200 OK, 404 Not Found, 500 Server Error), headers, and a body."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Raw GET request",
                        "code": "GET /api/users HTTP/1.1\nHost: techpath.dev\nAccept: application/json",
                    },
                    {
                        "step": 2,
                        "comment": "Response",
                        "code": "HTTP/1.1 200 OK\nContent-Type: application/json\n\n{\"users\": []}",
                    },
                ],
                "common_mistakes": [
                    "Using GET to modify data — GETs should be safe and idempotent.",
                    "Confusing 401 (not authenticated) with 403 (authenticated but forbidden).",
                ],
                "quiz": [
                    {
                        "question": "Which HTTP status code means 'you're authenticated but not allowed'?",
                        "options": ["400", "401", "403", "404"],
                        "correct": "403",
                        "explanation": "401 = not authenticated. 403 = authenticated but forbidden.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # DSA INTERMEDIATE (Year 2)
    # =========================================================================
    "dsa-intermediate": [
        {
            "title": "Hash maps: the O(1) lookup cheat code",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "You have a dictionary with 100,000 words. Finding 'python' by flipping "
                    "pages one by one would take forever. But the dictionary is alphabetized — "
                    "you jump to the P section instantly. A hash map is the same idea, but the "
                    "jump is computed from the word itself via a hash function."
                ),
                "aha_moment": "A hash function turns any key into an array index — lookup becomes O(1).",
                "concept_explained": (
                    "Hash maps store key-value pairs. Given a key, a hash function computes "
                    "an integer, which is modded by the array size to get a bucket. Collisions "
                    "(two keys landing in the same bucket) are handled with chaining or open "
                    "addressing. Average-case O(1) for get, put, and delete."
                ),
                "code_walkthrough": [
                    {"step": 1, "comment": "Python dict", "code": "counts = {}\ncounts['apple'] = 3"},
                    {
                        "step": 2,
                        "comment": "Count occurrences",
                        "code": "for word in text.split():\n    counts[word] = counts.get(word, 0) + 1",
                    },
                    {
                        "step": 3,
                        "comment": "Use in a problem (two sum)",
                        "code": "seen = {}\nfor i, n in enumerate(nums):\n    if target - n in seen:\n        return [seen[target - n], i]\n    seen[n] = i",
                    },
                ],
                "common_mistakes": [
                    "Using mutable objects (lists) as keys — they can't be hashed.",
                    "Assuming worst-case O(1). Bad hash functions give O(n).",
                ],
                "quiz": [
                    {
                        "question": "What's the average time for a hash map lookup?",
                        "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                        "correct": "O(1)",
                        "explanation": "With a good hash function and low load factor.",
                    }
                ],
            },
        },
        {
            "title": "BFS: concentric circles",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 12,
            "content_json": {
                "hook_story": (
                    "Throw a stone into a pond. Ripples spread outward in circles — first the "
                    "inner ring, then the next, then the next. Breadth-first search explores "
                    "a graph exactly like that: all nodes at distance 1, then all at distance "
                    "2, and so on."
                ),
                "aha_moment": "BFS finds the shortest path in an unweighted graph — always.",
                "concept_explained": (
                    "BFS uses a queue. Start with the source, mark it visited, enqueue its "
                    "neighbors. Dequeue the next node, enqueue its unvisited neighbors, and "
                    "repeat. Because you process layer by layer, the first time you reach any "
                    "node is via the shortest path."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "BFS template",
                        "code": (
                            "from collections import deque\n"
                            "def bfs(graph, start):\n"
                            "    visited = {start}\n"
                            "    queue = deque([start])\n"
                            "    while queue:\n"
                            "        node = queue.popleft()\n"
                            "        for nxt in graph[node]:\n"
                            "            if nxt not in visited:\n"
                            "                visited.add(nxt)\n"
                            "                queue.append(nxt)"
                        ),
                    }
                ],
                "common_mistakes": [
                    "Marking a node visited only when you dequeue it — leads to duplicates in the queue.",
                    "Using BFS on a weighted graph expecting shortest paths.",
                ],
                "quiz": [
                    {
                        "question": "Which data structure does BFS use?",
                        "options": ["Stack", "Queue", "Heap", "Set"],
                        "correct": "Queue",
                        "explanation": "FIFO order gives you layer-by-layer traversal.",
                    }
                ],
            },
        },
    ],

    # =========================================================================
    # FULL STACK NODE (Year 2)
    # =========================================================================
    "full-stack-node": [
        {
            "title": "REST: nouns not verbs",
            "type": "story",
            "xp_reward": 15,
            "duration_minutes": 10,
            "content_json": {
                "hook_story": (
                    "Early APIs were wild. Endpoints like /getUser, /createOrder, /deleteProduct "
                    "— every action got its own URL. REST flipped it: URLs name things (nouns), "
                    "HTTP methods describe actions (verbs). Fewer endpoints, consistent pattern."
                ),
                "aha_moment": "In REST, the URL says what, the method says how.",
                "concept_explained": (
                    "A REST resource has a plural URL like /users. GET /users lists them. "
                    "GET /users/123 fetches one. POST /users creates. PUT /users/123 replaces. "
                    "DELETE /users/123 removes. Predictable, composable, cacheable."
                ),
                "code_walkthrough": [
                    {
                        "step": 1,
                        "comment": "Express router",
                        "code": (
                            "router.get('/users', listUsers);\n"
                            "router.get('/users/:id', getUser);\n"
                            "router.post('/users', createUser);\n"
                            "router.put('/users/:id', updateUser);\n"
                            "router.delete('/users/:id', deleteUser);"
                        ),
                    }
                ],
                "common_mistakes": [
                    "Using GET /deleteUser?id=5 — GETs should never modify data.",
                    "Putting verbs in URLs: /users/create instead of POST /users.",
                ],
                "quiz": [
                    {
                        "question": "Which method should create a new resource?",
                        "options": ["GET", "POST", "PUT", "DELETE"],
                        "correct": "POST",
                        "explanation": "POST to a collection creates a new member.",
                    }
                ],
            },
        },
    ],
}
