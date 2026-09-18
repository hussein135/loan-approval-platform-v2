from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class LoanApplication(models.Model):

    # -----------------------------
    # Choices
    # -----------------------------

    EDUCATION_CHOICES = [
        ("Graduate", "Graduate"),
        ("High School", "High School"),
        ("Postgrad", "Postgrad"),
    ]

    EMPLOYMENT_CHOICES = [
        ("Employed", "Employed"),
        ("Self-Employed", "Self-Employed"),
        ("Unemployed", "Unemployed"),
    ]

    OCCUPATION_CHOICES = [
        ("Business", "Business"),
        ("Freelancer", "Freelancer"),
        ("Professional", "Professional"),
        ("Salaried", "Salaried"),
    ]

    RESIDENTIAL_CHOICES = [
        ("Own", "Own"),
        ("Rent", "Rent"),
        ("Other", "Other"),
    ]

    CITY_CHOICES = [
        ("Urban", "Urban"),
        ("Suburban", "Suburban"),
        ("Rural", "Rural"),
    ]

    LOAN_PURPOSE_CHOICES = [
        ("Education", "Education"),
        ("Home", "Home"),
        ("Personal", "Personal"),
        ("Vehicle", "Vehicle"),
    ]

    LOAN_TYPE_CHOICES = [
        ("Secured", "Secured"),
        ("Unsecured", "Unsecured"),
    ]

    CO_APPLICANT_CHOICES = [
        ("Yes", "Yes"),
        ("No", "No"),
    ]

    RECOMMENDATION_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Under Review", "Under Review"),
    ]

    HUMAN_DECISION_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    # -----------------------------
    # Applicant / Model Features
    # -----------------------------

    dependents = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ]
    )

    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
    )

    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
    )

    occupation_type = models.CharField(
        max_length=20,
        choices=OCCUPATION_CHOICES,
    )

    residential_status = models.CharField(
        max_length=20,
        choices=RESIDENTIAL_CHOICES,
    )

    city_town = models.CharField(
        max_length=20,
        choices=CITY_CHOICES,
    )

    annual_income = models.FloatField(
        validators=[
            MinValueValidator(20009),
            MaxValueValidator(149998),
        ]
    )

    monthly_expenses = models.FloatField(
        validators=[
            MinValueValidator(500),
            MaxValueValidator(4999),
        ]
    )

    credit_score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(300),
            MaxValueValidator(849),
        ]
    )

    existing_loans = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(2),
        ]
    )

    total_existing_loan_amount = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(49999),
        ]
    )

    outstanding_debt = models.FloatField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(29998),
        ]
    )

    loan_history = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ]
    )

    loan_amount_requested = models.FloatField(
        validators=[
            MinValueValidator(5000),
            MaxValueValidator(44848),
        ]
    )

    loan_term = models.PositiveIntegerField(
        validators=[
            MinValueValidator(12),
            MaxValueValidator(239),
        ]
    )

    loan_purpose = models.CharField(
        max_length=20,
        choices=LOAN_PURPOSE_CHOICES,
    )

    loan_type = models.CharField(
        max_length=20,
        choices=LOAN_TYPE_CHOICES,
    )

    co_applicant = models.CharField(
        max_length=3,
        choices=CO_APPLICANT_CHOICES,
    )

    bank_account_history = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9),
        ]
    )

    transaction_frequency = models.PositiveIntegerField(
        validators=[
            MinValueValidator(5),
            MaxValueValidator(29),
        ]
    )

    # -----------------------------
    # Machine Learning Results
    # -----------------------------

    model_recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES,
        default="Pending",
    )

    approval_probability = models.FloatField(
        null=True,
        blank=True,
    )

    risk_score = models.FloatField(
        null=True,
        blank=True,
    )

    secondary_recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES,
        default="Pending",
    )

    secondary_probability = models.FloatField(
        null=True,
        blank=True,
    )

    # -----------------------------
    # Decision / Human Review
    # -----------------------------

    system_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )

    review_reason = models.CharField(
        max_length=200,
        blank=True,
    )

    human_decision = models.CharField(
        max_length=20,
        choices=HUMAN_DECISION_CHOICES,
        default="Pending",
    )

    # -----------------------------
    # Timestamps
    # -----------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return (
            f"Application #{self.id} "
            f"- {self.system_status}"
        )

    class Meta:
        ordering = ["-created_at"]