import axios from "axios";

const getAll = () => axios.get("http://localhost:8000/project/");

//change this
const getById = async (projectId) => {
  try {
    const projectResponse = await axios.get(
      `http://localhost:8000/project/${projectId}/`
    );
    return projectResponse.data;
  } catch (error) {
    alert(error);
    return undefined;
  }
};

const create = (project) =>
  axios
    .post("http://localhost:8000/project/", project)
    .catch((error) => alert(error));

const remove = (projectId) =>
  axios.delete(`http://localhost:8000/project/${projectId}/`);

const update = (project) =>
  axios.put(`http://localhost:8000/project/${project.id}/`, project);

const ProjectService = {
  getAll,
  getById,
  create,
  remove,
  update,
};

export default ProjectService;
