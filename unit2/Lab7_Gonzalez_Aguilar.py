student = {
    "name": input("Enter your name: "),
    "programming": int(input("Programming score (1-10): ")),
    "design": int(input("Design score (1-10): ")),
    "networking": int(input("Networking score (1-10): "))
}
print("\nCareer Assessment Report")
print(f"Name: {student['name']}")
print(f"Programming: {student['programming']}")
print(f"Design: {student['design']}")
print(f"Networking: {student['networking']}")
max_score = max(student["programming"], student["design"], student["networking"])
if student["programming"] == student["design"] or student["programming"] == student["networking"] or student["design"] == student["networking"]:
    print("Recommended Career: Multiple Career Paths Identified")
elif student["programming"] == max_score:
    print("Recommended Career: Software Developer")
elif student["design"] == max_score:
    print("Recommended Career: UI/UX Designer")
else:
    print("Recommended Career: Network Administrator")