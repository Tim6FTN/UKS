import axios from "axios";

const url = `${process.env.API_URL}/label`

const getAll = () => axios.get(`${url}/`);

const create = (label) => axios.post(`${url}/`, label);

const remove = (labelId) =>
  axios.delete(`${url}/${labelId}/`);

const update = (label) =>
  axios.put(`${url}/${label.id}/`, label);

const LabelService = {
  getAll,
  create,
  remove,
  update,
};

export default LabelService;
