import { useRouter } from "next/router";
import { useContext } from "react";
import ReactMarkdown from "react-markdown";
import ProjectWrapper from "../../../components/project/wrapper";
import Container from "../../../components/util/container";
import Navbar from "../../../components/util/navbar";
import { ProjectContext } from "../../../contexts/projectContext";

const Project = () => {
  const router = useRouter();
  const { project, unauthorized } = useContext(ProjectContext);

  if (unauthorized) {
    router.push("/");
  }

  return (
    <>
      <ProjectWrapper>
        <ReactMarkdown>{project?.description}</ReactMarkdown>
      </ProjectWrapper>
    </>
  );
};

export default Project;
