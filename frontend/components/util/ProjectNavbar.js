import { faEdit, faStar, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import { useRouter } from "next/router";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../../contexts/userContext";

const ProjectNavbar = ({
  project,
  addStar,
  tryDelete,
  starColor,
  loading,
  route,
}) => {
  const router = useRouter();
  const { user } = useContext(UserContext);

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
          {user && user.id == project.owner.id && (
            <>
              <FontAwesomeIcon
                icon={faEdit}
                onClick={() => router.push(`/project/${project.id}/edit`)}
                className="mr-4"
                style={{ cursor: "pointer" }}
              />
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
          <Link href={`/project/${project.id}/task`}>
            <a style={{ textDecorationLine: "none" }}> Tasks </a>
          </Link>
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
            route === "/project/[id]/wiki" ? "active" : ""
          }`}
        >
          {" "}
          <Link href={`/project/${project.id}/wiki`}>
            <a style={{ textDecorationLine: "none" }}> Wiki </a>
          </Link>
        </div>
        {user && user.id == project.owner.id && (
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
        {user && (
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
