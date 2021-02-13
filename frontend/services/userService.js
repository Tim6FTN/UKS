import axios from 'axios'

const url = `${process.env.API_URL}/user`


const getAll = () =>
  axios.get(`${url}/`)


const UserService = {
  getAll
}

export default UserService