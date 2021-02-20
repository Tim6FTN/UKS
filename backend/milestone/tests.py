# Create your tests here.
from datetime import datetime

import pytz
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.http import QueryDict

from label.models import Label
from milestone.models import Milestone
from project.models import Project
from repository.models import Repository
from task.models import Task


def milestone_list(project_id):
    return reverse('milestone-list', args=(project_id,))


def milestone_detail(project_id, milestone_id):
    return reverse('milestone-detail', args=(project_id, milestone_id,))


class MilestoneTests(APITestCase):

    def setUp(self) -> None:
        admin = User.objects.create_superuser(username="admin", password="admin")
        user = User.objects.create_user(username="user", password="user")

        repository1 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        repository2 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')

        project1 = Project.objects.create(name="Project1", repository=repository1, owner=admin)
        project2 = Project.objects.create(name="Project2", repository=repository2, owner=user)
        project2.collaborators.add(admin)

        milestone1 = Milestone.objects.create(title="Milestone1", description="Milestone Description", project=project1)
        milestone2 = Milestone.objects.create(title="Milestone2", description="Milestone Description", project=project2)

        label1 = Label.objects.create(project=project1, name="backend", color="#111111")
        label2 = Label.objects.create(project=project1, name="frontend", color="#222222")
        label3 = Label.objects.create(project=project1, name="devops", color="#333333")

        milestone1.labels.add(label1)
        milestone1.labels.add(label2)
        milestone1.labels.add(label3)

        Task.objects.create(title="Task1", project=project1, author=admin,
                            date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        Task.objects.create(title="Task2", project=project1, author=admin,
                            date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        Task.objects.create(title="Task3", project=project1, author=admin,
                            date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))

    def test_get_all_milestones_unauthenticated(self):
        response = self.client.get(milestone_list(1))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_all_milestones_not_project_owner(self):
        self.client.login(username='user', password='user')
        response = self.client.get(milestone_list(1))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_get_all_milestones_owner(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(milestone_list(1))
        self.assertEqual(1, len(response.data))
        self.assertEqual('Milestone1', response.data[0].get('title'))
        self.assertEqual('Milestone Description', response.data[0].get('description'))
        self.assertEqual(datetime.today().strftime('%Y-%m-%d'), response.data[0].get('start_date'))
        self.assertEqual(None, response.data[0].get('due_date'))

    def test_get_all_milestones_collaborator(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(milestone_list(2))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual('Milestone2', response.data[0].get('title'))
        self.assertEqual('Milestone Description', response.data[0].get('description'))
        self.assertEqual(datetime.today().strftime('%Y-%m-%d'), response.data[0].get('start_date'))
        self.assertEqual(None, response.data[0].get('due_date'))

    def test_create_milestone_unauthenticated(self):
        response = self.client.post(milestone_list(1), data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    '''
    def test_create_milestone_name_already_exists(self):
        self.client.login(username="admin", password="admin")
        data = QueryDict(mutable=True).update({"title": "Milestone1", "description": "desc"})
        response = self.client.post(milestone_list(1), data=data)
        self.assertEqual("Milestone with given title already exists", response.data.get('non_field_errors')[0])
    '''

    def test_create_milestone_not_project_owner_or_collaborator(self):
        # Check for collaborators
        self.client.login(username="user", password="user")
        data = {"title": "Milestone123", "description": "desc"}
        response = self.client.post(milestone_list(1), data=data)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    '''
    def test_create_milestone_due_date_validation(self):
        self.client.login(username="admin", password="admin")
        data = QueryDict(mutable=True).update({"title": "Milestone123", "description": "desc", "due_date": "2020-10-10"})
        response = self.client.post(milestone_list(1), data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid due date.', response.data.get('non_field_errors')[0])
    
    def test_create_milestone_successful(self):
        self.client.login(username="admin", password="admin")
        data = QueryDict(mutable=True).update({"title": "Milestone123", "description": "desc", "due_date": "2022-10-10"})
        response = self.client.post(milestone_list(2), data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('Milestone123', response.data.get('title'))
        self.assertEqual('desc', response.data.get('description'))
        self.assertEqual(datetime.today().strftime('%Y-%m-%d'), response.data.get('start_date'))
        self.assertEqual('2022-10-10', response.data.get('due_date'))
        self.assertEqual('2', response.data.get('project_id'))
    '''
    def test_update_milestone_unauthenticated(self):
        response = self.client.put(milestone_detail(1, 1), data={})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_milestone_not_project_owner(self):
        # Check for collaborators
        pass

    def test_update_milestone_due_date_validation(self):
        pass

    def test_delete_milestone_unauthenticated(self):
        response = self.client.delete(milestone_detail(1, 1))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_milestone_not_owner_or_collaborator(self):
        self.client.login(username="user", password="user")
        response = self.client.delete(milestone_detail(1, 1))
        self.assertEqual('You do not have permission to perform this action.', response.data.get('detail'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(1, Milestone.objects.filter(project_id=1).count())

    def test_delete_milestone_successful(self):
        self.client.login(username="admin", password="admin")
        response = self.client.delete(milestone_detail(1, 1))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Milestone.objects.filter(project_id=1).count())
