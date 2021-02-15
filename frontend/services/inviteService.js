import axios from "axios";

const inviteUrl = `${process.env.API_URL}/invite`;

const create = (invite) =>
  axios.post(`${inviteUrl}/`, invite, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const getAll = () =>
  axios.get(`${inviteUrl}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const accept = (inviteId) =>
  axios.get(`${inviteUrl}/${inviteId}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const decline = (inviteId) =>
  axios.delete(`${inviteUrl}/${inviteId}/`, {
    headers: { Authorization: `Token ${localStorage.getItem("token")}` },
  });

const InviteService = {
  getAll,
  create,
  accept,
  decline,
};

export default InviteService;
