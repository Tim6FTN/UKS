# Create your tests here.
from unittest.mock import MagicMock

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from integration.importer import RepositoryImporter
from project.models import Project, Invite
from repository.models import Repository

url_list = reverse('project-list')


def url_detail(project_id):
    return reverse('project-detail', args=(project_id,))


class ProjectTests(APITestCase):

    def setUp(self) -> None:
        admin = User.objects.create_superuser(username="admin", password="admin")
        user = User.objects.create_user(username="user", password="user")
        repository1 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        repository2 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        repository3 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')

        project1 = Project.objects.create(name="Project1", repository=repository1, owner=admin, is_public=False)
        project11 = Project.objects.create(name="Project11", repository=repository3, owner=admin)
        project2 = Project.objects.create(name="Project2", repository=repository2, owner=user)
        project2.collaborators.add(admin)

    def test_get_all_unauthenticated(self):
        response = self.client.get(url_list)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(url_list)

        project_names = ["Project1", "Project11", "Project2"]
        self.assertEqual(len(response.data), 3)
        self.assertIn(response.data[0].get('name'), project_names)
        self.assertIn(response.data[1].get('name'), project_names)
        self.assertIn(response.data[2].get('name'), project_names)

    def test_get_by_id_unauthenticated_public(self):
        project = Project.objects.get(name="Project1")
        response = self.client.get(url_detail(project.id))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_by_id_unauthenticated_private(self):
        project = Project.objects.get(name="Project1")
        response = self.client.get(url_detail(project.id))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_by_id_owner(self):
        project = Project.objects.get(name="Project1")
        self.client.login(username="admin", password="admin")
        response = self.client.get(url_detail(project.id))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_by_id_collaborator(self):
        project = Project.objects.get(name="Project2")
        self.client.login(username="admin", password="admin")
        response = self.client.get(url_detail(project.id))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_project_unauthenticated(self):
        response = self.client.post(url_list, data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_project_already_exists(self):
        self.client.login(username="admin", password="admin")
        response = self.client.post(url_list, data={'name': 'Project1'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Project with name Project1 already exists')

    '''
    def test_create_project_empty_name(self):
        self.client.login(username="admin", password="admin")
        data = {'name': '', 'repositoryUrl': 'https://github.com/Tim6FTN/JSD'}
        response = self.client.post(url_list, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('name')[0], 'This field may not be blank.')
    '''

    def test_create_project_empty_repository(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project3', 'repositoryUrl': ""}
        response = self.client.post(url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Invalid input.')

    '''
    def test_create_project_default_values(self):
        repository_url = "https://github.com/Tim6FTN/JSD"
        repository = Repository.objects.create(url=repository_url, name="REPOSITORY", description="DESC",
                                               is_public=True)
        repository_importer = RepositoryImporter(repository_url)
        repository_importer.check_if_repository_exists = MagicMock(return_value=True)
        repository_importer.import_repository = MagicMock(return_value=repository)

        self.client.login(username="admin", password="admin")
        data = {'name': 'Project3', 'repositoryUrl': repository_url}
        response = self.client.post(url_list, data=data)
        self.assertEqual(response.data.get('owner').get('username'), "admin")
        self.assertEqual(response.data.get('is_public'), True)

    def test_create_project_private(self):
        repository_url = "https://github.com/Tim6FTN/JSD"
        repository = Repository.objects.create(url=repository_url, name="REPOSITORY", description="DESC",
                                               is_public=True)
        repository_importer = RepositoryImporter(repository_url)
        repository_importer.check_if_repository_exists = MagicMock(return_value=True)
        repository_importer.import_repository = MagicMock(return_value=repository)

        self.client.login(username="user", password="user")
        data = {'name': 'Project1', 'repositoryUrl': repository_url,
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false'}
        response = self.client.post(url_list, data=data)

        self.assertEqual(response.data.get('name'), "Project1")
        self.assertEqual(response.data.get('owner').get('username'), "user")
        self.assertEqual(response.data.get('description'), "DESCRIPTION MARKDOWN")
        self.assertEqual(response.data.get('stars'), [])
        self.assertEqual(False, response.data.get('is_public'))
    '''

    def test_update_project_empty_fields(self):
        project = Project.objects.get(name="Project1")
        self.client.login(username="admin", password="admin")
        response = self.client.put(url_detail(project.id), data={})
        self.assertEqual('This field is required.', response.data.get('name')[0])

    def test_update_not_owner(self):
        project = Project.objects.get(name="Project2")
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project11', 'repository_url': 'https://github.com/Tim6FTN/JSD',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(project.id), data=data)
        self.assertEqual('You do not have permission to perform this action.', str(response.data.get('detail')))

    def test_update_unique_name(self):
        project = Project.objects.get(name="Project1")
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project11', 'repository_url': 'https://github.com/Tim6FTN/JSD',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(project.id), data=data)
        self.assertEqual('Project with name Project11 already exists', response.data[0])

    def test_update_successful(self):
        project = Project.objects.get(name="Project1")
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project123',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(project.id), data=data)
        self.assertEqual('Project123', response.data.get('name'))
        self.assertEqual('DESCRIPTION MARKDOWN', response.data.get('description'))
        self.assertEqual(False, response.data.get('is_public'))
        self.assertEqual('wiki', response.data.get('wiki_content'))

    def test_delete_unauthorized(self):
        response = self.client.delete(url_detail(1))
        self.assertEqual('Authentication credentials were not provided.', response.data.get('detail'))

    def test_delete_not_owner(self):
        project = Project.objects.get(name="Project2")
        self.client.login(username="admin", password="admin")
        response = self.client.delete(url_detail(project.id))
        self.assertEqual('You do not have permission to perform this action.', response.data.get('detail'))

    def test_delete_successful(self):
        project = Project.objects.get(name="Project1")
        self.client.login(username="admin", password="admin")
        response = self.client.delete(url_detail(project.id))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


invite_url = reverse('invite-list')


def invite_url_detail(invite_id):
    return reverse('invite-detail', args=(invite_id,))


class InviteTest(APITestCase):
    def setUp(self) -> None:
        admin = User.objects.create_superuser(username="admin", password="admin")
        user = User.objects.create_user(username="user", password="user")
        repository1 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        project1 = Project.objects.create(name="Project1", repository=repository1, owner=admin, is_public=False)
        invite = Invite.objects.create(user=user, project=project1)

    def test_get_all_invites_unauthenticated(self):
        response = self.client.get(invite_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_all_invites(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(invite_url)
        self.assertEqual(0, len(response.data))

    def test_get_all_invites2(self):
        self.client.login(username="user", password="user")
        response = self.client.get(invite_url)
        self.assertEqual(1, len(response.data))
        self.assertEqual('user', response.data[0].get('user').get('username'))

    def test_accept_invite_forbidden(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(invite_url_detail(1))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_accept_invite_successful(self):
        invite = Invite.objects.all().first()
        self.client.login(username="user", password="user")
        response = self.client.get(invite_url_detail(invite.id))
        project = Project.objects.get(name="Project1")
        self.assertEqual('user', project.collaborators.all()[0].username)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_decline_invite_forbidden(self):
        invite = Invite.objects.all().first()
        self.client.login(username="admin", password="admin")
        response = self.client.delete(invite_url_detail(invite.id))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_decline_invite_successful(self):
        invite = Invite.objects.all().first()
        project = Project.objects.get(name="Project1")
        self.client.login(username="user", password="user")
        response = self.client.delete(invite_url_detail(invite.id))
        self.assertEqual(0, len(project.collaborators.all()))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_invite(self):
        invite = Invite.objects.all().first()
        self.client.login(username="admin", password="admin")
        response = self.client.put(invite_url_detail(invite.id), data={})
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
