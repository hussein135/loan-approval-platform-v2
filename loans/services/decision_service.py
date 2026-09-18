def make_decision(
    prediction_result,
    business_review=False
):
    primary_prediction = prediction_result[
        "primary_prediction"
    ]

    primary_probability = prediction_result[
        "primary_probability"
    ]

    secondary_prediction = prediction_result[
        "secondary_prediction"
    ]

    secondary_probability = prediction_result[
        "secondary_probability"
    ]

    model_recommendation = (
        "Approved"
        if primary_prediction == 1
        else "Rejected"
    )

    secondary_recommendation = (
        "Approved"
        if secondary_prediction == 1
        else "Rejected"
    )

    risk_score = 1 - primary_probability

    if business_review:
        system_status = "Under Review"
        review_reason = "Business or manual review"

    elif primary_prediction != secondary_prediction:
        system_status = "Under Review"
        review_reason = "Model disagreement"

    else:
        system_status = model_recommendation
        review_reason = "Models agree"

    return {
        "model_recommendation":
            model_recommendation,

        "approval_probability":
            primary_probability,

        "risk_score":
            risk_score,

        "secondary_recommendation":
            secondary_recommendation,

        "secondary_probability":
            secondary_probability,

        "system_status":
            system_status,

        "review_reason":
            review_reason,
    }