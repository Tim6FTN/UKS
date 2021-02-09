import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import ProjectService from "../../../services/projectService";
import Form from "../../../components/project/form";
import Navbar from '../../../components/util/navbar'

const EditProject = (props) => {
  const router = useRouter();
  const [project, setProject] = useState();

  useEffect(async () => {
    if (router.query.id) {
      const project = await ProjectService.getById(router.query.id);
      if (project) setProject(project);
    }
  }, [router.query.id]);

  const onSubmit = async () => {
    await ProjectService.update(project);
    router.push("/project");
  };
  return (
    <>
      <Navbar />
      {project && (
        <Form project={project} setProject={setProject} onSubmit={onSubmit} />
      )}
    </>
  );
};

export default EditProject;
