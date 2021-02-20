from change.models import Comment
from datetime import datetime
from django.http.request import QueryDict

import pytz
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from label.models import Label
from milestone.models import Milestone
from project.models import Project
from repository.models import Repository
from task.models import Task

def TASK_API(project_id):
  return reverse('task-list', args=(project_id,))


def TASK_INSTANCE_API(project_id, task_id):
  return reverse('task-detail', args=(project_id, task_id,))

def OPEN_TASK_API(project_id, task_id):
  return reverse('task-open_task', args=(project_id, task_id,))

def CLOSE_TASK_API(project_id, task_id):
  return reverse('task-close_task', args=(project_id, task_id,))

def TASK_COMMENTS_API(project_id, task_id):
  return reverse('task-comment', args=(project_id, task_id,))

def CHANGES_API(project_id, task_id):
  return reverse('task-changes', args=(project_id, task_id,))

class TaskTests(APITestCase):

    def setUp(self) -> None:
        admin = User.objects.create_superuser(username="admin", password="admin")
        user = User.objects.create_user(username="user", password="user")
        user2 = User.objects.create_user(username="user2", password="user")

        repository1 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')
        repository2 = Repository.objects.create(url='https://github.com/Tim6FTN/UKS', name='UKS')

        project1 = Project.objects.create(name="Project1", repository=repository1, owner=admin)
        project2 = Project.objects.create(name="Project2", repository=repository2, owner=user)
        project2.collaborators.add(admin)
        project2.collaborators.add(user2)

        milestone1 = Milestone.objects.create(title="Milestone1", description="Milestone Description", project=project1)
        milestone2 = Milestone.objects.create(title="Milestone2", description="Milestone Description", project=project2)

        label1 = Label.objects.create(project=project1, name="backend", color="#111111")
        label2 = Label.objects.create(project=project1, name="frontend", color="#222222")
        label3 = Label.objects.create(project=project1, name="devops", color="#333333")
        label4 = Label.objects.create(project=project2, name="test", color="#444444")
        label5 = Label.objects.create(project=project2, name="feature", color="#555555")


        task1 = Task.objects.create(
          title="Task1", 
          project=project1, 
          author=admin,
          date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
          milestone=milestone1
        )

        task2 = Task.objects.create(
          title="Task2", 
          project=project1, 
          author=admin,
          date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC),
          milestone=milestone2
          )

        task3 = Task.objects.create(
          title="Task3", 
          project=project2, 
          author=user,
          date_opened=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC))
        
        Comment.objects.create(
          change_type = 'Update',
          description = 'New comment created',
          user = user,
          text = 'First task comment',
          task = task1,
          timestamp=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        )

        Comment.objects.create(
          change_type = 'Update',
          description = 'New comment created',
          user = user,
          text = 'Third task comment',
          task = task3,
          timestamp=datetime(2020, 11, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        )

        Comment.objects.create(
          change_type = 'Update',
          description = 'New comment created',
          user = user,
          text = 'Third task second comment',
          task = task3,
          timestamp=datetime(2021, 1, 20, 20, 8, 7, 127325, tzinfo=pytz.UTC)
        )

        task1.labels.add(label1)
        task1.labels.add(label2)

        task2.labels.add(label2)
    
    def test_get_project_tasks(self):
      self.client.login(username='user', password='user')
      response = self.client.get(TASK_API(1))
      self.assertEqual(2, len(response.data))
      self.assertEqual('Task1', response.data[0].get('title'))
      self.assertEqual('Task2', response.data[1].get('title'))

    def test_create_task_unauthorised(self):
      data = QueryDict(mutable=True).update({"title":"NewTask"})
      response = self.client.post(TASK_API(1), data=data)
      self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_task_with_only_title(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask"
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('NotAssigned', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(0, len(createdTask.get('assignees')))
      self.assertIsNone(createdTask.get('labels'))
      self.assertIsNone(createdTask.get('milestone'))


    def test_create_task_with_description(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "description": "Task desc"
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('Task desc', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('NotAssigned', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(0, len(createdTask.get('assignees')))
      self.assertIsNone(createdTask.get('labels'))
      self.assertIsNone(createdTask.get('milestone'))

    def test_create_task_with_priority(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "priority": "High"
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('High', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(0, len(createdTask.get('assignees')))
      self.assertIsNone(createdTask.get('labels'))
      self.assertIsNone(createdTask.get('milestone'))

    def test_try_to_create_task_with_bad_priority(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "priority": "Bad"
      }
      response = self.client.post(TASK_API(2), data=data)
      self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_create_task_with_assignees(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "assignees": ["user", "user2"]
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('NotAssigned', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(2, len(createdTask.get('assignees')))
      self.assertIsNone(createdTask.get('labels'))
      self.assertIsNone(createdTask.get('milestone'))

    def test_create_task_with_milestone(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "milestone": 2
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('NotAssigned', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(0, len(createdTask.get('assignees')))
      self.assertIsNone(createdTask.get('labels'))
      self.assertEqual('Milestone2',createdTask.get('milestoneInfo').get('title'))

    def test_create_task_with_labels(self):
      self.client.login(username='user', password='user')
      data = {
        "title": "NewTask",
        "labels": [4, 5]
      }
      response = self.client.post(TASK_API(2), data=data)
      createdTask = response.data

      self.assertEqual(status.HTTP_201_CREATED, response.status_code)
      self.assertEqual('NewTask', createdTask.get('title'))
      self.assertEqual('user', createdTask.get('author').get('username'))
      self.assertEqual('', createdTask.get('description'))
      self.assertEqual('Open', createdTask.get('state'))
      self.assertIsNone(createdTask.get('date_closed'))
      self.assertEqual('NotAssigned', createdTask.get('priority'))
      self.assertEqual('Backlog', createdTask.get('task_status'))
      self.assertEqual(0, len(createdTask.get('assignees')))
      self.assertEqual(2, len(createdTask.get('labelsInfo')))
      self.assertIsNone(createdTask.get('milestoneInfo'))

    def test_close_task(self):
      self.client.login(username='user', password='user')
      response = self.client.post(CLOSE_TASK_API(2, 3))
      changed_task = response.data

      self.assertEqual(status.HTTP_200_OK, response.status_code)
      self.assertEqual(3, changed_task.get('id'))
      self.assertEqual('Task3', changed_task.get('title'))
      self.assertEqual('Closed', changed_task.get('state'))
      self.assertIsNotNone(changed_task.get('date_closed'))

    def open_task(self):
      self.client.login(username='user', password='user')
      response = self.client.post(CLOSE_TASK_API(2, 3))
      changed_task = response.data

      self.assertEqual(status.HTTP_200_OK, response.status_code)
      self.assertEqual('Closed', changed_task.get('state'))

      second_response = self.client.post(OPEN_TASK_API(2, 3))
      changed_task = second_response.data
      self.assertEqual(status.status.HTTP_200_OK, response.status_code)
      self.assertEqual('Opened', changed_task.get('state'))
      self.assertIsNone(changed_task.get('date_closed'))

    def test_get_tasks_comments(self):
      self.client.login(username='user', password='user')
      response = self.client.get(TASK_COMMENTS_API(2, 3))
      comments = response.data

      self.assertEqual(status.HTTP_200_OK, response.status_code)
      self.assertEqual(2, len(comments))
      self.assertEqual('Third task comment', comments[0].get('text'))
      self.assertEqual('Third task second comment', comments[1].get('text'))

    def test_add_comments_to_task(self):
      self.client.login(username='user', password='user')
      data = {
        'text': 'This is new comment for task'
      }
      response = self.client.post(TASK_COMMENTS_API(2,3), data=data)
      self.assertEqual(status.HTTP_201_CREATED, response.status_code)

      response = self.client.get(TASK_COMMENTS_API(2, 3))
      comments = response.data

      self.assertEqual(status.HTTP_200_OK, response.status_code)
      self.assertEqual(3, len(comments))
      self.assertEqual('Third task comment', comments[0].get('text'))
      self.assertEqual('Third task second comment', comments[1].get('text'))
      self.assertEqual('This is new comment for task', comments[2].get('text'))

    def test_try_to_delete_task(self):
      self.client.login(username='user', password='user')
      response = self.client.delete(TASK_INSTANCE_API(2, 3))
      self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)