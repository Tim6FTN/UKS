import { useRouter } from "next/router";
import { useState } from "react";
import Form from "../../components/project/form";
import ProjectService from "../../services/projectService";

const NewProject = () => {
  const emptyProject = {
    id: "",
    name: "",
    description: "",
    users: [],
    isPublic: true,
  };
  const [project, setProject] = useState(emptyProject);
  const router = useRouter();

  const onSubmit = async () => {
    const projectResponse = await ProjectService.create(project);
    if (projectResponse) {
      router.push("/project");
    }
  };

  return <Form project={project} setProject={setProject} onSubmit={onSubmit} />;
};

export default NewProject;
