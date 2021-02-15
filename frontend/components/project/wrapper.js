import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import ProjectService from "../../services/projectService";
import ProjectNavbar from "../util/ProjectNavbar";

const ProjectWrapper = ({ children }) => {
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
  const [loading, setLoading] = useState(true);
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
          setLoading(false)
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 403) {
          router.push("/");
        }
      }
    }
  }, [router.query.id]);

  const tryDelete = () => {
    if (window.confirm("Are you sure you want to delete this project?"))
      ProjectService.remove(project.id).then(() => router.push("/project"));
  };

  const addStar = () => {
    if (starColor === "black") {
      ProjectService.addStar(project.id).then(() => {
        setStarColor("orange");
        setProject({ ...project, stars: [...project.stars, {}] });
      });
    }
  };

  return (
    <>
      <ProjectNavbar
        project={project}
        tryDelete={tryDelete}
        addStar={addStar}
        starColor={starColor}
        loading={loading}
        route = {router.route}
      />
      {children}
    </>
  );
};

export default ProjectWrapper;
