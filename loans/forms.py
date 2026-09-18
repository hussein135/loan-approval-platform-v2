from django import forms

from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):

    class Meta:
        model = LoanApplication

        fields = [
            "dependents",
            "education",
            "employment_status",
            "occupation_type",
            "residential_status",
            "city_town",
            "annual_income",
            "monthly_expenses",
            "credit_score",
            "existing_loans",
            "total_existing_loan_amount",
            "outstanding_debt",
            "loan_history",
            "loan_amount_requested",
            "loan_term",
            "loan_purpose",
            "loan_type",
            "co_applicant",
            "bank_account_history",
            "transaction_frequency",
        ]

        labels = {
            "dependents": "Dependents",
            "education": "Education",
            "employment_status": "Employment Status",
            "occupation_type": "Occupation Type",
            "residential_status": "Residential Status",
            "city_town": "City / Town",
            "annual_income": "Annual Income",
            "monthly_expenses": "Monthly Expenses",
            "credit_score": "Credit Score",
            "existing_loans": "Existing Loans",
            "total_existing_loan_amount":
                "Total Existing Loan Amount",
            "outstanding_debt": "Outstanding Debt",
            "loan_history": "Loan History",
            "loan_amount_requested":
                "Loan Amount Requested",
            "loan_term": "Loan Term",
            "loan_purpose": "Loan Purpose",
            "loan_type": "Loan Type",
            "co_applicant": "Co-Applicant",
            "bank_account_history":
                "Bank Account History",
            "transaction_frequency":
                "Transaction Frequency",
        }

        widgets = {
            "annual_income": forms.NumberInput(
                attrs={"step": "0.01"}
            ),
            "monthly_expenses": forms.NumberInput(
                attrs={"step": "0.01"}
            ),
            "total_existing_loan_amount":
                forms.NumberInput(
                    attrs={"step": "0.01"}
                ),
            "outstanding_debt": forms.NumberInput(
                attrs={"step": "0.01"}
            ),
            "loan_amount_requested":
                forms.NumberInput(
                    attrs={"step": "0.01"}
                ),
        }