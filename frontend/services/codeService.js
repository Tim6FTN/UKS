import axios from 'axios'

const branchUrl = `${process.env.API_URL}/branch/`
const commitUrl = `${process.env.API_URL}/commit/`

const getBranches = (repoId) => {
  return axios.get(`${branchUrl}?id=${repoId}`)
}

const createBranch = (repoId, branch) => {
  return axios.post(`${branchUrl}?id=${repoId}`, branch)
}

const getCommits = (branchId) => {
  return axios.get(`${commitUrl}?id=${branchId}`)
}

const createCommit = (branchId, commit) => {
  return axios.post(`${commitUrl}?id=${branchId}`, commit)
}

export default {
  getBranches,
  createBranch,
  getCommits,
  createCommit
};
