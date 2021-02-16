# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from project.models import Project
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

        self.assertEqual(len(response.data), 3)
        self.assertEqual('Project1', response.data[0].get('name'))
        self.assertEqual('Project11', response.data[1].get('name'))
        self.assertEqual('Project2', response.data[2].get('name'))

    def test_get_by_id_unauthenticated_public(self):
        response = self.client.get(url_detail(1))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_by_id_unauthenticated_private(self):
        response = self.client.get(url_detail(1))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_by_id_owner(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(url_detail(1))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_by_id_collaborator(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(url_detail(3))
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_create_project_unauthenticated(self):
        response = self.client.post(url_list, data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_project_already_exists(self):
        self.client.login(username="admin", password="admin")
        response = self.client.post(url_list, data={'name': 'Project1'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], 'Project with name Project1 already exists')

    def test_create_project_empty_name(self):
        self.client.login(username="admin", password="admin")
        data = {'name': '', 'repository_url': 'https://github.com/Tim6FTN/UKS'}
        response = self.client.post(url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('name')[0], 'This field may not be blank.')

    def test_create_project_empty_repository(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project3', 'repository_url': ''}
        response = self.client.post(url_list, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('repository_url')[0], 'This field may not be blank.')

    def test_create_project_default_values(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project3', 'repository_url': 'https://github.com/Tim6FTN/UKS'}
        response = self.client.post(url_list, data=data)
        self.assertEqual(response.data.get('owner').get('username'), "admin")
        self.assertEqual(response.data.get('is_public'), True)

    def test_create_project_private(self):
        self.client.login(username="user", password="user")
        data = {'name': 'Project1', 'repository_url': 'https://github.com/Tim6FTN/UKS',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false'}
        response = self.client.post(url_list, data=data)

        self.assertEqual(response.data.get('name'), "Project1")
        self.assertEqual(response.data.get('owner').get('username'), "user")
        self.assertEqual(response.data.get('description'), "DESCRIPTION MARKDOWN")
        self.assertEqual(response.data.get('stars'), [])
        self.assertEqual(False, response.data.get('is_public'))

    def test_update_project_empty_fields(self):
        self.client.login(username="admin", password="admin")
        response = self.client.put(url_detail(1), data={})
        print(response.data)
        self.assertEqual('This field is required.', response.data.get('name')[0])

    def test_update_not_owner(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project11', 'repository_url': 'https://github.com/Tim6FTN/UKS',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(3), data=data)
        self.assertEqual('You do not have permission to perform this action.', str(response.data.get('detail')))
        print(response.data)

    def test_update_unique_name(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project11', 'repository_url': 'https://github.com/Tim6FTN/UKS',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(1), data=data)
        self.assertEqual('Project with name Project11 already exists', response.data[0])

    def test_update_successful(self):
        self.client.login(username="admin", password="admin")
        data = {'name': 'Project123',
                'description': 'DESCRIPTION MARKDOWN', 'is_public': 'false', 'wiki_content': 'wiki'}
        response = self.client.put(url_detail(1), data=data)
        self.assertEqual('Project123', response.data.get('name'))
        self.assertEqual('DESCRIPTION MARKDOWN', response.data.get('description'))
        self.assertEqual(False, response.data.get('is_public'))
        self.assertEqual('wiki', response.data.get('wiki_content'))

    def test_delete_unauthorized(self):
        response = self.client.delete(url_detail(1))
        self.assertEqual('Authentication credentials were not provided.', response.data.get('detail'))

    def test_delete_not_owner(self):
        self.client.login(username="admin", password="admin")
        response = self.client.delete(url_detail(3))
        self.assertEqual('You do not have permission to perform this action.', response.data.get('detail'))

    def test_delete_successful(self):
        self.client.login(username="admin", password="admin")
        response = self.client.delete(url_detail(1))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
