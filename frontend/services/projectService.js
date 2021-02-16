import axios from "axios";

const projectUrl = `${process.env.API_URL}/project`;

const getAll = () =>
  axios.get(`${projectUrl}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const getById = async (projectId) => {
  const token = localStorage.getItem("token");
  if (token) {
    return axios.get(`${projectUrl}/${projectId}/`, {
      headers: { Authorization: `Token ${localStorage.getItem("token")}` },
    });
  } else {
    return axios.get(`${projectUrl}/${projectId}/`);
  }
};

const create = (project) =>
  axios.post(`${projectUrl}/`, project, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const remove = (projectId) =>
  axios.delete(`${projectUrl}/${projectId}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const update = (projectId, project) =>
  axios.put(`${projectUrl}/${projectId}/`, project, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const addStar = (id) =>
  axios.get(`${projectUrl}/${id}/star`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const removeStar = (id) => {
  return axios.get(`${projectUrl}/${id}/removeStar`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });
};

const getTopFive = () => axios.get(`${projectUrl}/getTopFive/`);

const search = (searchValue) =>
  axios.get(`${projectUrl}/search/`, { params: { value: searchValue } });

const ProjectService = {
  getAll,
  getById,
  create,
  remove,
  update,
  addStar,
  removeStar,
  getTopFive,
  search,
};

export default ProjectService;
