import axios from 'axios'

const userUrl = `${process.env.API_URL}/user`

const authUrl = `${process.env.API_URL}/api-token-auth/`

const getAll = () =>
  axios.get(`${userUrl}/`)

const login = credentials =>
  axios.post(authUrl, credentials)

const register = registerInfo =>
  axios.post(`${userUrl}/`, registerInfo)

const UserService = {
  getAll,
  login,
  register
}

export default UserService