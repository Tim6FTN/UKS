import axios from 'axios'

const repositoryUrl = `${process.env.API_URL}/repository`
const inviteUrl = `${process.env.API_URL}/invite`

const getAll = () =>
  axios.get(`${repositoryUrl}/`)


const getById = repositoryId =>
  axios.get(`${repositoryUrl}/${repositoryId}/`)

const create = repository =>
  axios.post(`${repositoryUrl}/`, repository)

const remove = id =>
  axios.delete(`${repositoryUrl}/${id}/`)

const invite = invite =>
  axios.post(`${inviteUrl}/`, invite)

const addStar = id =>
  axios.get(`${repositoryUrl}/${id}/star`)

const getTopFive = () =>
  axios.get(`${repositoryUrl}/getTopFive/`)

const update = (id, repository) => {
  axios.put(`${repositoryUrl}/${id}/`, repository)
}

const search = (searchValue) =>
  axios.get(`${repositoryUrl}/search/`, { params: { value: searchValue } })


const RepositoryService = {
  getAll,
  getById,
  create,
  remove,
  update,
  invite,
  addStar,
  getTopFive,
  search
}


export default RepositoryService