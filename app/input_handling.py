# setting up inputs
import json

def get_user_inputs():
    inputs = {
        "subjects":{
            "Math":{"difficulty": 3, "topics": 10},
            "Physics": {"difficulty": 4, "topics": 8},
            "Chemistry": {"difficulty": 2, "topics": 6}
        },
        "total_hours_per_day": 4,
        "deadline_days": 30
    }

    return inputs

def validate_inputs(inputs):
    if inputs["total_hours_per_day"] <= 0:
        raise ValueError("Total hours per day must be greater than zero.")
    if inputs["deadline_days"] <= 0:
        raise ValueError("Deadline days must be greater than zero.")
    for subject, details in inputs["subjects"].items():
        if details["difficulty"] < 1 or details["difficulty"] > 5:
            raise ValueError(f"Difficulty for {subject} must be between 1 and 5.")
        if details["topics"] <= 0:
            raise ValueError(f"Topics for {subject} must be greater than zero.")

    print("Inputs validated successfully!")
    
    return True