from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the trained model
study_time_model = joblib.load('models/study_time_model.pkl')

def create_daily_schedule(study_plan, total_hours_per_day):
    """Create a daily schedule that distributes subjects throughout the day"""
    
    # Define time slots (assuming 8 hours of study)
    time_slots = [
        ("09:00", "10:30"),
        ("10:45", "12:15"),
        ("14:00", "15:30"),
        ("15:45", "17:15"),
        ("17:30", "19:00")
    ]
    
    # Calculate minutes per subject based on their weights
    total_minutes = total_hours_per_day * 60
    subject_minutes = {
        subject: int((data['hours'] / sum(d['hours'] for d in study_plan.values())) * total_minutes)
        for subject, data in study_plan.items()
    }
    
    # Create daily schedule
    schedule = []
    current_subject_idx = 0
    subjects = list(study_plan.keys())
    
    for start_time, end_time in time_slots:
        if current_subject_idx < len(subjects):
            schedule.append({
                'time': f"{start_time} - {end_time}",
                'subject': subjects[current_subject_idx],
                'focus': 'Main concepts and problem solving'
            })
            current_subject_idx += 1
    
    return schedule

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    try:
        # Get form data
        subject_names = request.form.getlist('subject_names[]')
        difficulties = [int(d) for d in request.form.getlist('difficulties[]')]
        topics = [int(t) for t in request.form.getlist('topics[]')]
        prior_knowledge = [3] * len(subject_names)  # Default value, could be added to form
        hours_per_day = float(request.form['hours_per_day'])
        deadline_days = int(request.form['deadline_days'])
        
        # Calculate study time for each subject using ML model
        study_plan = {}
        for i, subject in enumerate(subject_names):
            # Predict required time in minutes
            predicted_time = study_time_model.predict([[
                difficulties[i],
                topics[i],
                prior_knowledge[i]
            ]])[0]
            
            # Convert to hours and adjust for available time
            total_hours = (predicted_time * topics[i]) / 60
            
            study_plan[subject] = {
                'hours': round(total_hours, 2),
                'difficulty': difficulties[i],
                'topics': topics[i],
                'hours_per_topic': round(total_hours / topics[i], 2),
                'daily_hours': round(total_hours / deadline_days, 2)
            }
        
        # Create daily schedule
        daily_schedule = create_daily_schedule(study_plan, hours_per_day)
        
        # Generate weekly timetable
        weeks = []
        current_date = datetime.now()
        for week in range((deadline_days // 7) + 1):
            weekly_schedule = []
            for day in range(7):
                if week * 7 + day < deadline_days:
                    day_schedule = {
                        'date': current_date.strftime('%Y-%m-%d'),
                        'schedule': daily_schedule
                    }
                    weekly_schedule.append(day_schedule)
                    current_date += timedelta(days=1)
            if weekly_schedule:
                weeks.append(weekly_schedule)
        
        # Create visualizations
        plt.style.use('seaborn')
        
        # Time distribution pie chart
        plt.figure(figsize=(10, 6))
        plt.pie([data['hours'] for data in study_plan.values()],
                labels=[f"{subject}\n({data['hours']}h)" for subject, data in study_plan.items()],
                autopct='%1.1f%%',
                startangle=90)
        plt.title('Total Study Time Distribution')
        
        # Save pie chart
        img_pie = io.BytesIO()
        plt.savefig(img_pie, format='png', bbox_inches='tight')
        img_pie.seek(0)
        pie_chart = base64.b64encode(img_pie.getvalue()).decode('utf-8')
        plt.close()
        
        # Daily hours bar chart
        plt.figure(figsize=(12, 6))
        subjects = list(study_plan.keys())
        daily_hours = [data['daily_hours'] for data in study_plan.values()]
        
        plt.bar(subjects, daily_hours)
        plt.title('Daily Study Hours per Subject')
        plt.xlabel('Subjects')
        plt.ylabel('Hours per Day')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save bar chart
        img_bar = io.BytesIO()
        plt.savefig(img_bar, format='png', bbox_inches='tight')
        img_bar.seek(0)
        bar_chart = base64.b64encode(img_bar.getvalue()).decode('utf-8')
        plt.close()

        return render_template('plan.html',
                             study_plan=study_plan,
                             daily_schedule=daily_schedule,
                             weeks=weeks,
                             pie_chart=pie_chart,
                             bar_chart=bar_chart,
                             total_hours=sum(data['hours'] for data in study_plan.values()),
                             days=deadline_days)

    except Exception as e:
        print(f"Error in generate_plan: {str(e)}")
        return f"An error occurred: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)