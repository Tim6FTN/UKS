import axios from 'axios'

const getAll = () =>
  axios.get("http://localhost:8000/user/")


const UserService = {
  getAll
}

export default UserService