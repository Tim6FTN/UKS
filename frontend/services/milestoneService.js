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

const MilestoneService = {
  get,
  getAll,
};

export default MilestoneService;
