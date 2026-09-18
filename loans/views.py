from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from .forms import LoanApplicationForm
from .models import LoanApplication

from .services.application_service import process_application
from .services.explanation_service import explain_application


def home(request):
    return render(
        request,
        "loans/home.html"
    )


def create_application(request):

    if request.method == "POST":

        form = LoanApplicationForm(
            request.POST
        )

        if form.is_valid():

            application = form.save()

            process_application(
                application
            )

            return redirect(
                "application_result",
                application_id=application.id
            )

    else:
        form = LoanApplicationForm()

    return render(
        request,
        "loans/application_form.html",
        {
            "form": form
        }
    )


def result(request, application_id):

    application = get_object_or_404(
        LoanApplication,
        id=application_id
    )

    approval_percentage = None
    risk_percentage = None
    secondary_percentage = None

    if application.approval_probability is not None:
        approval_percentage = round(
            application.approval_probability * 100,
            2
        )

    if application.risk_score is not None:
        risk_percentage = round(
            application.risk_score * 100,
            2
        )

    if application.secondary_probability is not None:
        secondary_percentage = round(
            application.secondary_probability * 100,
            2
        )

    try:
        explanation = explain_application(
            application,
            top_n=10
        )

    except Exception:
        explanation = []

    return render(
        request,
        "loans/result.html",
        {
            "application": application,
            "approval_percentage": approval_percentage,
            "risk_percentage": risk_percentage,
            "secondary_percentage": secondary_percentage,
            "explanation": explanation,
        }
    )


@staff_member_required
def dashboard(request):

    applications = LoanApplication.objects.all()

    total_count = applications.count()

    approved_count = applications.filter(
        system_status="Approved"
    ).count()

    rejected_count = applications.filter(
        system_status="Rejected"
    ).count()

    review_count = applications.filter(
        system_status="Under Review"
    ).count()

    pending_count = applications.filter(
        system_status="Pending"
    ).count()

    average_probability = applications.aggregate(
        average=Avg("approval_probability")
    )["average"]

    if average_probability is not None:
        average_probability = round(
            average_probability * 100,
            2
        )

    human_reviewed_count = applications.exclude(
        human_decision="Pending"
    ).count()

    recent_applications = applications.order_by(
        "-created_at"
    )[:10]

    context = {
        "total_count": total_count,
        "approved_count": approved_count,
        "rejected_count": rejected_count,
        "review_count": review_count,
        "pending_count": pending_count,
        "average_probability": average_probability,
        "human_reviewed_count": human_reviewed_count,
        "recent_applications": recent_applications,
    }

    return render(
        request,
        "loans/dashboard.html",
        context
    )


@staff_member_required
def application_list(request):

    applications = (
        LoanApplication.objects
        .all()
        .order_by("-created_at")
    )

    return render(
        request,
        "loans/application_list.html",
        {
            "applications": applications
        }
    )


@staff_member_required
def review_dashboard(request):

    applications = (
        LoanApplication.objects
        .filter(
            system_status="Under Review"
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "loans/review_dashboard.html",
        {
            "applications": applications
        }
    )


@staff_member_required
def review_application(
    request,
    application_id
):

    application = get_object_or_404(
        LoanApplication,
        id=application_id,
        system_status="Under Review",
    )

    if request.method == "POST":

        human_decision = request.POST.get(
            "human_decision"
        )

        if human_decision in [
            "Approved",
            "Rejected",
        ]:

            application.human_decision = (
                human_decision
            )

            application.system_status = (
                human_decision
            )

            application.review_reason = (
                "Final decision by human reviewer"
            )

            application.save(
                update_fields=[
                    "human_decision",
                    "system_status",
                    "review_reason",
                    "updated_at",
                ]
            )

            return redirect(
                "review_dashboard"
            )

    return render(
        request,
        "loans/review_application.html",
        {
            "application": application
        }
    )