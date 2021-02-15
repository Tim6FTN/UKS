import axios from "axios";

const userUrl = `${process.env.API_URL}/user`;

const authUrl = `${process.env.API_URL}/api-token-auth/`;

const getAll = () => axios.get(`${userUrl}/`);

const login = (credentials) => axios.post(authUrl, credentials);

const register = (registerInfo) => axios.post(`${userUrl}/`, registerInfo);

const profile = () =>
  axios.get(`${userUrl}/profile`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const UserService = {
  getAll,
  login,
  register,
  profile,
};

export default UserService;
