import { useState } from "react";
import { useRouter } from "next/router";
import Navbar from "../../../components/util/navbar";
import Container from "../../../components/util/container";
import withAuth from "../../../components/util/withAuth";
import ProjectWrapper from "../../../components/project/wrapper";
import InviteService from "../../../services/inviteService";

const Invite = () => {
  const [username, setUsername] = useState("");
  const router = useRouter();
  const [message, setMessage] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await InviteService.create({
        username: username,
        projectId: router.query.id,
      });
      setMessage(`Invite sent to ${username}`);
    } catch (error) {
      if (error?.response.status === 404) {
        setMessage("User not found");
      } else if (error?.response.status === 400) {
        setMessage(error.response.data);
      }
    }
  };

  return (
    <div>
      <ProjectWrapper>
        <div className="w-50 mt-3">
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="col">
                <input
                  className="form-control"
                  value={username}
                  onChange={(event) => {
                    setUsername(event.target.value);
                    setMessage("");
                  }}
                  placeholder="Username"
                  required
                />
              </div>
              <div className="col text-left">
                <input
                  type="submit"
                  className="btn btn-success"
                  value="Invite"
                />
              </div>
            </div>
          </form>
          {message && <p className="row mt-2 ml-1 text-danger">{message}</p>}
        </div>
      </ProjectWrapper>
    </div>
  );
};

export default withAuth(Invite);
