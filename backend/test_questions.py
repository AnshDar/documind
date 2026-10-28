import time
from app.rag import answer_question

questions = [
    ("What is the hotel limit in metro cities?", "4,500"),
    ("What is the hotel limit in other cities?", "3,000"),
    ("How many casual leaves does a permanent employee get?", "12"),
    ("How many casual leaves does a contract employee get?", "8"),
    ("What is the maximum carry-forward for earned leave?", "30"),
    ("How long is maternity leave?", "26"),
    ("How many days of paternity leave are allowed?", "10"),
    ("How many days a week can I work from home?", "2 days"),
    ("What is the minimum password length?", "12"),
    ("Within how many hours must a lost laptop be reported?", "4 hours"),
    ("How many days do I have to submit an expense claim?", "30"),
    ("Above what amount is a receipt needed?", "500"),
    ("What time is lunch served in the cafeteria?", "12:30"),
    ("How much does a guest meal cost?", "150"),
    ("What does four-wheeler parking cost per month?", "1,500"),
    ("How many seats are in the boardroom?", "14"),
    ("What is the longest a meeting room can be booked for?", "2 hours"),
    ("What is the office dress code?", None),
    ("What is the annual bonus?", None),
    ("Who is the CEO of the company?", None),
]

passed = 0
real_distances = []
trap_distances = []

for q, expected in questions:
    result = answer_question(q)
    answer = result["answer"].replace("\u202f", " ")

    if expected is None:
        ok = "could not find" in answer.lower()
        trap_distances.append(result["best_distance"])
    else:
        ok = expected in answer
        real_distances.append(result["best_distance"])

    if ok:
        passed += 1
    print("PASS" if ok else "FAIL", round(result["best_distance"], 2), q)
    if not ok:
        print("      answer:", answer)
    time.sleep(3)

print()
print(passed, "of", len(questions), "passed")
print("worst real question distance:", round(max(real_distances), 2))
print("closest trap question distance:", round(min(trap_distances), 2))