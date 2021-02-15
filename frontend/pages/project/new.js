import { useEffect, useState } from "react";
import RepositoryService from "../../services/repositoryService";
import Navbar from "../../components/util/navbar";
import UserService from "../../services/userService";
import { useRouter } from "next/router";
import Container from "../../components/util/container";
import ProjectService from "../../services/projectService";

const NewRepository = () => {
  const emptyProject = {
    name: "",
    repositoryUrl: "",
    description: "",
    isPublic: true,
  };

  const router = useRouter();
  const [project, setProject] = useState(emptyProject);

  const [error, setError] = useState("");

  const onSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await ProjectService.create(project);
      router.push("/project");
    } catch (error) {
      setError(error?.response?.data);
    }
  };

  const handleChange = (name) => (event) => {
    setError("");
    setProject({ ...project, [name]: event.target.value });
  };
  return (
    <>
      <Navbar />
      <Container>
        <h1>Create a new project</h1>
        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label>Project name</label>
            <input
              type="text"
              className="form-control"
              value={project.name}
              onChange={handleChange("name")}
              required
            />
          </div>
          <div className="form-group">
            <label>Repository URL</label>
            <input
              type="text"
              className="form-control"
              value={project.repositoryUrl}
              onChange={handleChange("repositoryUrl")}
              required
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              className="form-control"
              rows={10}
              value={project.description}
              onChange={handleChange("description")}
            ></textarea>
          </div>

          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              checked={project.isPublic}
              onChange={(event) =>
                setProject({ ...project, isPublic: event.target.checked })
              }
            />
            <label className="form-check-label">Is public?</label>
          </div>
          <div className="form-group">
            <input
              type="submit"
              className="btn btn-success"
              value="Create project"
            />
          </div>
          <div className="text-danger">{error}</div>
        </form>
      </Container>
    </>
  );
};

export default NewRepository;
