import time
import random

# Problem setup
days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
slots_per_day = 3  # 3 slots per day → realistic timetable size
courses = [
    "Math", "Physics", "Chemistry", "English", "CS",
    "Biology", "Economics", "History", "Geography", "Art",
    "Philosophy", "Music", "PE"
]
professors = {
    "Math": "Dr. A", "Physics": "Dr. B", "Chemistry": "Dr. A",
    "English": "Dr. C", "CS": "Dr. D", "Biology": "Dr. E",
    "Economics": "Dr. C", "History": "Dr. F", "Geography": "Dr. G",
    "Art": "Dr. H", "Philosophy": "Dr. D", "Music": "Dr. E", "PE": "Dr. F"
}

time_slots = [(d, s) for d in days for s in range(1, slots_per_day + 1)]


# ---------------- Helper functions ----------------
def print_timetable(timetable):
    print("\n=== Generated Timetable ===")
    grid = {day: ["---"] * slots_per_day for day in days}
    for course, slot in timetable.items():
        d, s = slot
        grid[d][s - 1] = course[:3]  # display first 3 letters
    for d in days:
        print(f"{d}: {' | '.join(grid[d])}")


def no_conflict(course, slot, timetable):
    for c, s in timetable.items():
        if s == slot and professors[c] == professors[course]:
            return False
    return True


# ---------------- Heuristic Backtracking ----------------
def backtrack_heuristic(timetable, unassigned):
    global backtrack_count1
    if not unassigned:
        return True

    # Fixed order selection for structured output
    course = unassigned[0]
    slots = sorted(time_slots, key=lambda x: (days.index(x[0]), x[1]))

    for slot in slots:
        if no_conflict(course, slot, timetable) and slot not in timetable.values():
            timetable[course] = slot
            if backtrack_heuristic(timetable, [c for c in unassigned if c != course]):
                return True
            backtrack_count1 += 1
            del timetable[course]
    return False


# ---------------- Forward Checking ----------------
def forward_checking(timetable, unassigned, domains):
    global backtrack_count2
    if not unassigned:
        return True

    course = unassigned[0]
    for slot in sorted(domains[course], key=lambda x: (days.index(x[0]), x[1])):
        if no_conflict(course, slot, timetable) and slot not in timetable.values():
            timetable[course] = slot
            new_domains = {c: list(domains[c]) for c in domains}
            for c in unassigned:
                if c != course and slot in new_domains[c]:
                    new_domains[c].remove(slot)
            if forward_checking(timetable, [c for c in unassigned if c != course], new_domains):
                return True
            backtrack_count2 += 1
            del timetable[course]
    return False


# ---------------- Run multiple times and average ----------------
runs = 5
avg_time_bt = 0
avg_time_fc = 0
avg_bt_count = 0
avg_fc_count = 0

for i in range(runs):
    backtrack_count1 = 0
    backtrack_count2 = 0

    # Backtracking
    start1 = time.perf_counter()
    timetable1 = {}
    backtrack_heuristic(timetable1, courses.copy())
    avg_time_bt += time.perf_counter() - start1
    avg_bt_count += backtrack_count1

    # Forward checking
    start2 = time.perf_counter()
    timetable2 = {}
    domains = {c: list(time_slots) for c in courses}
    forward_checking(timetable2, courses.copy(), domains)
    avg_time_fc += time.perf_counter() - start2
    avg_fc_count += backtrack_count2

# ---------------- Display average results ----------------
avg_time_bt /= runs
avg_time_fc /= runs
avg_bt_count //= runs
avg_fc_count //= runs

# Sort timetables for neat printing
timetable1 = dict(sorted(timetable1.items(), key=lambda x: (days.index(x[1][0]), x[1][1])))
timetable2 = dict(sorted(timetable2.items(), key=lambda x: (days.index(x[1][0]), x[1][1])))

print_timetable(timetable1)
print_timetable(timetable2)

print("\n=== Average Comparison Over Multiple Runs ===")
print(f"{'Method':35} {'Avg Time (s)':<15} {'Avg Backtracks'}")
print(f"{'Heuristic Backtracking':35} {avg_time_bt:.5f}         {avg_bt_count}")
print(f"{'Forward Checking':35} {avg_time_fc:.5f}         {avg_fc_count}")
