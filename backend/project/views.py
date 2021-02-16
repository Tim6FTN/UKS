import re

import requests
from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.utils import json

from branch.models import Branch
from commit.models import Commit
from integration.views import handle_commit, COMPARE_URL, handle_private_diff, handle_public_diff
from label.serializers import LabelSerializer
from project.models import Project, Invite
from project.serializers import ProjectSerializer, InviteSerializer
from repository.models import Repository


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        if not (project.is_public or project.owner == request.user or project.collaborators.filter(
                id=request.user.id).exists()):
            raise PermissionDenied()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        if Project.objects.filter(owner=request.user, name=name).exists():
            raise ValidationError(f"Project with name {name} already exists")

        repository_url = request.data.get('repositoryUrl')

        # TODO: STEP 1 - Check if repo exists on GH
        repository_response = requests.get(repository_url)
        if repository_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'The repository {repository_url} either does not exist on GitHub, or is private.')

        # TODO: STEP 2 - Get repository info from GH API
        owner_and_repo_name = re.sub('https://github.com/', '', repository_url)
        if owner_and_repo_name == repository_url:
            owner_and_repo_name = re.sub('http://github.com/', '', repository_url)
        owner, repo_name = owner_and_repo_name.split('/')
        repository_response = requests.get(f'https://api.github.com/repos/{owner}/{repo_name}')
        if repository_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'Unable to fetch info for repository {repository_url}.')

        # TODO: STEP 3 - Parse repository data
        repository_data = json.loads(repository_response.content.decode('utf-8'))
        repository_default_branch = repository_data['default_branch']
        repository_name = repository_data['name']
        repository_description = repository_data['description']
        is_repository_private = repository_data['private']

        # TODO: STEP 4 - Get info of all branches from GH API for current repository
        repository_branches_url = re.sub('{/branch}', '', repository_data['branches_url'])
        branches_response = requests.get(repository_branches_url)
        if branches_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'Unable to fetch branches info for repository {repository_url}.')
        all_branches_data = json.loads(branches_response.content.decode('utf-8'))
        names_of_all_branches = [branch_data['name'] for branch_data in all_branches_data]

        # TODO: STEP 5 - Get info of all commits for main branch
        commits_response = requests.get(f'https://api.github.com/repos/{owner}/{repo_name}/commits?sha=main')
        if commits_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'Unable to fetch commit info for main branch of repository {repository_url}.')
        commits_data = json.loads(commits_response.content.decode('utf-8'))

        # TODO: STEP 6 - Create repository
        repository = Repository.objects.create(
            url=repository_url,
            name=repository_name,
            description=repository_description,
            is_public=not is_repository_private
        )

        # TODO: STEP 7 - Create branches
        branches = [Branch.objects.create(repository=repository, name=name) for name in names_of_all_branches]

        # TODO: STEP 8 - Process commits of main branch
        main_branch = Branch.objects.filter(repository_id=repository.id, name='main').first()
        compare_url_template = repository_data[COMPARE_URL]
        handle_diff_func = handle_private_diff if is_repository_private else handle_public_diff
        sha_of_previous_commit = '0000000000000000000000000000000000000000'
        for commit_data in commits_data:

            # Adding missing values because payloads are different
            commit_data['id'] = commit_data['sha']
            commit_data['message'] = commit_data['commit']['message']
            commit_data['timestamp'] = commit_data['commit']['committer']['date']
            commit_data['author']['name'] = commit_data['author']['login']
            commit_data['author']['email'] = "unknown"
            commit_data['added'] = []
            commit_data['removed'] = []
            commit_data['modified'] = []

            handle_commit(
                commit_data=commit_data,
                branch=main_branch,
                sha_of_previous_commit=sha_of_previous_commit,
                compare_url_template=compare_url_template,
                diff_handler_func=handle_diff_func
            )
            sha_of_previous_commit = commit_data['sha']

        # TODO: STEP 9 - Create project
        description = request.data['description']
        is_public = request.data.get('isPublic')
        project = Project.objects.create(name=name, repository=repository, description=description, is_public=is_public,
                                         owner=request.user)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=request.data['id'])
        if project.owner != request.user:
            raise PermissionDenied()
        project.name = request.data['name']
        project.description = request.data['description']
        project.wiki_content = request.data['wiki_content'] if not None else project.wiki_content
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        # Returns project where user is owner or user is in collaborators
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        projects = Project.objects.filter(Q(collaborators__id=request.user.id) | Q(owner=request.user))
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def star(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        project.stars.add(request.user)
        return Response()

    @action(detail=True)
    def removeStar(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=kwargs.get('pk'))
        project.stars.remove(request.user)
        return Response()

    @action(detail=False, permission_classes=[AllowAny])
    def getTopFive(self, *args, **kwargs):
        projects = Project.objects.filter(is_public=True).annotate(star_count=Count('stars')).order_by('-star_count')[
                   :5]
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[AllowAny])
    def search(self, *args, **kwargs):
        search_param = self.request.query_params.get("value")
        projects = Project.objects.filter(name__contains=search_param, is_public=True).annotate(
            star_count=Count('stars')).order_by('-star_count')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all()
    serializer_class = InviteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.data.get('username'))

        if user == request.user:
            raise ValidationError("You cannot invite yourself")

        project = get_object_or_404(Project, id=request.data.get('projectId'))
        if project.owner.id != request.user.id:
            raise ValidationError("You are not owner of the project")

        invite = Invite.objects.create(user=user, project=project)
        serializer = InviteSerializer(invite)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        invite = get_object_or_404(Invite, pk=kwargs.get('pk'))
        if invite.user_id != request.user.id:
            raise ValidationError(code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        invite.project.collaborators.add(invite.user)
        invite.delete()
        return Response()
