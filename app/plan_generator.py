def generate_study_plan(inputs):

    subjects = inputs["subjects"]
    total_hours = inputs["total_hours_per_day"]
    deadline_days = inputs["deadline_days"]

    study_plan = {}
    # total study slots 
    total_slots = total_hours*deadline_days
    # distributing slots among subjects 
    total_topics = sum(subject["topics"] for subject in subjects.values())
    slots_per_subject = {
        subject: (details["topics"] / total_topics)*total_slots
        for subject, details in subjects.items()
    }

    # assign topics to each day

    day = 1
    for subject, slots in slots_per_subject.items():
        study_plan[subject] = []
        for i in range(int(slots)):
            if day > deadline_days:
                day = 1
            study_plan[subject].append(f"Day {day}: Topic {i + 1}")
            day += 1

    return study_plan


if __name__ == "__main__":
    from input_handling import get_user_inputs, validate_inputs

    inputs = get_user_inputs()
    validate_inputs(inputs)
    plan = generate_study_plan(inputs)
    for subject, schedule in plan.items():
        print(f"{subject} Study Plan:")
        print("\n".join(schedule))