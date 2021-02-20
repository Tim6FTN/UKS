import axios from "axios";

const milestoneUrl = (projectId) =>
  `${process.env.API_URL}/project/${projectId}/milestone/`;

const getAll = async (projectId) =>
  await axios.get(`${milestoneUrl(projectId)}`, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  });

const get = async (projectId, milestoneId) =>
  await axios.get(`${milestoneUrl(projectId)}${milestoneId}`, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  });

const create = async (projectId, milestone) =>
  await axios.post(`${milestoneUrl(projectId)}`, milestone, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  });
const update = async (projectId, milestoneId, milestone) =>
  await axios.put(`${milestoneUrl(projectId)}${milestoneId}/`, milestone, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  });

const remove = async (projectId, milestoneId) =>
  await axios.delete(`${milestoneUrl(projectId)}${milestoneId}`, {
    headers: {
      Authorization: `Token ${localStorage.getItem("token")}`,
    },
  });

const MilestoneService = {
  get,
  getAll,
  create,
  remove,
  update,
};

export default MilestoneService;
