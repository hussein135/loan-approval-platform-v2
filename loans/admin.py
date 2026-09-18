from django.contrib import admin
from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "credit_score",
        "annual_income",
        "loan_amount_requested",
        "model_recommendation",
        "system_status",
        "human_decision",
        "created_at",
    ]

    list_editable = [
        "system_status",
        "human_decision",
    ]

    list_filter = [
        "model_recommendation",
        "system_status",
        "human_decision",
        "loan_purpose",
        "employment_status",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]