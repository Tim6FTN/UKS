import asyncio
import json
import re

import httpx
import requests
from asgiref.sync import sync_to_async
from django.core.exceptions import SuspiciousOperation
from rest_framework import status

from branch.models import Branch
from commit.models import CommitMetaData
from integration.views import handle_private_diff, handle_public_diff, COMPARE_URL, handle_commit, ADDED, REMOVED, \
    MODIFIED, FILES, ADDITIONS, DELETIONS, CHANGES
from repository.models import Repository

GITHUB_URL = 'http://github.com/'
GITHUB_SECURE_URL = 'https://github.com/'
EMPTY_STRING = ''
SLASH = '/'

API_REPOSITORY_URL = 'https://api.github.com/repos'


class RepositoryImporter:

    def __init__(self, repository_url: str):
        self.__repository_url = repository_url
        self.__owner = str()
        self.__repository_name = str()
        self.__raw_repository_data = dict()
        self.__raw_commits_data = dict()

    def check_if_repository_exists(self):
        repository_response = requests.get(self.__repository_url)
        if repository_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'The repository {self.__repository_url} either does not exist on GitHub, or is private.')

    def __get_repository_data(self):
        if re.match(GITHUB_SECURE_URL, self.__repository_url):
            owner_and_repo_name = re.sub(GITHUB_SECURE_URL, EMPTY_STRING, self.__repository_url)
        elif re.match(GITHUB_URL, self.__repository_url):
            owner_and_repo_name = re.sub(GITHUB_URL, EMPTY_STRING, self.__repository_url)
        else:
            raise SuspiciousOperation(f'The repository URL {self.__repository_url} is invalid.')

        try:
            self.__owner, self.__repository_name = owner_and_repo_name.split(SLASH)
        except ValueError:
            raise SuspiciousOperation(f'The repository URL {self.__repository_url} is invalid.')

        repository_response = requests.get(f'{API_REPOSITORY_URL}{SLASH}{self.__owner}{SLASH}{self.__repository_name}')
        if repository_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'Unable to fetch info for repository {self.__repository_url}.')

        self.__raw_repository_data = json.loads(repository_response.content.decode('utf-8'))

    def __parse_repository_data(self):
        self.__repository_default_branch = self.__raw_repository_data['default_branch']
        self.__repository_name = self.__raw_repository_data['name']
        self.__repository_description = self.__raw_repository_data['description']
        self.__is_repository_public = not self.__raw_repository_data['private']
        self.__branches_url = re.sub('{/branch}', '', self.__raw_repository_data['branches_url'])

    def __fetch_all_branches_data(self):
        branches_response = requests.get(self.__branches_url)
        if branches_response.status_code != status.HTTP_200_OK:
            raise SuspiciousOperation(f'Unable to fetch branches info for repository {self.__repository_url}.')

        self.__raw_branches_data = json.loads(branches_response.content.decode('utf-8'))
        self.__names_of_all_branches = [branch_data['name'] for branch_data in self.__raw_branches_data]

    def __fetch_commits(self):
        for branch_name in self.__names_of_all_branches:
            commits_response = requests.get(f'{API_REPOSITORY_URL}{SLASH}{self.__owner}{SLASH}{self.__repository_name}/commits?sha={branch_name}')
            if commits_response.status_code != status.HTTP_200_OK:
                raise SuspiciousOperation(f'Unable to fetch commit info for main branch of repository {self.__repository_url}.')

            self.__raw_commits_data[branch_name] = json.loads(commits_response.content.decode('utf-8'))

    def __create_repository(self) -> Repository:
        return Repository.objects.create(
            url=self.__repository_url,
            name=self.__repository_name,
            description=self.__repository_description,
            is_public=self.__is_repository_public
        )

    def __create_branches(self, repository: Repository):
        return [Branch.objects.create(repository=repository, name=branch_name) for branch_name in self.__names_of_all_branches]

    def __process_commits(self, repository: Repository, branch_name: str):
        branch = Branch.objects.filter(repository_id=repository.id, name=branch_name).first()
        handle_commit_func = RepositoryImporter.handle_public_commit if self.__is_repository_public else RepositoryImporter.handle_private_commit
        for commit_data in self.__raw_commits_data[branch_name]:

            # Adding missing values because payloads are different
            commit_data['id'] = commit_data['sha']
            commit_data['message'] = commit_data['commit']['message']
            commit_data['timestamp'] = commit_data['commit']['committer']['date']
            commit_data['author']['name'] = commit_data['author']['login']
            commit_data['author']['email'] = "unknown"

            commit_full_data_url = f'{API_REPOSITORY_URL}{SLASH}{self.__owner}{SLASH}{self.__repository_name}{SLASH}commits{SLASH}{commit_data["sha"]}'

            handle_commit(
                commit_data=commit_data,
                branch=branch,
                sha_of_previous_commit='',
                compare_url_template=commit_full_data_url,
                diff_handler_func=handle_commit_func
            )

    @staticmethod
    async def handle_public_commit(commit_data: dict, sha_of_previous_commit: str, compare_url_template: str) -> CommitMetaData:
        diff_files = []
        try:
            async with httpx.AsyncClient() as client:
                diff_response = await asyncio.gather(client.get(compare_url_template))
                if diff_response[0].status_code == httpx.codes.OK:
                    diff_data = diff_response[0].json()
                    diff_files = diff_data[FILES]
        except httpx.RequestError as e:
            print(f'An error occurred while requesting diff on URL {e.request.url!r}.')

        added_files_count, deleted_files_count, modified_files_count = 0, 0, 0
        added_lines_count, deleted_lines_count, modified_lines_count = diff_data['stats']['additions'], diff_data['stats']['deletions'], diff_data['stats']['total']

        try:
            for file in diff_files:
                if file['status'] == 'added':
                    added_files_count += 1
                elif file['status'] == 'deleted':
                    deleted_files_count += 1
                else:
                    modified_lines_count += 1
        except KeyError:
            pass

        return await sync_to_async(CommitMetaData.objects.create)(
            file_additions_count=added_files_count,
            file_deletions_count=deleted_files_count,
            file_modifications_count=modified_files_count,
            line_additions_count=added_lines_count,
            line_deletions_count=deleted_lines_count,
            line_modifications_count=modified_lines_count
        )

    @staticmethod
    async def handle_private_commit(commit_data: dict, *args, **kwargs) -> CommitMetaData:
        return await sync_to_async(CommitMetaData.objects.create)(
            file_additions_count=len(commit_data[ADDED]),
            file_deletions_count=len(commit_data[REMOVED]),
            file_modifications_count=len(commit_data[MODIFIED])
        )

    def import_repository(self) -> Repository:
        self.__get_repository_data()
        self.__parse_repository_data()
        self.__fetch_all_branches_data()
        self.__fetch_commits()
        repository = self.__create_repository()
        branches = self.__create_branches(repository=repository)
        for branch in branches:
            self.__process_commits(repository=repository, branch_name=branch.name)

        return repository
