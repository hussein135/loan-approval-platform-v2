from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "apply/",
        views.create_application,
        name="create_application"
    ),

    path(
        "result/<int:application_id>/",
        views.result,
        name="application_result"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "applications/",
        views.application_list,
        name="application_list"
    ),

    path(
        "review/",
        views.review_dashboard,
        name="review_dashboard"
    ),

    path(
        "review/<int:application_id>/",
        views.review_application,
        name="review_application"
    ),
]