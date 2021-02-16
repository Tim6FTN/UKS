import { useState, createContext, useEffect } from "react";
import ProjectService from "../services/projectService";

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

export const ProjectContext = createContext(emptyProject);

export const ProjectProvider = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [project, setProject] = useState(emptyProject);
  const [unauthorized, setUnauthorized] = useState(false);

  useEffect(() => {
    if (project) localStorage.setItem("project", JSON.stringify(project));
  }, [project]);

  useEffect(() => {
    setProject(JSON.parse(localStorage.getItem("project")));
  }, []);

  const updateProject = (newProject) => {
    setProject({ ...newProject });
    localStorage.setItem("project", JSON.stringify({ ...newProject }));
  };

  const removeProject = () => {
    setProject(emptyProject);
  };

  const getProject = async (id) => {
    setLoading(true);
    try {
      const projectResponse = await ProjectService.getById(id);
      updateProject(projectResponse.data);
    } catch (error) {
      if (error?.response?.status === 403) {
        setUnauthorized(true);
      } else {
        console.log(error);
      }
    }
    setLoading(false);
  };

  return (
    <ProjectContext.Provider
      value={{ unauthorized, loading, project, getProject, removeProject }}
    >
      {children}
    </ProjectContext.Provider>
  );
};
