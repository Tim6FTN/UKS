import { faEdit, faStar, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import { useEffect, useState } from "react";

const ProjectNavbar = ({
  project,
  addStar,
  tryDelete,
  starColor,
  loading,
  route,
}) => {
  const [loggedIn, setLoggedIn] = useState(false);
  useEffect(() => {
    setLoggedIn(localStorage.getItem("token"));
  }, []);
  console.log(loggedIn);
  return (
    <>
      <div className="row border-dark border-bottom mb-2">
        <div className="col text-left">
          {!loading && (
            <>
              <span className="h2 pr-2 mr-2 border-dark border-right">
                <FontAwesomeIcon
                  color={starColor}
                  onClick={addStar}
                  icon={faStar}
                  className="ml-2 mr-1"
                  style={{ cursor: "pointer" }}
                />
                <span style={{ display: "inline-block" }}>
                  {project.stars.length}
                </span>
              </span>
              <h2
                style={{ display: "inline-block" }}
              >{`${project.owner.username} - ${project.name}`}</h2>
            </>
          )}
        </div>

        <div className="col text-right h2">
          {loggedIn && (
            <>
              <Link href={`/project/${project.id}/edit`}>
                <FontAwesomeIcon
                  icon={faEdit}
                  className="mr-4"
                  style={{ cursor: "pointer" }}
                />
              </Link>
              <FontAwesomeIcon
                onClick={tryDelete}
                icon={faTrashAlt}
                className="mr-2"
                style={{ cursor: "pointer" }}
                className="text-danger"
              />
            </>
          )}
        </div>
      </div>
      <div className="row nav-tabs mb-2">
        <div
          className={`nav-item nav-link ${
            route == "/project/[id]" ? "active" : ""
          }`}
        >
          <Link href={`/project/${project.id}`}>
            <a style={{ textDecorationLine: "none" }}> Readme </a>
          </Link>
        </div>
        <div
          className={`nav-item nav-link ${
            route == "/project/[id]/code" ? "active" : ""
          }`}
        >
          <Link href={`/project/${project.id}/code`}>
            <a style={{ textDecorationLine: "none" }}> Code </a>
          </Link>
        </div>
        <div
          className={`nav-item nav-link ${
            route == "/project/[id]/tasks" ? "active" : ""
          }`}
        >
          {" "}
          <a style={{ textDecorationLine: "none" }}> Tasks </a>
        </div>
        <div
          className={`nav-item nav-link ${
            route == "/project/[id]/kanban" ? "active" : ""
          }`}
        >
          {" "}
          <a style={{ textDecorationLine: "none" }}> Kanban </a>
        </div>
        <div
          className={`nav-item nav-link ${
            route == "/project/[id]/wiki" ? "active" : ""
          }`}
        >
          {" "}
          <a style={{ textDecorationLine: "none" }}> Wiki </a>
        </div>
        {loggedIn && (
          <div
            className={`nav-item nav-link ${
              route == "/project/[id]/invite" ? "active" : ""
            }`}
          >
            {" "}
            <Link href={`/project/${project.id}/invite`}>
              <a style={{ textDecorationLine: "none" }}> Invite users </a>
            </Link>
          </div>
        )}
        {loggedIn && (
          <div
            className={`nav-item nav-link ${
              route == "/project/[id]/label" ? "active" : ""
            }`}
          >
            {" "}
            <Link href={`/project/${project.id}/label`}>
              <a style={{ textDecorationLine: "none" }}> Labels </a>
            </Link>
          </div>
        )}
      </div>
    </>
  );
};

export default ProjectNavbar;
