"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from milestone.views import MilestoneViewSet
from task.views import TaskViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from branch.views import BranchViewSet
from commit.views import CommitViewSet
from integration.views import receive_webhook_request
from label.views import LabelViewSet
from project.views import ProjectViewSet, InviteViewSet
from user.views import UserViewSet
from repository.views import RepositoryViewSet
from rest_framework_nested import routers as nested_router

router = routers.DefaultRouter()
router.register(r'project', ProjectViewSet)
router.register(r'repository', RepositoryViewSet)
router.register(r'user', UserViewSet)
router.register(r'invite', InviteViewSet)
router.register(r'branch', BranchViewSet)
router.register(r'commit', CommitViewSet)

projects_router = nested_router.NestedSimpleRouter(router, r'project', lookup='project')
projects_router.register(r'label', LabelViewSet)
projects_router.register(r'task', TaskViewSet)
projects_router.register(r'milestone', MilestoneViewSet)


tasks_router = nested_router.NestedSimpleRouter(projects_router, r'task', lookup='task')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls), name='project'),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('notify', receive_webhook_request, name='notify')
]
