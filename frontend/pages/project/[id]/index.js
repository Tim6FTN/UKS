import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import ProjectWrapper from "../../../components/project/wrapper";
import Container from "../../../components/util/container";
import Navbar from "../../../components/util/navbar";
import ProjectService from "../../../services/projectService";

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
  useEffect(async () => {
    if (router.query.id) {
      try {
        const projectResponse = await ProjectService.getById(router.query.id);
        if (projectResponse.data) {
          setProject(projectResponse.data);
        }
      } catch (error) {
        console.log(error);
        if (error.response.status === 403) {
          router.push("/");
        }
      }
    }
  }, [router.query.id]);

  return (
    <>
      <Navbar />
      <Container>
        <ProjectWrapper>
          <ReactMarkdown>{project.description}</ReactMarkdown>
        </ProjectWrapper>
      </Container>
    </>
  );
};

export default Project;
