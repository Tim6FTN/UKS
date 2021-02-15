import { faEdit, faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import Container from "../../../components/util/container";
import Navbar from "../../../components/util/navbar";
import Link from "next/link";
import ProjectService from "../../../services/projectService";
import withAuth from "../../../components/util/withAuth";

const Project = () => {
  const router = useRouter();
  const emptyProject = {
    name: "",
    owner: {
      id: "",
      username: "",
    },
    description: "",
    repository: "",
    stars: [],
  };
  const [project, setProject] = useState(emptyProject);
  const [starColor, setStarColor] = useState("black");
  useEffect(async () => {
    if (router.query.id) {
      try {
        const projectResponse = await ProjectService.getById(router.query.id);
        if (projectResponse.data) {
          if (
            projectResponse.data.stars.some(
              (user) => user.id === projectResponse.data.owner.id
            )
          )
            setStarColor("orange");
          setProject(projectResponse.data);
        }
      } catch (error) {
        console.log(error)
        if (error.response.status === 403) {
          router.push('/')
        }
      }
    }
  }, [router.query.id]);

  const tryDelete = () => {
    if (window.confirm("Are you sure you want to delete this project?"))
      ProjectService.remove(project.id).then((response) =>
        router.push("/project")
      );
  };

  const addStar = () => {
    if (starColor === "black") {
      ProjectService.addStar(project.id).then((response) => {
        setStarColor("orange");
        setProject({ ...project, stars: [...project.stars, {}] });
      });
    }
  };

  return (
    <>
      <Navbar />
      <Container>
        <div className="d-flex justify-content-center align-items-center">
          <FontAwesomeIcon
            onClick={() => router.push(`/project/${router.query.id}/edit`)}
            icon={faEdit}
            className="mr-2"
            style={{ cursor: "pointer" }}
          />
          <h3 className="text-center">{`${project.owner.username} / ${project.name}`}</h3>
          <FontAwesomeIcon
            color={starColor}
            onClick={addStar}
            icon={faStar}
            className="ml-2 mr-1"
            style={{ cursor: "pointer" }}
          />
          <span>{project.stars.length}</span>
        </div>

        <div className="row bg-light">
          <div className="col text-center">
            <Link href={`/project/${router.query.id}/code`}>
              <a className="btn btn-secondary"> Code </a>
            </Link>
          </div>
          <div className="col text-center">
            <button className="btn btn-secondary"> Tasks </button>
          </div>
          <div className="col text-center">
            <button className="btn btn-secondary"> Kanban </button>
          </div>
          <div className="col text-center">
            <button className="btn btn-secondary"> Wiki </button>
          </div>
          <div className="col text-center">
            <Link href={`/project/${router.query.id}/invite`}>
              <a className="btn btn-secondary"> Invite users </a>
            </Link>
          </div>
          <div className="col text-center">
            <Link href={`/project/${router.query.id}/label`}>
              <a className="btn btn-secondary"> Labels </a>
            </Link>
          </div>
          <div className="col text-center">
            <button className="btn btn-danger" onClick={tryDelete}>
              Delete
            </button>
          </div>
        </div>

        <ReactMarkdown>{project.description}</ReactMarkdown>
      </Container>
    </>
  );
};

export default Project;
