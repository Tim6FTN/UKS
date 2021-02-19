import { useContext, useEffect, useState } from "react";
import { useRouter } from "next/router";
import ProjectWrapper from "../../../../components/project/wrapper";
import TaskList from "../../../../components/task/list";
import TaskService from "../../../../services/taskService";
import Link from "next/link";
import { UserContext } from "../../../../contexts/userContext";
import { ProjectContext } from "../../../../contexts/projectContext";

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const router = useRouter();
  const { user } = useContext(UserContext);
  const { project } = useContext(ProjectContext);

  useEffect(() => {
    if (router.query.id) {
      getTasks(router.query.id);
    }
  }, [router.query.id]);

  const getTasks = async (paramProjectId) => {
    const newTasks = (await TaskService.getAll(paramProjectId)).data;
    setProjectId(paramProjectId);
    setTasks(newTasks);
  };

  return (
    <>
      <ProjectWrapper>
        <div className="row">
          <h1 className="ml-3">Tasks</h1>
          {user &&
            (user?.id === project.owner.id ||
              project?.collaborators?.some((collab) => collab.id == user.id)) && (
              <Link href={`/project/${project.id}/task/new`}>
                <a className="mx-2 font-weight-bold ml-auto my-auto">
                  Create task
                </a>
              </Link>
            )}
        </div>
        {tasks && <TaskList tasks={tasks} projectId={project.id} />}
      </ProjectWrapper>
    </>
  );
};

export default Tasks;