from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Student:
    """Represents a single student and their subject-wise marks."""
    name: str
    roll_no: str
    marks: Dict[str, float] = field(default_factory=dict)

    @property
    def total(self) -> float:
        return sum(self.marks.values())

    @property
    def average(self) -> float:
        return self.total / len(self.marks) if self.marks else 0.0

    @property
    def grade(self) -> str:
        return calculate_grade(self.average)

    @property
    def result(self) -> str:
        """Fail if any subject is below the passing mark (default 33)."""
        return "FAIL" if any(m < 33 for m in self.marks.values()) else "PASS"

def validate_name(name: str) -> str:
    name = name.strip()
    if not name or not all(part.isalpha() for part in name.split()):
        raise ValueError("Name must contain only letters and spaces.")
    return name.title()


def validate_roll_no(roll_no: str) -> str:
    roll_no = roll_no.strip()
    if not roll_no:
        raise ValueError("Roll number cannot be empty.")
    return roll_no


def validate_mark(subject: str, value: str) -> float:
    try:
        mark = float(value)
    except ValueError:
        raise ValueError(f"Mark for '{subject}' must be a number.")
    if not (0 <= mark <= 100):
        raise ValueError(f"Mark for '{subject}' must be between 0 and 100.")
    return mark


def validate_subject_count(count: str) -> int:
    try:
        n = int(count)
    except ValueError:
        raise ValueError("Number of subjects must be a whole number.")
    if n <= 0:
        raise ValueError("Number of subjects must be greater than zero.")
    return n

def calculate_grade(average: float) -> str:
    """Map an average score to a letter grade."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    elif average >= 33:
        return "E"
    else:
        return "F"


def class_statistics(students: List[Student]) -> Dict[str, float]:
    """Compute simple class-wide statistics."""
    if not students:
        return {"class_average": 0.0, "highest": 0.0, "lowest": 0.0, "pass_percentage": 0.0}

    averages = [s.average for s in students]
    passed = sum(1 for s in students if s.result == "PASS")

    return {
        "class_average": round(sum(averages) / len(averages), 2),
        "highest": round(max(averages), 2),
        "lowest": round(min(averages), 2),
        "pass_percentage": round((passed / len(students)) * 100, 2),
    }


def rank_students(students: List[Student]) -> List[Student]:
    """Return students sorted by average marks, highest first."""
    return sorted(students, key=lambda s: s.average, reverse=True)

def input_with_retry(prompt: str, validator):
    """Keep asking until the user provides valid input."""
    while True:
        raw = input(prompt)
        try:
            return validator(raw)
        except ValueError as err:
            print(f"  Invalid input: {err} Please try again.")


def collect_student(subjects: List[str]) -> Student:
    name = input_with_retry("Student name: ", validate_name)
    roll_no = input_with_retry("Roll number: ", validate_roll_no)
    student = Student(name=name, roll_no=roll_no)

    for subject in subjects:
        mark = input_with_retry(
            f"  Marks in {subject} (0-100): ",
            lambda v, subj=subject: validate_mark(subj, v)
        )
        student.marks[subject] = mark

    return student


def collect_subjects() -> List[str]:
    n = input_with_retry("How many subjects? ", validate_subject_count)
    subjects = []
    for i in range(n):
        while True:
            subj = input(f"  Subject {i + 1} name: ").strip()
            if subj and subj not in subjects:
                subjects.append(subj)
                break
            print("  Invalid or duplicate subject name. Try again.")
    return subjects

def print_student_report(student: Student) -> None:
    print(f"\n--- Report Card: {student.name} (Roll No: {student.roll_no}) ---")
    for subject, mark in student.marks.items():
        print(f"  {subject:<15}: {mark:>6.2f}")
    print(f"  {'Total':<15}: {student.total:>6.2f}")
    print(f"  {'Average':<15}: {student.average:>6.2f}")
    print(f"  {'Grade':<15}: {student.grade}")
    print(f"  {'Result':<15}: {student.result}")


def print_class_report(students: List[Student]) -> None:
    stats = class_statistics(students)
    ranked = rank_students(students)

    print("\n===== CLASS SUMMARY =====")
    print(f"Number of students : {len(students)}")
    print(f"Class average      : {stats['class_average']}")
    print(f"Highest average    : {stats['highest']}")
    print(f"Lowest average     : {stats['lowest']}")
    print(f"Pass percentage    : {stats['pass_percentage']}%")

    print("\n===== RANKING (highest to lowest) =====")
    for rank, student in enumerate(ranked, start=1):
        print(f"{rank}. {student.name:<15} Avg: {student.average:>6.2f}  Grade: {student.grade}  {student.result}")

def run_analyzer() -> None:
    print("===== STUDENT RESULT ANALYZER =====\n")

    try:
        subjects = collect_subjects()
        num_students = input_with_retry(
            "\nHow many students? ",
            validate_subject_count  # reuses positive-integer validation
        )

        students: List[Student] = []
        for i in range(num_students):
            print(f"\n-- Entering data for student {i + 1} --")
            student = collect_student(subjects)
            students.append(student)

        print("\n\n===== INDIVIDUAL REPORT CARDS =====")
        for student in students:
            print_student_report(student)

        print_class_report(students)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting gracefully.")
    except Exception as err:  # final safety net for unexpected errors
        print(f"\nAn unexpected error occurred: {err}")

def self_test() -> None:
    """Quick sanity check using sample data, demonstrating processing logic."""
    print("Running self-test with sample data...\n")

    sample = [
        Student("Asha Rao", "R001", {"Maths": 92, "Science": 88, "English": 79}),
        Student("Vikram Singh", "R002", {"Maths": 45, "Science": 30, "English": 60}),
        Student("Meena Iyer", "R003", {"Maths": 70, "Science": 65, "English": 72}),
    ]

    for student in sample:
        print_student_report(student)
    print_class_report(sample)

if __name__ == "__main__":
    print("1. Run with your own data (interactive)")
    print("2. Run self-test with sample data")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "2":
        self_test()
    else:
        run_analyzer()