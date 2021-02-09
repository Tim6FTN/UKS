import axios from 'axios'

const url = `${process.env.API_URL}/repository`


const getAll = () =>
  axios.get(`${url}/`)


const getById = repositoryId =>
  axios.get(`${url}/${repositoryId}/`)

const create = repository =>
  axios.post(`${url}/`, repository)


const RepositoryService = {
  getAll,
  getById,
  create
}


export default RepositoryService