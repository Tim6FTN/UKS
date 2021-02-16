import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Container from "../../../components/util/container";
import Navbar from "../../../components/util/navbar";
import withAuth from "../../../components/util/withAuth";
import ProjectService from "../../../services/projectService";

const EditRepository = () => {
  const [project, setProject] = useState({ name: "", description: "" });
  const router = useRouter();

  useEffect(() => {
    if (router.query.id)
      ProjectService.getById(router.query.id).then((response) =>
        setProject(response.data)
      );
  }, [router.query.id]);

  const handleSubmit = (event) => {
    event.preventDefault();
    ProjectService.update(router.query.id, project).then((response) => {
      if (response.status === 200) router.push(`/project/${router.query.id}`);
    });
  };
  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <span>Project name</span>
          <input
            className="form-control"
            value={project.name}
            onChange={(event) =>
              setProject({ ...project, name: event.target.value })
            }
          />
        </div>

        <div className="form-group">
          <span>Description</span>
          <textarea
            className="form-control"
            rows={10}
            value={project.description}
            onChange={(event) =>
              setProject({ ...project, description: event.target.value })
            }
          />
        </div>

        <input type="submit" className="btn btn-success" value="Submit" />
      </form>
    </div>
  );
};

export default withAuth(EditRepository);
