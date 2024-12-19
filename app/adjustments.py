def adjust_plan_for_missed_days(study_plan, missed_days):
    """
    Reallocate topics for missed days.
    """
    for subject, schedule in study_plan.items():
        adjusted_schedule = []
        for task in schedule:
            day = int(task.split(":")[0].split(" ")[1])
            if day in missed_days:
                day += 1
            adjusted_schedule.append(f"Day {day}: {task.split(': ')[1]}")
        study_plan[subject] = adjusted_schedule

    return study_plan
