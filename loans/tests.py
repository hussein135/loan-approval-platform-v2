from unittest.mock import patch
from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .services.application_service import process_application
from .forms import LoanApplicationForm
from .models import LoanApplication
from .services.decision_service import make_decision
from .services.ml_service import predict_application

class LoanPlatformTests(TestCase):

    def setUp(self):

        self.test_password = token_urlsafe(24)

        self.valid_data = {
            "dependents": 1,
            "education": "Graduate",
            "employment_status": "Employed",
            "occupation_type": "Salaried",
            "residential_status": "Own",
            "city_town": "Urban",
            "annual_income": 90000,
            "monthly_expenses": 2500,
            "credit_score": 700,
            "existing_loans": 1,
            "total_existing_loan_amount": 10000,
            "outstanding_debt": 5000,
            "loan_history": 1,
            "loan_amount_requested": 30000,
            "loan_term": 120,
            "loan_purpose": "Personal",
            "loan_type": "Unsecured",
            "co_applicant": "No",
            "bank_account_history": 5,
            "transaction_frequency": 17,
        }

        User = get_user_model()

        self.staff_user = User.objects.create_user(
            username="staffuser",
            password=self.test_password,
            is_staff=True,
        )

    def create_application(self, **changes):

        data = self.valid_data.copy()
        data.update(changes)

        return LoanApplication.objects.create(
            **data
        )

    # ---------------------------------
    # Model Tests
    # ---------------------------------

    def test_application_can_be_created(self):

        application = self.create_application()

        self.assertEqual(
            application.credit_score,
            700
        )

        self.assertEqual(
            application.system_status,
            "Pending"
        )

    def test_application_string(self):

        application = self.create_application()

        self.assertEqual(
            str(application),
            f"Application #{application.id} - Pending"
        )

    # ---------------------------------
    # Form Tests
    # ---------------------------------

    def test_valid_application_form(self):

        form = LoanApplicationForm(
            data=self.valid_data
        )

        self.assertTrue(
            form.is_valid()
        )

    def test_invalid_credit_score(self):

        data = self.valid_data.copy()

        data["credit_score"] = 1000

        form = LoanApplicationForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "credit_score",
            form.errors
        )

    def test_invalid_dependents(self):

        data = self.valid_data.copy()

        data["dependents"] = 10

        form = LoanApplicationForm(
            data=data
        )

        self.assertFalse(
            form.is_valid()
        )

    # ---------------------------------
    # Decision Engine Tests
    # ---------------------------------

    def test_models_agree_approved(self):

        prediction = {
            "primary_prediction": 1,
            "primary_probability": 0.85,
            "secondary_prediction": 1,
            "secondary_probability": 0.80,
        }

        decision = make_decision(prediction)

        self.assertEqual(
            decision["model_recommendation"],
            "Approved"
        )

        self.assertEqual(
            decision["system_status"],
            "Approved"
        )

        self.assertEqual(
            decision["review_reason"],
            "Models agree"
        )

    def test_models_agree_rejected(self):

        prediction = {
            "primary_prediction": 0,
            "primary_probability": 0.20,
            "secondary_prediction": 0,
            "secondary_probability": 0.30,
        }

        decision = make_decision(prediction)

        self.assertEqual(
            decision["system_status"],
            "Rejected"
        )

        self.assertAlmostEqual(
            decision["risk_score"],
            0.80
        )

    def test_model_disagreement_creates_review(self):

        prediction = {
            "primary_prediction": 1,
            "primary_probability": 0.80,
            "secondary_prediction": 0,
            "secondary_probability": 0.40,
        }

        decision = make_decision(prediction)

        self.assertEqual(
            decision["system_status"],
            "Under Review"
        )

        self.assertEqual(
            decision["review_reason"],
            "Model disagreement"
        )

    def test_business_review_has_priority(self):

        prediction = {
            "primary_prediction": 1,
            "primary_probability": 0.90,
            "secondary_prediction": 1,
            "secondary_probability": 0.88,
        }

        decision = make_decision(
            prediction,
            business_review=True
        )

        self.assertEqual(
            decision["system_status"],
            "Under Review"
        )

    # ---------------------------------
    # Public View Tests
    # ---------------------------------

    def test_home_page(self):

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_application_form_page(self):

        response = self.client.get(
            reverse("create_application")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ---------------------------------
    # Staff Permission Tests
    # ---------------------------------

    def test_dashboard_requires_staff(self):

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_staff_can_open_dashboard(self):

        self.client.login(
            username="staffuser",
            password=self.test_password
        )

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertEqual(
            response.status_code,
            200
        )

    # ---------------------------------
    # Human Review Tests
    # ---------------------------------

    def test_human_reviewer_can_approve(self):

        application = self.create_application(
            system_status="Under Review",
            review_reason="Model disagreement",
        )

        self.client.login(
            username="staffuser",
            password=self.test_password
        )

        response = self.client.post(
            reverse(
                "review_application",
                args=[application.id]
            ),
            {
                "human_decision": "Approved"
            }
        )

        application.refresh_from_db()

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            application.human_decision,
            "Approved"
        )

        self.assertEqual(
            application.system_status,
            "Approved"
        )

    # ---------------------------------
    # Application Submission Test
    # ---------------------------------

    @patch(
        "loans.views.process_application"
    )
    def test_application_submission(
        self,
        mock_process_application
    ):

        response = self.client.post(
            reverse("create_application"),
            data=self.valid_data
        )

        self.assertEqual(
            LoanApplication.objects.count(),
            1
        )

        application = (
            LoanApplication.objects.first()
        )

        mock_process_application.assert_called_once_with(
            application
        )

        self.assertEqual(
            response.status_code,
            302
        )
        from .services.ml_service import predict_application
from .services.application_service import process_application


class MachineLearningIntegrationTests(TestCase):

    def setUp(self):

        self.application = LoanApplication.objects.create(
            dependents=1,
            education="Graduate",
            employment_status="Employed",
            occupation_type="Salaried",
            residential_status="Own",
            city_town="Urban",
            annual_income=90000,
            monthly_expenses=2500,
            credit_score=497,
            existing_loans=1,
            total_existing_loan_amount=10000,
            outstanding_debt=5000,
            loan_history=1,
            loan_amount_requested=30000,
            loan_term=120,
            loan_purpose="Personal",
            loan_type="Unsecured",
            co_applicant="No",
            bank_account_history=5,
            transaction_frequency=17,
        )

    def test_real_models_load_and_predict(self):

        result = predict_application(
            self.application
        )

        self.assertIn(
            result["primary_prediction"],
            [0, 1]
        )

        self.assertIn(
            result["secondary_prediction"],
            [0, 1]
        )

        self.assertGreaterEqual(
            result["primary_probability"],
            0
        )

        self.assertLessEqual(
            result["primary_probability"],
            1
        )

        self.assertGreaterEqual(
            result["secondary_probability"],
            0
        )

        self.assertLessEqual(
            result["secondary_probability"],
            1
        )

    def test_real_application_processing(self):

        process_application(
            self.application
        )

        self.application.refresh_from_db()

        self.assertIn(
            self.application.model_recommendation,
            [
                "Approved",
                "Rejected",
            ]
        )

        self.assertIn(
            self.application.system_status,
            [
                "Approved",
                "Rejected",
                "Under Review",
            ]
        )

        self.assertIsNotNone(
            self.application.approval_probability
        )

        self.assertIsNotNone(
            self.application.risk_score
        )

        self.assertIsNotNone(
            self.application.secondary_probability
        )
