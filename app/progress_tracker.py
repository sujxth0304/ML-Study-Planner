import matplotlib.pyplot as plt

def track_progress(study_plan, completed_tasks):
    """
    Visualize study plan progress.
    """
    total_tasks = sum(len(schedule) for schedule in study_plan.values())
    completed = len(completed_tasks)
    completion_rate = (completed / total_tasks) * 100

    print(f"Completion Rate: {completion_rate:.2f}%")

    # Plot progress
    labels = ['Completed', 'Remaining']
    sizes = [completed, total_tasks - completed]
    colors = ['green', 'red']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("Study Plan Progress")
    plt.show()
