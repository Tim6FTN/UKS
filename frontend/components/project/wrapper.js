import { useRouter } from "next/router";
import { useContext, useEffect, useState } from "react";
import { ProjectContext, ProjectProvider } from "../../contexts/projectContext";
import { UserContext } from "../../contexts/userContext";

import ProjectService from "../../services/projectService";
import ProjectNavbar from "../util/ProjectNavbar";

const ProjectWrapper = ({ children }) => {
  const router = useRouter();

  const { project, loading, getProject, unauthorized } = useContext(
    ProjectContext
  );
  const { user } = useContext(UserContext);

  const [starColor, setStarColor] = useState("black");
  useEffect(async () => {
    if (router.query.id) {
      getProject(router.query.id);
    }
  }, [router.query.id]);

  if (unauthorized) {
    router.push("/");
  }

  const tryDelete = () => {
    if (window.confirm("Are you sure you want to delete this project?"))
      ProjectService.remove(project.id).then(() => router.push("/project"));
  };

  useEffect(() => {
    if (project?.stars.some((proj) => proj.id === user?.id)) {
      setStarColor("orange");
    } else {
      setStarColor("black");
    }
  }, [project, user]);

  const addStar = async () => {
    if (!user) {
      return;
    }
    if (starColor === "black") {
      await ProjectService.addStar(project.id);
    } else {
      await ProjectService.removeStar(project.id);
    }
    getProject(router.query.id);
  };

  return (
    <>
      <ProjectNavbar
        project={project}
        tryDelete={tryDelete}
        addStar={addStar}
        starColor={starColor}
        loading={loading}
        route={router.route}
      />
      {children}
    </>
  );
};

export default ProjectWrapper;
