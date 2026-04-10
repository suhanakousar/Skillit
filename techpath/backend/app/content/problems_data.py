"""Real problem content for TechPath seed.

50+ problems across arrays, strings, two-pointers, sliding window, binary search,
trees, graphs, DP, stacks, queues, and hashing. Each has real test cases written
against simple stdin/stdout formats so Judge0 can validate them.
"""

PROBLEMS: list[dict] = [
    # =========================================================================
    # ARRAYS (difficulty 1-3)
    # =========================================================================
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "description": (
            "Given an array of integers `nums` and an integer `target`, return the "
            "indices of the two numbers that add up to `target`. You may assume exactly "
            "one solution exists, and you may not use the same element twice."
        ),
        "difficulty": 1,
        "tags": ["arrays", "hashing"],
        "xp_reward": 20,
        "examples_json": [
            {"input": "nums=[2,7,11,15], target=9", "output": "[0,1]"},
            {"input": "nums=[3,2,4], target=6", "output": "[1,2]"},
        ],
        "constraints_text": "2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9",
        "test_cases_json": [
            {"input": "4\n2 7 11 15\n9\n", "output": "0 1"},
            {"input": "3\n3 2 4\n6\n", "output": "1 2"},
            {"input": "2\n3 3\n6\n", "output": "0 1"},
        ],
        "starter_code_json": {
            "python": (
                "def two_sum(nums, target):\n"
                "    seen = {}\n"
                "    # your code\n"
                "    return [-1, -1]\n\n"
                "n = int(input())\n"
                "nums = list(map(int, input().split()))\n"
                "target = int(input())\n"
                "print(*two_sum(nums, target))\n"
            ),
            "cpp": (
                "#include <bits/stdc++.h>\n"
                "using namespace std;\n"
                "int main(){ int n; cin>>n; vector<int> a(n); "
                "for(auto& x: a) cin>>x; int t; cin>>t; /* TODO */ return 0; }\n"
            ),
            "java": (
                "import java.util.*;\n"
                "public class Main {\n"
                "    public static void main(String[] args) {\n"
                "        Scanner sc = new Scanner(System.in);\n"
                "        int n = sc.nextInt();\n"
                "        int[] a = new int[n];\n"
                "        for (int i = 0; i < n; i++) a[i] = sc.nextInt();\n"
                "        int t = sc.nextInt();\n"
                "        // TODO\n"
                "    }\n"
                "}\n"
            ),
        },
        "hints_json": [
            {"level": 1, "text": "Do you really need two nested loops?"},
            {"level": 2, "text": "A hash map remembers what you've already seen."},
            {"level": 3, "text": "For each num, check if (target - num) is already in the map."},
        ],
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "description": "Return true if any value appears at least twice in the array, false otherwise.",
        "difficulty": 1,
        "tags": ["arrays", "hashing"],
        "xp_reward": 20,
        "examples_json": [{"input": "[1,2,3,1]", "output": "true"}],
        "test_cases_json": [
            {"input": "4\n1 2 3 1\n", "output": "true"},
            {"input": "4\n1 2 3 4\n", "output": "false"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "A set is perfect for 'have I seen this before?'"}],
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-buy-sell-stock",
        "description": "Given prices on each day, find the max profit from one buy and one later sell.",
        "difficulty": 2,
        "tags": ["arrays", "dp"],
        "xp_reward": 40,
        "examples_json": [{"input": "[7,1,5,3,6,4]", "output": "5"}],
        "test_cases_json": [
            {"input": "6\n7 1 5 3 6 4\n", "output": "5"},
            {"input": "5\n7 6 4 3 1\n", "output": "0"},
        ],
        "starter_code_json": {"python": "n = int(input())\nprices = list(map(int, input().split()))\n"},
        "hints_json": [
            {"level": 1, "text": "One pass. Track the minimum price so far."},
            {"level": 2, "text": "At each day: best profit = max(best, price - min_so_far)."},
        ],
    },
    {
        "title": "Maximum Subarray (Kadane)",
        "slug": "maximum-subarray",
        "description": "Find the contiguous subarray with the largest sum.",
        "difficulty": 3,
        "tags": ["arrays", "dp"],
        "xp_reward": 50,
        "examples_json": [{"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"}],
        "test_cases_json": [
            {"input": "9\n-2 1 -3 4 -1 2 1 -5 4\n", "output": "6"},
            {"input": "1\n1\n", "output": "1"},
            {"input": "5\n5 4 -1 7 8\n", "output": "23"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [
            {"level": 1, "text": "At each index, either start fresh or extend the previous subarray."},
            {"level": 2, "text": "current = max(num, current + num); best = max(best, current)."},
        ],
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-except-self",
        "description": "Return an array where output[i] = product of all elements except nums[i]. No division.",
        "difficulty": 3,
        "tags": ["arrays", "prefix"],
        "xp_reward": 50,
        "examples_json": [{"input": "[1,2,3,4]", "output": "[24,12,8,6]"}],
        "test_cases_json": [{"input": "4\n1 2 3 4\n", "output": "24 12 8 6"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Two passes: prefix products, then suffix products."}],
    },
    {
        "title": "Rotate Array",
        "slug": "rotate-array",
        "description": "Rotate the array to the right by k steps.",
        "difficulty": 2,
        "tags": ["arrays"],
        "xp_reward": 40,
        "examples_json": [{"input": "nums=[1,2,3,4,5,6,7], k=3", "output": "[5,6,7,1,2,3,4]"}],
        "test_cases_json": [{"input": "7\n1 2 3 4 5 6 7\n3\n", "output": "5 6 7 1 2 3 4"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\nk = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Reverse all, reverse first k, reverse the rest."}],
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "description": "Merge all overlapping intervals.",
        "difficulty": 3,
        "tags": ["arrays", "sorting"],
        "xp_reward": 50,
        "examples_json": [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"}],
        "test_cases_json": [{"input": "4\n1 3\n2 6\n8 10\n15 18\n", "output": "1 6\n8 10\n15 18"}],
        "starter_code_json": {"python": "n = int(input())\nivs = [list(map(int, input().split())) for _ in range(n)]\n"},
        "hints_json": [{"level": 1, "text": "Sort by start. Walk once and extend the current interval."}],
    },
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "description": "Move all zeroes to the end while maintaining the order of non-zero elements. In place.",
        "difficulty": 1,
        "tags": ["arrays", "two-pointers"],
        "xp_reward": 20,
        "examples_json": [{"input": "[0,1,0,3,12]", "output": "[1,3,12,0,0]"}],
        "test_cases_json": [{"input": "5\n0 1 0 3 12\n", "output": "1 3 12 0 0"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Two pointers: write index and read index."}],
    },

    # =========================================================================
    # STRINGS
    # =========================================================================
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "description": "Given a string containing `()[]{}`, return true if the input is valid.",
        "difficulty": 1,
        "tags": ["strings", "stack"],
        "xp_reward": 20,
        "examples_json": [{"input": "()[]{}", "output": "true"}, {"input": "(]", "output": "false"}],
        "test_cases_json": [
            {"input": "()[]{}\n", "output": "true"},
            {"input": "(]\n", "output": "false"},
            {"input": "((())\n", "output": "false"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [
            {"level": 1, "text": "What data structure matches 'last in, first out'?"},
            {"level": 2, "text": "Push open brackets; on close, pop and compare."},
        ],
    },
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "description": "Given two strings s and t, return true if t is an anagram of s.",
        "difficulty": 1,
        "tags": ["strings", "hashing"],
        "xp_reward": 20,
        "examples_json": [{"input": "s=anagram, t=nagaram", "output": "true"}],
        "test_cases_json": [
            {"input": "anagram\nnagaram\n", "output": "true"},
            {"input": "rat\ncar\n", "output": "false"},
        ],
        "starter_code_json": {"python": "s = input()\nt = input()\n"},
        "hints_json": [{"level": 1, "text": "Same multiset of characters? Compare sorted strings or counts."}],
    },
    {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "description": "Considering only alphanumeric characters and ignoring case, is the string a palindrome?",
        "difficulty": 1,
        "tags": ["strings", "two-pointers"],
        "xp_reward": 20,
        "examples_json": [{"input": "A man, a plan, a canal: Panama", "output": "true"}],
        "test_cases_json": [
            {"input": "A man a plan a canal Panama\n", "output": "true"},
            {"input": "race a car\n", "output": "false"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [{"level": 1, "text": "Two pointers from each end, skipping non-alphanumerics."}],
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-no-repeat",
        "description": "Find the length of the longest substring without repeating characters.",
        "difficulty": 3,
        "tags": ["strings", "sliding-window", "hashing"],
        "xp_reward": 50,
        "examples_json": [{"input": "abcabcbb", "output": "3"}],
        "test_cases_json": [
            {"input": "abcabcbb\n", "output": "3"},
            {"input": "bbbbb\n", "output": "1"},
            {"input": "pwwkew\n", "output": "3"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [
            {"level": 1, "text": "Move a window. Shrink it when you hit a duplicate."},
            {"level": 2, "text": "Track the last index of each character in a dict."},
        ],
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "description": "Group strings that are anagrams of each other together.",
        "difficulty": 3,
        "tags": ["strings", "hashing"],
        "xp_reward": 50,
        "examples_json": [{"input": "[eat,tea,tan,ate,nat,bat]", "output": "[[eat,tea,ate],[tan,nat],[bat]]"}],
        "test_cases_json": [{"input": "6\neat\ntea\ntan\nate\nnat\nbat\n", "output": "3"}],
        "starter_code_json": {"python": "n = int(input())\nwords = [input() for _ in range(n)]\n"},
        "hints_json": [{"level": 1, "text": "Key each word by its sorted form or by a char-count tuple."}],
    },
    {
        "title": "Longest Palindromic Substring",
        "slug": "longest-palindromic-substring",
        "description": "Find the longest palindromic substring.",
        "difficulty": 3,
        "tags": ["strings", "dp"],
        "xp_reward": 50,
        "examples_json": [{"input": "babad", "output": "bab or aba"}],
        "test_cases_json": [
            {"input": "babad\n", "output": "3"},
            {"input": "cbbd\n", "output": "2"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [{"level": 1, "text": "Expand around each center (both odd and even)."}],
    },
    {
        "title": "Reverse a String",
        "slug": "reverse-string",
        "description": "Reverse the given string.",
        "difficulty": 1,
        "tags": ["strings", "two-pointers"],
        "xp_reward": 20,
        "examples_json": [{"input": "hello", "output": "olleh"}],
        "test_cases_json": [
            {"input": "hello\n", "output": "olleh"},
            {"input": "techpath\n", "output": "htaphcet"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [{"level": 1, "text": "Two pointers, swap inward."}],
    },
    {
        "title": "First Unique Character",
        "slug": "first-unique-character",
        "description": "Return the index of the first non-repeating character in a string, or -1.",
        "difficulty": 1,
        "tags": ["strings", "hashing"],
        "xp_reward": 20,
        "examples_json": [{"input": "leetcode", "output": "0"}],
        "test_cases_json": [
            {"input": "leetcode\n", "output": "0"},
            {"input": "loveleetcode\n", "output": "2"},
            {"input": "aabb\n", "output": "-1"},
        ],
        "starter_code_json": {"python": "s = input()\n"},
        "hints_json": [{"level": 1, "text": "Count occurrences, then walk once."}],
    },

    # =========================================================================
    # BINARY SEARCH
    # =========================================================================
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "description": "Given a sorted array and a target, return the index of target or -1.",
        "difficulty": 1,
        "tags": ["binary-search"],
        "xp_reward": 20,
        "examples_json": [{"input": "nums=[-1,0,3,5,9,12], target=9", "output": "4"}],
        "test_cases_json": [
            {"input": "6\n-1 0 3 5 9 12\n9\n", "output": "4"},
            {"input": "6\n-1 0 3 5 9 12\n2\n", "output": "-1"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\ntarget = int(input())\n"},
        "hints_json": [
            {"level": 1, "text": "Maintain low and high. Compare against nums[mid]."},
        ],
    },
    {
        "title": "Search Insert Position",
        "slug": "search-insert",
        "description": "Return the index where target would be inserted in order.",
        "difficulty": 1,
        "tags": ["binary-search"],
        "xp_reward": 20,
        "examples_json": [{"input": "[1,3,5,6], target=5", "output": "2"}],
        "test_cases_json": [
            {"input": "4\n1 3 5 6\n5\n", "output": "2"},
            {"input": "4\n1 3 5 6\n2\n", "output": "1"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\ntarget = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Lower bound — smallest index where nums[i] >= target."}],
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-rotated",
        "description": "A sorted array is rotated at some unknown pivot. Find target in O(log n).",
        "difficulty": 3,
        "tags": ["binary-search", "arrays"],
        "xp_reward": 50,
        "examples_json": [{"input": "[4,5,6,7,0,1,2], target=0", "output": "4"}],
        "test_cases_json": [
            {"input": "7\n4 5 6 7 0 1 2\n0\n", "output": "4"},
            {"input": "7\n4 5 6 7 0 1 2\n3\n", "output": "-1"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\ntarget = int(input())\n"},
        "hints_json": [
            {"level": 1, "text": "At each mid, one of the halves is sorted — figure out which."},
            {"level": 2, "text": "Check if target lies within the sorted half; move accordingly."},
        ],
    },
    {
        "title": "Koko Eating Bananas",
        "slug": "koko-bananas",
        "description": "Find the minimum integer k such that Koko can eat all piles in h hours (eats at k bananas/hour).",
        "difficulty": 4,
        "tags": ["binary-search"],
        "xp_reward": 80,
        "examples_json": [{"input": "piles=[3,6,7,11], h=8", "output": "4"}],
        "test_cases_json": [{"input": "4\n3 6 7 11\n8\n", "output": "4"}],
        "starter_code_json": {"python": "n = int(input())\npiles = list(map(int, input().split()))\nh = int(input())\n"},
        "hints_json": [
            {"level": 1, "text": "Binary search on the answer (k)."},
            {"level": 2, "text": "For each candidate k, compute hours needed = sum(ceil(p/k))."},
        ],
    },

    # =========================================================================
    # TREES
    # =========================================================================
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "max-depth-bt",
        "description": "Return the max depth of a binary tree (given as level-order array with null for empty).",
        "difficulty": 1,
        "tags": ["trees", "dfs"],
        "xp_reward": 20,
        "examples_json": [{"input": "[3,9,20,null,null,15,7]", "output": "3"}],
        "test_cases_json": [{"input": "1\n3 9 20 # # 15 7\n", "output": "3"}],
        "starter_code_json": {"python": "# helper to parse level-order\n"},
        "hints_json": [{"level": 1, "text": "Recursively: depth = 1 + max(left, right)."}],
    },
    {
        "title": "Invert Binary Tree",
        "slug": "invert-bt",
        "description": "Invert a binary tree — swap left and right at every node.",
        "difficulty": 1,
        "tags": ["trees", "dfs"],
        "xp_reward": 20,
        "examples_json": [{"input": "[4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]"}],
        "test_cases_json": [{"input": "7\n4 2 7 1 3 6 9\n", "output": "4 7 2 9 6 3 1"}],
        "starter_code_json": {"python": "# recursive swap\n"},
        "hints_json": [{"level": 1, "text": "Recurse on each child, then swap."}],
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "bt-level-order",
        "description": "Return the level-by-level traversal of a binary tree.",
        "difficulty": 3,
        "tags": ["trees", "bfs"],
        "xp_reward": 50,
        "examples_json": [{"input": "[3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"}],
        "test_cases_json": [{"input": "7\n3 9 20 # # 15 7\n", "output": "3"}],
        "starter_code_json": {"python": "# use a queue\n"},
        "hints_json": [{"level": 1, "text": "BFS. Track the size of each level before processing."}],
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-bst",
        "description": "Determine if a binary tree is a valid BST.",
        "difficulty": 3,
        "tags": ["trees", "bst", "dfs"],
        "xp_reward": 50,
        "examples_json": [{"input": "[2,1,3]", "output": "true"}],
        "test_cases_json": [{"input": "3\n2 1 3\n", "output": "true"}],
        "starter_code_json": {"python": "# recurse with low/high bounds\n"},
        "hints_json": [{"level": 1, "text": "Pass down min/max bounds as you recurse."}],
    },

    # =========================================================================
    # GRAPHS
    # =========================================================================
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "description": "Given a 2D grid of '1' (land) and '0' (water), count connected islands.",
        "difficulty": 3,
        "tags": ["graphs", "dfs", "bfs"],
        "xp_reward": 50,
        "examples_json": [{"input": "grid=[[1,1,0],[1,0,0],[0,0,1]]", "output": "2"}],
        "test_cases_json": [{"input": "3 3\n110\n100\n001\n", "output": "2"}],
        "starter_code_json": {"python": "r, c = map(int, input().split())\ngrid = [input() for _ in range(r)]\n"},
        "hints_json": [
            {"level": 1, "text": "Flood-fill each '1' and mark visited."},
            {"level": 2, "text": "DFS or BFS from each unvisited land cell; increment counter."},
        ],
    },
    {
        "title": "Clone Graph",
        "slug": "clone-graph",
        "description": "Deep copy a connected undirected graph.",
        "difficulty": 3,
        "tags": ["graphs", "dfs", "hashing"],
        "xp_reward": 50,
        "examples_json": [{"input": "adj=[[2,4],[1,3],[2,4],[1,3]]", "output": "same structure"}],
        "test_cases_json": [{"input": "4\n2 4\n1 3\n2 4\n1 3\n", "output": "4"}],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Keep a dict from original node -> clone node."}],
    },
    {
        "title": "Course Schedule",
        "slug": "course-schedule",
        "description": "Given prerequisites, determine if all courses can be finished (cycle detection).",
        "difficulty": 3,
        "tags": ["graphs", "topo-sort"],
        "xp_reward": 50,
        "examples_json": [{"input": "numCourses=2, prerequisites=[[1,0]]", "output": "true"}],
        "test_cases_json": [
            {"input": "2 1\n1 0\n", "output": "true"},
            {"input": "2 2\n1 0\n0 1\n", "output": "false"},
        ],
        "starter_code_json": {"python": "n, m = map(int, input().split())\n"},
        "hints_json": [
            {"level": 1, "text": "Detect a cycle in the prerequisite graph."},
            {"level": 2, "text": "Kahn's algorithm: process nodes with in-degree 0."},
        ],
    },

    # =========================================================================
    # STACKS, QUEUES, HEAPS
    # =========================================================================
    {
        "title": "Min Stack",
        "slug": "min-stack",
        "description": "Design a stack that supports push, pop, top, and getMin — all in O(1).",
        "difficulty": 2,
        "tags": ["stack", "design"],
        "xp_reward": 40,
        "examples_json": [{"input": "push 3; push 5; getMin; push 2; getMin", "output": "3 2"}],
        "test_cases_json": [{"input": "5\npush 3\npush 5\ngetMin\npush 2\ngetMin\n", "output": "3\n2"}],
        "starter_code_json": {"python": "# maintain a parallel min stack\n"},
        "hints_json": [{"level": 1, "text": "Push the running minimum alongside each value."}],
    },
    {
        "title": "Daily Temperatures",
        "slug": "daily-temperatures",
        "description": "For each day, how many days until a warmer temperature?",
        "difficulty": 3,
        "tags": ["stack", "monotonic-stack"],
        "xp_reward": 50,
        "examples_json": [{"input": "[73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"}],
        "test_cases_json": [{"input": "8\n73 74 75 71 69 72 76 73\n", "output": "1 1 4 2 1 1 0 0"}],
        "starter_code_json": {"python": "n = int(input())\nt = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Monotonic decreasing stack of indices."}],
    },
    {
        "title": "K Closest Points to Origin",
        "slug": "k-closest-points",
        "description": "Return the k closest points to (0, 0) using Euclidean distance.",
        "difficulty": 3,
        "tags": ["heap", "sorting"],
        "xp_reward": 50,
        "examples_json": [{"input": "points=[[1,3],[-2,2]], k=1", "output": "[[-2,2]]"}],
        "test_cases_json": [{"input": "2 1\n1 3\n-2 2\n", "output": "-2 2"}],
        "starter_code_json": {"python": "n, k = map(int, input().split())\n"},
        "hints_json": [{"level": 1, "text": "Max-heap of size k, or sort by distance."}],
    },

    # =========================================================================
    # LINKED LISTS
    # =========================================================================
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "description": "Reverse a singly linked list.",
        "difficulty": 1,
        "tags": ["linked-list"],
        "xp_reward": 20,
        "examples_json": [{"input": "1->2->3->4->5", "output": "5->4->3->2->1"}],
        "test_cases_json": [{"input": "5\n1 2 3 4 5\n", "output": "5 4 3 2 1"}],
        "starter_code_json": {"python": "n = int(input())\nvals = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "prev=None; while curr: next=curr.next; curr.next=prev; prev=curr; curr=next."}],
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "description": "Merge two sorted linked lists into one sorted list.",
        "difficulty": 1,
        "tags": ["linked-list", "two-pointers"],
        "xp_reward": 20,
        "examples_json": [{"input": "[1,2,4], [1,3,4]", "output": "[1,1,2,3,4,4]"}],
        "test_cases_json": [{"input": "3\n1 2 4\n3\n1 3 4\n", "output": "1 1 2 3 4 4"}],
        "starter_code_json": {"python": "a = list(map(int, input().split()))[1:]\nb = list(map(int, input().split()))[1:]\n"},
        "hints_json": [{"level": 1, "text": "Use a dummy head and walk both lists."}],
    },
    {
        "title": "Linked List Cycle",
        "slug": "linked-list-cycle",
        "description": "Detect if a linked list has a cycle.",
        "difficulty": 2,
        "tags": ["linked-list", "two-pointers"],
        "xp_reward": 40,
        "examples_json": [{"input": "list with cycle", "output": "true"}],
        "test_cases_json": [{"input": "4\n3 2 0 -4\n1\n", "output": "true"}],
        "starter_code_json": {"python": "# Floyd's tortoise and hare\n"},
        "hints_json": [{"level": 1, "text": "Slow pointer advances 1, fast advances 2. They meet iff cycle."}],
    },

    # =========================================================================
    # DP
    # =========================================================================
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "description": "You can climb 1 or 2 steps at a time. How many distinct ways to reach step n?",
        "difficulty": 1,
        "tags": ["dp"],
        "xp_reward": 20,
        "examples_json": [{"input": "n=3", "output": "3"}],
        "test_cases_json": [
            {"input": "3\n", "output": "3"},
            {"input": "5\n", "output": "8"},
        ],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "It's Fibonacci: ways(n) = ways(n-1) + ways(n-2)."}],
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "description": "Rob houses to maximize total, but you can't rob two adjacent houses.",
        "difficulty": 2,
        "tags": ["dp"],
        "xp_reward": 40,
        "examples_json": [{"input": "[2,7,9,3,1]", "output": "12"}],
        "test_cases_json": [
            {"input": "5\n2 7 9 3 1\n", "output": "12"},
            {"input": "4\n1 2 3 1\n", "output": "4"},
        ],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "dp[i] = max(dp[i-1], dp[i-2] + nums[i])."}],
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "description": "Fewest coins to make amount. Return -1 if impossible.",
        "difficulty": 3,
        "tags": ["dp"],
        "xp_reward": 50,
        "examples_json": [{"input": "coins=[1,2,5], amount=11", "output": "3"}],
        "test_cases_json": [
            {"input": "3\n1 2 5\n11\n", "output": "3"},
            {"input": "1\n2\n3\n", "output": "-1"},
        ],
        "starter_code_json": {"python": "n = int(input())\ncoins = list(map(int, input().split()))\namount = int(input())\n"},
        "hints_json": [{"level": 1, "text": "dp[a] = 1 + min(dp[a - c] for each coin c)."}],
    },
    {
        "title": "Longest Common Subsequence",
        "slug": "longest-common-subsequence",
        "description": "Find the length of the longest common subsequence of two strings.",
        "difficulty": 3,
        "tags": ["dp", "strings"],
        "xp_reward": 50,
        "examples_json": [{"input": "abcde, ace", "output": "3"}],
        "test_cases_json": [
            {"input": "abcde\nace\n", "output": "3"},
            {"input": "abc\ndef\n", "output": "0"},
        ],
        "starter_code_json": {"python": "a = input()\nb = input()\n"},
        "hints_json": [{"level": 1, "text": "2D dp[i][j] = LCS of a[:i], b[:j]."}],
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "description": "Minimum edits (insert, delete, replace) to convert word1 to word2.",
        "difficulty": 5,
        "tags": ["dp", "strings"],
        "xp_reward": 150,
        "examples_json": [{"input": "horse -> ros", "output": "3"}],
        "test_cases_json": [{"input": "horse\nros\n", "output": "3"}],
        "starter_code_json": {"python": "a = input()\nb = input()\n"},
        "hints_json": [{"level": 1, "text": "dp[i][j] = min of three options from smaller subproblems."}],
    },

    # =========================================================================
    # HARD
    # =========================================================================
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-two-sorted",
        "description": "Find the median of two sorted arrays in O(log(min(m,n))).",
        "difficulty": 5,
        "tags": ["arrays", "binary-search"],
        "xp_reward": 150,
        "examples_json": [{"input": "[1,3], [2]", "output": "2.0"}],
        "test_cases_json": [
            {"input": "2\n1 3\n1\n2\n", "output": "2.0"},
            {"input": "2\n1 2\n2\n3 4\n", "output": "2.5"},
        ],
        "starter_code_json": {"python": "# binary search on the shorter array\n"},
        "hints_json": [
            {"level": 1, "text": "Binary search partition of the smaller array."},
            {"level": 2, "text": "Partition so left halves contain half the total; compare max-left to min-right."},
        ],
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "description": "Given heights, compute how much water can be trapped after raining.",
        "difficulty": 5,
        "tags": ["arrays", "two-pointers", "dp"],
        "xp_reward": 150,
        "examples_json": [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"}],
        "test_cases_json": [{"input": "12\n0 1 0 2 1 0 1 3 2 1 2 1\n", "output": "6"}],
        "starter_code_json": {"python": "n = int(input())\nh = list(map(int, input().split()))\n"},
        "hints_json": [
            {"level": 1, "text": "Water above index i = min(maxLeft, maxRight) - height[i]."},
            {"level": 2, "text": "Two pointers with running max on each side."},
        ],
    },
    {
        "title": "Minimum Window Substring",
        "slug": "min-window-substring",
        "description": "Find the shortest substring of s that contains all characters of t (with multiplicity).",
        "difficulty": 5,
        "tags": ["strings", "sliding-window"],
        "xp_reward": 150,
        "examples_json": [{"input": "s=ADOBECODEBANC, t=ABC", "output": "BANC"}],
        "test_cases_json": [{"input": "ADOBECODEBANC\nABC\n", "output": "BANC"}],
        "starter_code_json": {"python": "s = input()\nt = input()\n"},
        "hints_json": [
            {"level": 1, "text": "Sliding window with a need/have counter."},
            {"level": 2, "text": "Expand right until valid, then shrink left while still valid."},
        ],
    },

    # =========================================================================
    # EASY fundamentals (for Year 1 students)
    # =========================================================================
    {
        "title": "FizzBuzz",
        "slug": "fizzbuzz",
        "description": "Print 1..n; multiples of 3 -> Fizz; of 5 -> Buzz; both -> FizzBuzz.",
        "difficulty": 1,
        "tags": ["basics"],
        "xp_reward": 20,
        "examples_json": [{"input": "5", "output": "1\\n2\\nFizz\\n4\\nBuzz"}],
        "test_cases_json": [{"input": "5\n", "output": "1\n2\nFizz\n4\nBuzz"}],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Check %15 first, then %3, then %5."}],
    },
    {
        "title": "Sum of Digits",
        "slug": "sum-of-digits",
        "description": "Compute the sum of digits of a positive integer.",
        "difficulty": 1,
        "tags": ["basics", "math"],
        "xp_reward": 20,
        "examples_json": [{"input": "1234", "output": "10"}],
        "test_cases_json": [
            {"input": "1234\n", "output": "10"},
            {"input": "99\n", "output": "18"},
        ],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Use %10 and //10 in a loop, or convert to string."}],
    },
    {
        "title": "Factorial",
        "slug": "factorial",
        "description": "Compute n! iteratively.",
        "difficulty": 1,
        "tags": ["basics", "math"],
        "xp_reward": 20,
        "examples_json": [{"input": "5", "output": "120"}],
        "test_cases_json": [
            {"input": "5\n", "output": "120"},
            {"input": "0\n", "output": "1"},
        ],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Start with 1, multiply from 2 to n."}],
    },
    {
        "title": "Prime Check",
        "slug": "prime-check",
        "description": "Is the given integer prime?",
        "difficulty": 1,
        "tags": ["basics", "math"],
        "xp_reward": 20,
        "examples_json": [{"input": "7", "output": "true"}],
        "test_cases_json": [
            {"input": "7\n", "output": "true"},
            {"input": "9\n", "output": "false"},
        ],
        "starter_code_json": {"python": "n = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Check divisors up to sqrt(n)."}],
    },
    {
        "title": "GCD (Euclidean)",
        "slug": "gcd-euclidean",
        "description": "Compute the greatest common divisor of two positive integers.",
        "difficulty": 1,
        "tags": ["basics", "math"],
        "xp_reward": 20,
        "examples_json": [{"input": "12 8", "output": "4"}],
        "test_cases_json": [
            {"input": "12 8\n", "output": "4"},
            {"input": "7 11\n", "output": "1"},
        ],
        "starter_code_json": {"python": "a, b = map(int, input().split())\n"},
        "hints_json": [{"level": 1, "text": "gcd(a, b) = gcd(b, a % b) until b is 0."}],
    },
    {
        "title": "Reverse Integer",
        "slug": "reverse-integer",
        "description": "Reverse the digits of a signed integer. Return 0 on 32-bit overflow.",
        "difficulty": 2,
        "tags": ["math"],
        "xp_reward": 40,
        "examples_json": [{"input": "-123", "output": "-321"}],
        "test_cases_json": [
            {"input": "-123\n", "output": "-321"},
            {"input": "120\n", "output": "21"},
        ],
        "starter_code_json": {"python": "x = int(input())\n"},
        "hints_json": [{"level": 1, "text": "Use abs, reverse, reapply sign, check overflow."}],
    },
    {
        "title": "Single Number",
        "slug": "single-number",
        "description": "Every element appears twice except one. Find the single one. Linear time, constant space.",
        "difficulty": 1,
        "tags": ["arrays", "bit-manipulation"],
        "xp_reward": 20,
        "examples_json": [{"input": "[2,2,1]", "output": "1"}],
        "test_cases_json": [{"input": "3\n2 2 1\n", "output": "1"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "XOR all elements — pairs cancel."}],
    },
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "description": "Given an array of size n, return the element that appears more than ⌊n/2⌋ times.",
        "difficulty": 1,
        "tags": ["arrays"],
        "xp_reward": 20,
        "examples_json": [{"input": "[3,2,3]", "output": "3"}],
        "test_cases_json": [{"input": "3\n3 2 3\n", "output": "3"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Boyer-Moore voting algorithm: one pass, O(1) extra."}],
    },
    {
        "title": "Missing Number",
        "slug": "missing-number",
        "description": "Given an array containing n distinct numbers from [0, n], find the missing one.",
        "difficulty": 1,
        "tags": ["arrays", "math"],
        "xp_reward": 20,
        "examples_json": [{"input": "[3,0,1]", "output": "2"}],
        "test_cases_json": [{"input": "3\n3 0 1\n", "output": "2"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Sum 0..n and subtract sum of array."}],
    },
    {
        "title": "Intersection of Two Arrays",
        "slug": "array-intersection",
        "description": "Return unique elements present in both arrays.",
        "difficulty": 1,
        "tags": ["arrays", "hashing"],
        "xp_reward": 20,
        "examples_json": [{"input": "[1,2,2,1], [2,2]", "output": "[2]"}],
        "test_cases_json": [{"input": "4\n1 2 2 1\n2\n2 2\n", "output": "2"}],
        "starter_code_json": {"python": "n = int(input())\na = list(map(int, input().split()))\nm = int(input())\nb = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Set intersection."}],
    },
    {
        "title": "Add Two Numbers (Linked List)",
        "slug": "add-two-numbers-ll",
        "description": "Two non-negative integers are stored in reverse order as linked lists. Return their sum as a linked list.",
        "difficulty": 3,
        "tags": ["linked-list", "math"],
        "xp_reward": 50,
        "examples_json": [{"input": "[2,4,3] + [5,6,4]", "output": "[7,0,8]"}],
        "test_cases_json": [{"input": "3\n2 4 3\n3\n5 6 4\n", "output": "7 0 8"}],
        "starter_code_json": {"python": "# carry + dummy head\n"},
        "hints_json": [{"level": 1, "text": "Walk both lists with a carry variable."}],
    },
    {
        "title": "LRU Cache",
        "slug": "lru-cache",
        "description": "Design an LRU cache supporting get and put in O(1).",
        "difficulty": 4,
        "tags": ["design", "hashing", "linked-list"],
        "xp_reward": 80,
        "examples_json": [{"input": "put(1,1); put(2,2); get(1); put(3,3); get(2)", "output": "1 -1"}],
        "test_cases_json": [{"input": "2\n5\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\n", "output": "1\n-1"}],
        "starter_code_json": {"python": "# OrderedDict or hash + doubly linked list\n"},
        "hints_json": [
            {"level": 1, "text": "Python: collections.OrderedDict has move_to_end."},
            {"level": 2, "text": "Manual: hash map of key -> node in a doubly linked list."},
        ],
    },
    {
        "title": "Word Break",
        "slug": "word-break",
        "description": "Given a string s and a dictionary, determine if s can be segmented into space-separated dictionary words.",
        "difficulty": 3,
        "tags": ["dp", "strings"],
        "xp_reward": 50,
        "examples_json": [{"input": "s=leetcode, dict=[leet,code]", "output": "true"}],
        "test_cases_json": [{"input": "leetcode\n2\nleet code\n", "output": "true"}],
        "starter_code_json": {"python": "s = input()\nn = int(input())\nwords = input().split()\n"},
        "hints_json": [{"level": 1, "text": "dp[i] = true iff some suffix ending at i matches a word and dp[i-len(word)] is true."}],
    },
    {
        "title": "Partition Equal Subset Sum",
        "slug": "partition-equal-subset-sum",
        "description": "Determine if an array can be partitioned into two subsets with equal sum.",
        "difficulty": 3,
        "tags": ["dp", "knapsack"],
        "xp_reward": 50,
        "examples_json": [{"input": "[1,5,11,5]", "output": "true"}],
        "test_cases_json": [{"input": "4\n1 5 11 5\n", "output": "true"}],
        "starter_code_json": {"python": "n = int(input())\nnums = list(map(int, input().split()))\n"},
        "hints_json": [{"level": 1, "text": "Sum must be even. Then 0/1 knapsack for target = sum/2."}],
    },
]
