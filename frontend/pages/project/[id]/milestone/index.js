import Link from "next/link";
import { useContext } from "react";
import { useEffect } from "react";
import { useState } from "react";
import ProjectWrapper from "../../../../components/project/wrapper";
import { ProjectContext } from "../../../../contexts/projectContext";
import MilestoneList from "../../../../components/milestone/list";
import { useRouter } from "next/router";

const Milestone = () => {
  const [milestones, setMilestones] = useState([]);
  const { project } = useContext(ProjectContext);
  const router = useRouter();

  useEffect(() => {
    if (router.query.id) {
      console.log(router.query.id);
    }
  }, []);

  return (
    <>
      <ProjectWrapper>
        <div className="row">
          <h1 className="ml-3">Milestones</h1>
          <Link href={`/project/${project.id}/milestone/new`}>
            <a className="mx-2 font-weight-bold ml-auto my-auto">
              Create milestone
            </a>
          </Link>
        </div>
        {project.milestone && (
          <MilestoneList
            milestones={project.milestone}
            projectId={project.id}
          />
        )}
      </ProjectWrapper>
    </>
  );
};

export default Milestone;
