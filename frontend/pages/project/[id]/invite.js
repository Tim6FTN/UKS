import { useState } from "react";
import { useRouter } from "next/router";
import ProjectService from "../../../services/projectService";
import Navbar from "../../../components/util/navbar";
import Container from "../../../components/util/container";
import withAuth from "../../../components/util/withAuth";
import ProjectWrapper from "../../../components/project/wrapper";

const Invite = () => {
  const [username, setUsername] = useState("");
  const router = useRouter();
  const [message, setMessage] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    ProjectService.invite({
      username: username,
      projectId: router.query.id,
    }).then(() => setMessage(`Invite sent to ${username}`)).catch(() => setMessage('User not found'));
  };

  return (
    <div>
      <Navbar />
      <Container>
        <ProjectWrapper>
          <div className="w-50 mt-3">
            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="col">
                  <input
                    className="form-control"
                    value={username}
                    onChange={(event) => {
                      setUsername(event.target.value)
                      setMessage('')
                    }}
                    placeholder="Username"
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
            {message && <p className="row mt-2 ml-1">{message}</p>}
          </div>
        </ProjectWrapper>
      </Container>
    </div>
  );
};

export default withAuth(Invite);
