"""RosterBuilder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import WorkboardView, RosterListView, DisplayRosterListView, FactionUnitsListView, CreateRosterView, \
    ManageRosterListView

app_name = "builder"

urlpatterns = [
    # path("<int:pk>", WorkboardView.as_view(), name="workboard"),
    path("roster_list/", RosterListView.as_view(), name="roster_list"),
    path("display_roster/<int:pk>", DisplayRosterListView.as_view(), name="display_roster"),
    path("manage_roster/<int:pk>", ManageRosterListView.as_view(), name="manage_roster"),
    path("units_list/", FactionUnitsListView.as_view(), name="units_list"),
    path("units_list/<int:pk>", FactionUnitsListView.as_view(), name="units_list"),
    path("roster_create/", CreateRosterView.as_view(), name="roster_create")
]
