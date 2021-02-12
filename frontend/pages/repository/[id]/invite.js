import { useState } from "react";
import { useRouter } from "next/router";
import RepositoryService from "../../../services/repositoryService";
import Navbar from "../../../components/util/navbar";
import Container from "../../../components/util/container";

const Invite = () => {
  const [username, setUsername] = useState("");
  const router = useRouter();

  const handleSubmit = (event) => {
    event.preventDefault();
    RepositoryService.invite({
      username: username,
      repositoryId: router.query.id,
    });
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

export default Invite;
