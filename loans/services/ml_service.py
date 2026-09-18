from functools import lru_cache

import joblib
import pandas as pd

from django.conf import settings


PRIMARY_MODEL_PATH = (
    settings.BASE_DIR
    / "models"
    / "gradient_boosting_pipeline.joblib"
)

SECONDARY_MODEL_PATH = (
    settings.BASE_DIR
    / "models"
    / "logistic_review_pipeline.joblib"
)


@lru_cache(maxsize=1)
def load_primary_model():
    return joblib.load(PRIMARY_MODEL_PATH)


@lru_cache(maxsize=1)
def load_secondary_model():
    return joblib.load(SECONDARY_MODEL_PATH)


def build_model_input(application):
    data = {
        "Dependents": application.dependents,
        "Education": application.education,
        "Employment_Status": application.employment_status,
        "Occupation_Type": application.occupation_type,
        "Residential_Status": application.residential_status,
        "City/Town": application.city_town,
        "Annual_Income": application.annual_income,
        "Monthly_Expenses": application.monthly_expenses,
        "Credit_Score": application.credit_score,
        "Existing_Loans": application.existing_loans,
        "Total_Existing_Loan_Amount":
            application.total_existing_loan_amount,
        "Outstanding_Debt": application.outstanding_debt,
        "Loan_History": application.loan_history,
        "Loan_Amount_Requested":
            application.loan_amount_requested,
        "Loan_Term": application.loan_term,
        "Loan_Purpose": application.loan_purpose,
        "Loan_Type": application.loan_type,
        "Co-Applicant": application.co_applicant,
        "Bank_Account_History":
            application.bank_account_history,
        "Transaction_Frequency":
            application.transaction_frequency,
    }

    return pd.DataFrame([data])


def predict_application(application):
    primary_model = load_primary_model()
    secondary_model = load_secondary_model()

    model_input = build_model_input(application)

    primary_prediction = int(
        primary_model.predict(model_input)[0]
    )

    primary_probability = float(
        primary_model.predict_proba(model_input)[0, 1]
    )

    secondary_prediction = int(
        secondary_model.predict(model_input)[0]
    )

    secondary_probability = float(
        secondary_model.predict_proba(model_input)[0, 1]
    )

    return {
        "primary_prediction": primary_prediction,
        "primary_probability": primary_probability,
        "secondary_prediction": secondary_prediction,
        "secondary_probability": secondary_probability,
    }