import axios from 'axios'

const repositoryUrl = `${process.env.API_URL}/repository`
const inviteUrl = `${process.env.API_URL}/invite`

const getAll = () =>
  axios.get(`${repositoryUrl}/`)


const getById = repositoryId =>
  axios.get(`${repositoryUrl}/${repositoryId}/`)

const create = repository =>
  axios.post(`${repositoryUrl}/`, repository)

const invite = invite =>
  axios.post(`${inviteUrl}/`, invite)

const RepositoryService = {
  getAll,
  getById,
  create,
  invite
}


export default RepositoryService