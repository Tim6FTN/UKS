import { useEffect, useState } from "react";
import ProjectService from "../../../../services/projectService";
import Link from "next/link";
import Navbar from '../../../../components/util/navbar'
import Container from "../../../../components/util/container";


const Project = () => {
  const [projects, setProjects] = useState([]);

  useEffect(async () => {
    const responseProjects = await ProjectService.getAll();
    setProjects(responseProjects.data);
  }, []);

  const tryDelete = (projectId) => {
    console.log(projectId);
    if (window.confirm("Are you sure you want to delete this project?"))
      ProjectService.remove(projectId).then((response) =>
        setProjects(projects.filter((project) => project.id != projectId))
      );
  };

  const projectRows = () =>
    projects.map((project, index) => (
      <tr key={index}>
        <td>{project.name}</td>
        <td>{project.description}</td>
        <td>
          <Link href={`/project/${project.id}/edit`}>
            <a className="btn btn-secondary">Edit</a>
          </Link>
        </td>

        <td>
          <button
            className="btn btn-danger"
            onClick={() => tryDelete(project.id)}
          >
            Delete
          </button>
        </td>
      </tr>
    ));
  return (
    <>
      <Navbar />
      <Container>
        <h1>PROJECT</h1>

        <div>
          <Link href="/project/new">
            <a className="btn btn-success">New project</a>
          </Link>
        </div>

        <table className="table">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Description</th>
              <th scope="col"></th>
              <th scope="col">Users</th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>{projectRows()}</tbody>
        </table>
      </Container>
    </>
  );
};

export default Project;
