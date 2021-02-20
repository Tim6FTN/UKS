# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from project.models import Project
from label.models import Label
from repository.models import Repository


class LabelTests(APITestCase):

    empty_project_pk = None
    non_empty_project_pk = None
    no_project_pk = 123456

    def setUp(self) -> None:
        admin = User.objects.create_superuser(username="admin", password="admin")
        repository1 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        repository2 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')

        project1 = Project.objects.create(name="Project1", repository=repository1, owner=admin)
        project2 = Project.objects.create(name="Project2", repository=repository2, owner=admin)

        label1 = Label.objects.create(name='Label1', color='#123456', project=project2)
        label2 = Label.objects.create(name='Label2', color='#123456', project=project2)
        label3 = Label.objects.create(name='Label3', color='#123456', project=project2)

        self.empty_project_pk = project1.pk
        self.non_empty_project_pk = project2.pk
        self.client.login(username='admin', password='admin')

    def test_get_all_unauthenticated(self):
        self.client.logout()
        url = reverse('label-list', args=(self.empty_project_pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_for_project1_empty(self):
        url = reverse('label-list', args=(self.empty_project_pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_all_for_project1_not_empty(self):
        url = reverse('label-list', args=(self.non_empty_project_pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_project_not_found(self):
        url = reverse('label-list', args=(self.no_project_pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_success(self):
        url = reverse('label-list', args=(self.non_empty_project_pk,))
        name = 'new_label'
        color = '#123456'
        response = self.client.post(url, data= {'name': name, 'color': color})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], name)
        self.assertEqual(response.data['color'], color)

    def test_create_alraedy_exists(self):
        url = reverse('label-list', args=(self.non_empty_project_pk,))
        project = Project.objects.get(pk=self.non_empty_project_pk)
        name = 'Label1'
        color = '#123456'
        response = self.client.post(url, data= {'name': name, 'color': color})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], f'Label with name {name} already exists in project {project}')

    def test_create_project_not_found(self):
        url = reverse('label-list', args=(self.no_project_pk,))
        name = 'Label1'
        color = '#123456'
        response = self.client.post(url, data= {'name': name, 'color': color})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_unauthorized(self):
        self.client.logout()
        url = reverse('label-list', args=(self.empty_project_pk,))
        name = 'Label1'
        color = '#123456'
        response = self.client.post(url, data= {'name': name, 'color': color})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

