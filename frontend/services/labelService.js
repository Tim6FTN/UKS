import axios from "axios";

const labelUrl = (projectId) =>
  `${process.env.API_URL}/project/${projectId}/label`;

const getAll = (projectId) =>
  axios.get(`${labelUrl(projectId)}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const create = (projectId, label) =>
  axios.post(`${labelUrl(projectId)}/`, label, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const remove = (projectId, labelId) =>
  axios.delete(`${labelUrl(projectId)}/${labelId}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const update = (projectId, labelId, label) =>
  axios.put(`${labelUrl(projectId)}/${labelId}/`, label, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const LabelService = {
  getAll,
  create,
  remove,
  update,
};

export default LabelService;
