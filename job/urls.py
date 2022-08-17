from django.urls import path

from job.views import RecruitmentView, ApplicationView, RecruitmentListView, RecruitmentDetailView

urlpatterns = [
    path("recruitment", RecruitmentView.as_view()),
    path("recruitment/<int:recruitment_id>", RecruitmentView.as_view()),
    path("recruitment/list", RecruitmentListView.as_view()),
    path("recruitment/<int:id>/detail", RecruitmentDetailView.as_view()),
    path("application", ApplicationView.as_view()),
]
