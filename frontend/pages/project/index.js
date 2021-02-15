import { useEffect, useState } from "react";
import RepositoryService from "../../services/repositoryService";
import Link from "next/link";
import Navbar from "../../components/util/navbar";
import Container from "../../components/util/container";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { faBook, faLock } from "@fortawesome/free-solid-svg-icons";
import ProjectService from "../../services/projectService";
import withAuth from "../../components/util/withAuth";

const Projects = () => {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    ProjectService.getAll().then((response) => setProjects(response.data));
  }, []);

  const links = () =>
    projects.map((project) => (
      <tr key={project.id}>
        <td>
          {project.is_public ? (
            <FontAwesomeIcon className="m-2" icon={faBook} size="2x" />
          ) : (
            <FontAwesomeIcon className="m-2" icon={faLock} size="2x" />
          )}
        </td>
        <td>
          <span className="h5">
            <Link key={project.id} href={`/project/${project.id}`}>
              {project.name}
            </Link>
          </span>
        </td>
      </tr>
    ));
  return (
    <>
      <Navbar />
      <Container>
        <div className="row border-dark border-bottom">
          <div className="col text-left">
            <h2>PROJECTS</h2>
          </div>
          <div className="col text-right">
            <Link href="/project/new">
              <button className="btn btn-success">New project</button>
            </Link>
          </div>
        </div>

        <table>
          <tbody>{links()}</tbody>
        </table>
      </Container>
    </>
  );
};

export default withAuth(Projects);
