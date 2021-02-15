import { useState } from "react";
import { useRouter } from "next/router";
import ProjectService from '../../../services/projectService'
import Navbar from "../../../components/util/navbar";
import Container from "../../../components/util/container";
import withAuth from "../../../components/util/withAuth";

const Invite = () => {
  const [username, setUsername] = useState("");
  const router = useRouter();

  const handleSubmit = (event) => {
    event.preventDefault();
    ProjectService.invite({
      username: username,
      projectId: router.query.id,
    }).then(response => router.push(`/project/${router.query.id}`));
  };

  return (
    <div>
      <Navbar />
      <Container>
        <div className="w-50 mx-auto">
          <form className="text-center" onSubmit={handleSubmit}>
            <div className="form-group">
              <input
                className="form-control"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="Username"
              />
            </div>
            <input type="submit" className="btn btn-success" value="Invite" />
          </form>
        </div>
      </Container>
    </div>
  );
};

export default withAuth(Invite);
