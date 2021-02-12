import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import ProjectService from "../../../../../services/projectService";
import Navbar from '../../../../../components/util/navbar'
import Form from '../../../../../components/project/form'
import Container from "../../../../../components/util/container";

const EditProject = (props) => {
  const router = useRouter();
  const [project, setProject] = useState();

  useEffect(async () => {
    if (router.query.projectId) {
      const project = await ProjectService.getById(router.query.projectId);
      if (project) setProject(project);
    }
  }, [router.query.projectId]);

  const onSubmit = async () => {
    await ProjectService.update(project);
    router.push(`/repository/${project.repository}`);
  };
  return (
    <>
      <Navbar />
      <Container>
        {project && (
          <Form project={project} setProject={setProject} onSubmit={onSubmit} />
        )}
      </Container>
    </>
  );
};

export default EditProject;
