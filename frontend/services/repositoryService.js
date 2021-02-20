import axios from "axios";

const repositoryUrl = `${process.env.API_URL}/repository`;

//{ headers: { "Authorization": `Token ${localStorage.getItem('token')}` } }

const getAll = () => axios.get(`${repositoryUrl}/`);

const getById = (repositoryId) =>
  axios.get(`${repositoryUrl}/${repositoryId}/`);

const create = (repository) => axios.post(`${repositoryUrl}/`, repository);

const remove = (id) => axios.delete(`${repositoryUrl}/${id}/`);

const update = (id, repository) => {
  axios.put(`${repositoryUrl}/${id}/`, repository);
};

const RepositoryService = {
  getAll,
  getById,
  create,
  remove,
  update,
};

export default RepositoryService;
