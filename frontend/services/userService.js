import axios from 'axios'

const url = `${process.env.API_URL}/user`

const authUrl = `${process.env.API_URL}/api-token-auth/`

const getAll = () =>
  axios.get(`${url}/`)

const login = credentials =>
  axios.post(authUrl, credentials)

const register = registerInfo =>
  axios.post()

const UserService = {
  getAll,
  login,
  register
}

export default UserService