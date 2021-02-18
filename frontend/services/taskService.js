import axios from 'axios';

const taskUrl = (projectId) => `${process.env.API_URL}/project/${projectId}/task/`;

const getAll = async (projectId) =>
  await axios.get(`${taskUrl(projectId)}`, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const get = async (projectId, taskId) =>
  await axios.get(`${taskUrl(projectId)}${taskId}`, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const create = async (projectId, taskId) =>
  await axios.post(`${taskUrl(projectId)}`, taskId, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const patch = async (projectId, taskId, data) =>
  await axios.patch(`${taskUrl(projectId)}${taskId}/`, data, {
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const openTask = async (projectId, taskId) =>
  await axios.post(`${taskUrl(projectId)}${taskId}/openTask/`, {} ,{
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const closeTask = async (projectId, taskId) =>
  await axios.post(`${taskUrl(projectId)}${taskId}/closeTask/`, {},{
    headers: {
      Authorization: `Token ${localStorage.getItem('token')}`,
    },
  });

const TaskService = {
  get,
  getAll,
  create,
  patch,
  openTask,
  closeTask,
};

export default TaskService;
