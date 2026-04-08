"""
Code Review Task Data - Medium Difficulty
"""

CODE_REVIEW_EASY_DATA = [
    {
        "code_snippet": """
def sum_numbers(a, b):
    return a + b
        """.strip(),
        "language": "python",
        "context": "Simple utility function",
        "function_name": "sum_numbers",
        "lines_of_code": 2,
        "correct_issues": [],
        "correct_severity": "none",
        "difficulty": "easy"
    },
    {
        "code_snippet": """
def get_user_password():
    password = "admin123"
    return password
        """.strip(),
        "language": "python",
        "context": "Authentication utility",
        "function_name": "get_user_password",
        "lines_of_code": 3,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "difficulty": "easy"
    },
    {
        "code_snippet": """
x=1+2
y = 3+4
print(x,y)
        """.strip(),
        "language": "python",
        "context": "Data processing",
        "function_name": "process_data",
        "lines_of_code": 3,
        "correct_issues": ["style"],
        "correct_severity": "minor",
        "difficulty": "easy"
    }
]

CODE_REVIEW_MEDIUM_DATA = [
    {
        "code_snippet": """
def process_user_data(user_input):
    query = "SELECT * FROM users WHERE id = " + user_input
    return database.execute(query)
        """.strip(),
        "language": "python",
        "context": "Database query processing",
        "function_name": "process_user_data",
        "lines_of_code": 3,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "difficulty": "medium"
    },
    {
        "code_snippet": """
def fibonacci(n):
    if n <= 1:
        return n
    result = 0
    for i in range(n):
        result += fibonacci(i)
    return result
        """.strip(),
        "language": "python",
        "context": "Mathematical computation",
        "function_name": "fibonacci",
        "lines_of_code": 7,
        "correct_issues": ["logic", "performance"],
        "correct_severity": "major",
        "difficulty": "medium"
    },
    {
        "code_snippet": """
def find_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False
        """.strip(),
        "language": "python",
        "context": "Array processing",
        "function_name": "find_duplicate",
        "lines_of_code": 6,
        "correct_issues": ["performance"],
        "correct_severity": "major",
        "difficulty": "medium"
    }
]

CODE_REVIEW_HARD_DATA = [
    {
        "code_snippet": """
def parse_json(data):
    try:
        parsed = eval(data)
        return parsed
    except:
        return {}
        """.strip(),
        "language": "python",
        "context": "JSON parsing utility",
        "function_name": "parse_json",
        "lines_of_code": 6,
        "correct_issues": ["security", "logic"],
        "correct_severity": "critical",
        "difficulty": "hard"
    },
    {
        "code_snippet": """
def calculate_discount(price, discount_percent):
    if discount_percent > 100:
        return 0
    return price * (100 - discount_percent) / 100
        """.strip(),
        "language": "python",
        "context": "E-commerce pricing",
        "function_name": "calculate_discount",
        "lines_of_code": 4,
        "correct_issues": [],
        "correct_severity": "none",
        "difficulty": "hard"
    },
    {
        "code_snippet": """
class UserManager:
    users = []
    def add_user(self, user):
        UserManager.users.append(user)
        """.strip(),
        "language": "python",
        "context": "User management system",
        "function_name": "UserManager",
        "lines_of_code": 4,
        "correct_issues": ["logic"],
        "correct_severity": "major",
        "difficulty": "hard"
    }
]
