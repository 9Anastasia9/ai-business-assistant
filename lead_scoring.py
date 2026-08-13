def calculate_lead_score(budget, urgency, interest_level):
    """
    Calculate a lead score from 0 to 100.
    """

    score = 0

    # Budget score
    if budget >= 10000:
        score += 40
    elif budget >= 5000:
        score += 30
    elif budget >= 2000:
        score += 20
    elif budget > 0:
        score += 10

    # Urgency score
    urgency_scores = {
        "Immediate": 30,
        "This week": 25,
        "This month": 15,
        "Just exploring": 5,
    }

    score += urgency_scores.get(urgency, 0)

    # Interest score
    interest_scores = {
        "High": 30,
        "Medium": 20,
        "Low": 10,
    }

    score += interest_scores.get(interest_level, 0)

    return min(score, 100)


def classify_lead(score):
    """
    Classify the lead based on its score.
    """

    if score >= 75:
        return "HOT"
    elif score >= 45:
        return "WARM"
    else:
        return "COLD"


def recommend_action(score):
    """
    Recommend the next sales action.
    """

    if score >= 75:
        return "Contact immediately and prepare a personalized offer."

    elif score >= 45:
        return "Follow up within 24 hours and gather more information."

    else:
        return "Add to nurturing pipeline and follow up later."


def analyze_lead(budget, urgency, interest_level):
    """
    Complete lead analysis.
    """

    score = calculate_lead_score(
        budget,
        urgency,
        interest_level,
    )

    return {
        "score": score,
        "priority": classify_lead(score),
        "recommended_action": recommend_action(score),
    }
