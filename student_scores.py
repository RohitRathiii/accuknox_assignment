import sys

import matplotlib.pyplot as plt
import requests

API_URL = "http://127.0.0.1:8000/api/students"
subjects = ["math", "science", "english"]

res = requests.get(API_URL, timeout=10)
res.raise_for_status()
data = res.json()

students = []
for s in data:
    scores = [s.get(sub) for sub in subjects]
    # if a score is missing skip the student, counting it as 0 would pull the average down
    if not all(isinstance(x, (int, float)) for x in scores):
        print(f"skipping {s['name']}, score missing")
        continue
    s["avg"] = sum(scores) / len(scores)
    students.append(s)

if not students:
    sys.exit("no valid student data from the api")

students.sort(key=lambda s: s["avg"], reverse=True)
class_avg = sum(s["avg"] for s in students) / len(students)

print(f"\n{'name':<10}{'math':>6}{'sci':>6}{'eng':>6}{'avg':>8}")
for s in students:
    print(f"{s['name']:<10}{s['math']:>6}{s['science']:>6}{s['english']:>6}{s['avg']:>8.1f}")

print()
for sub in subjects:
    print(f"{sub} average: {sum(s[sub] for s in students) / len(students):.1f}")
print(f"class average: {class_avg:.1f}")
print(f"top student: {students[0]['name']} ({students[0]['avg']:.1f})")

names = [s["name"] for s in students]
avgs = [s["avg"] for s in students]

plt.figure(figsize=(10, 5))
plt.bar(names, avgs)
plt.axhline(class_avg, color="black", linestyle="dashed", label=f"class average ({class_avg:.1f})")
plt.title("Average test score per student")
plt.xlabel("Student")
plt.ylabel("Average score")
plt.ylim(0, 100)
plt.legend()
plt.tight_layout()
plt.savefig("scores_chart.png")
plt.show()
