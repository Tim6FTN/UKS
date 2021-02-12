import axios from "axios";

const url = `${process.env.API_URL}/project`


const getAll = () => axios.get(`${url}/`);

const getById = async (projectId) => {
  try {
    const projectResponse = await axios.get(
      `${url}/${projectId}/`
    );
    return projectResponse.data;
  } catch (error) {
    alert(error);
    return undefined;
  }
};

const create = (project) =>
  axios
    .post(`${url}/`, project)
    .catch((error) => alert(error));

const remove = (projectId) =>
  axios.delete(`${url}/${projectId}/`);

const update = (project) =>
  axios.put(`${url}/${project.id}/`, project);

const ProjectService = {
  getAll,
  getById,
  create,
  remove,
  update,
};

export default ProjectService;
