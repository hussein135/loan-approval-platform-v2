from .ml_service import predict_application
from .decision_service import make_decision


def process_application(
    application,
    business_review=False
):
    prediction_result = predict_application(
        application
    )

    decision = make_decision(
        prediction_result,
        business_review=business_review
    )

    application.model_recommendation = decision[
        "model_recommendation"
    ]

    application.approval_probability = decision[
        "approval_probability"
    ]

    application.risk_score = decision[
        "risk_score"
    ]

    application.secondary_recommendation = decision[
        "secondary_recommendation"
    ]

    application.secondary_probability = decision[
        "secondary_probability"
    ]

    application.system_status = decision[
        "system_status"
    ]

    application.review_reason = decision[
        "review_reason"
    ]

    application.save(
        update_fields=[
            "model_recommendation",
            "approval_probability",
            "risk_score",
            "secondary_recommendation",
            "secondary_probability",
            "system_status",
            "review_reason",
            "updated_at",
        ]
    )

    return application