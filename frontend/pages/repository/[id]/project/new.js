import { route } from "next/dist/next-server/server/router";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import Form from "../../../../components/project/form";
import Container from "../../../../components/util/container";
import Navbar from "../../../../components/util/navbar";
import ProjectService from "../../../../services/projectService";

const NewProject = () => {
  const emptyProject = {
    id: "",
    name: "",
    description: "",
    repository: "",
  };
  const [project, setProject] = useState(emptyProject);
  const router = useRouter();

  useEffect(() => {
    if (router.query.id) {
      setProject({ ...project, repository: router.query.id })
    }
  }, [router.query.id])

  const onSubmit = async () => {
    const projectResponse = await ProjectService.create(project);
    if (projectResponse) {
      router.push(`/repository/${router.query.id}`);
    }
  };

  return (
    <>
      <Navbar />
      <Container>
        <Form project={project} setProject={setProject} onSubmit={onSubmit} />
      </Container>
    </>
  )
};

export default NewProject;
