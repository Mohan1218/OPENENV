"""
UPGRADED: Code Review Task Data with Realistic Security/Performance Issues
"""

CODE_REVIEW_EASY_DATA = [
    {
        "code_snippet": """
password = "admin123"
conn = mysql.connect(host, user, password)
result = conn.query("SELECT * FROM users")
""",
        "language": "python",
        "context": "Database connection code",
        "function_name": "connect_db",
        "lines_of_code": 3,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "easy",
        "issue_description": "Hardcoded password in source code - major security risk"
    },
    {
        "code_snippet": """
import os
api_key = "sk-xxxxxxxxxxx"
response = requests.get(f"https://api.com/data?key={api_key}")
""",
        "language": "python",
        "context": "API request with embedded key",
        "function_name": "fetch_data",
        "lines_of_code": 4,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "easy",
        "issue_description": "Exposed API key in code"
    },
    {
        "code_snippet": """
def process_data(data):
    result = eval(data)
    return result
""",
        "language": "python",
        "context": "User input processing",
        "function_name": "process_data",
        "lines_of_code": 3,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "easy",
        "issue_description": "Using eval() on user input allows arbitrary code execution"
    },
]

CODE_REVIEW_MEDIUM_DATA = [
    {
        "code_snippet": """
def search_items(items, query):
    results = []
    for item in items:
        for char in item:
            if char == query:
                results.append(item)
    return results
""",
        "language": "python",
        "context": "Search algorithm",
        "function_name": "search_items",
        "lines_of_code": 7,
        "correct_issues": ["performance"],
        "correct_severity": "major",
        "correct_priority": "medium",
        "difficulty": "medium",
        "issue_description": "Nested loop with O(n*m) complexity could be optimized"
    },
    {
        "code_snippet": """
user_input = request.get("name")
query = f"SELECT * FROM users WHERE name = '{user_input}'"
result = db.execute(query)
""",
        "language": "python",
        "context": "Database query",
        "function_name": "find_user",
        "lines_of_code": 3,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "medium",
        "issue_description": "SQL injection vulnerability - user input not sanitized"
    },
    {
        "code_snippet": """
def calculate_total(prices):
    total = 0
    for price in prices:
        total = total + price
    return total
""",
        "language": "python",
        "context": "Price calculation",
        "function_name": "calculate_total",
        "lines_of_code": 5,
        "correct_issues": ["style"],
        "correct_severity": "minor",
        "correct_priority": "low",
        "difficulty": "medium",
        "issue_description": "Can use sum() for cleaner code"
    },
]

CODE_REVIEW_HARD_DATA = [
    {
        "code_snippet": """
def sync_data():
    lock = threading.Lock()
    with lock:
        data = fetch_from_api()
        while fetch_from_api() != data:
            data = fetch_from_api()
    return data
""",
        "language": "python",
        "context": "Data synchronization",
        "function_name": "sync_data",
        "lines_of_code": 8,
        "correct_issues": ["performance", "logic"],
        "correct_severity": "major",
        "correct_priority": "high",
        "difficulty": "hard",
        "issue_description": "Infinite loop potential + excessive API calls in tight loop"
    },
    {
        "code_snippet": """
def decrypt_password(encrypted):
    key = "key123"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(encrypted)
""",
        "language": "python",
        "context": "Password decryption",
        "function_name": "decrypt_password",
        "lines_of_code": 4,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "hard",
        "issue_description": "Weak encryption: hardcoded key + ECB mode is insecure"
    },
    {
        "code_snippet": """
def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = {}".format(user_id)
    result = db.execute(query)
    return result[0] if result else None
""",
        "language": "python",
        "context": "User lookup",
        "function_name": "get_user_by_id",
        "lines_of_code": 4,
        "correct_issues": ["security"],
        "correct_severity": "critical",
        "correct_priority": "high",
        "difficulty": "hard",
        "issue_description": "String formatting allows SQL injection"
    },
]
