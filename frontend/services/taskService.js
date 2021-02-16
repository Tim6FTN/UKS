import axios from 'axios';

const taskUrl = (projectId) => `${process.env.API_URL}/project/${projectId}/task/`;

const getAll = async (projectId) =>
  await axios.get(`${taskUrl(projectId)}`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('token')}`,
    },
  });

const create = async (projectId, task) =>
  await axios.post(`${taskUrl(projectId)}`, task, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('token')}`,
    },
  });

const openTask = async (projectId, taskId) =>
  await axios.get(`${taskUrl(projectId)}${taskId}/openTask/`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('token')}`,
    },
  });

const closeTask = async (projectId, taskId) =>
  await axios.get(`${taskUrl(projectId)}${taskId}/closeTask/`, {
    headers: {
      'Authorization': `Token ${localStorage.getItem('token')}`,
    },
  });

const TaskService = {
  getAll,
  create,
  openTask,
  closeTask,
};

export default TaskService;