import axios from "axios"

const getAll = () =>
  axios.get("http://localhost:8000/label/")


const create = (label) =>
  axios.post("http://localhost:8000/label/", label);


const remove = (labelId) =>
  axios.delete(`http://localhost:8000/label/${labelId}/`)


const update = (labelId, label) =>
  axios.put(`http://localhost:8000/label/${labelId}/`, label)

const LabelService = {
  getAll,
  create,
  remove,
  update
}

export default LabelService