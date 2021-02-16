import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import NavBar from '../../../../components/util/navbar';
import Container from "../../../../components/util/container";
import ProjectWrapper from '../../../../components/project/wrapper';
import TaskList from '../../../../components/task/list';
import withAuth from '../../../../components/util/withAuth';
import TaskService from '../../../../services/taskService';
import Link from 'next/link';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [projectId, setProjectId] = useState(null);
  const router = useRouter();


  useEffect(() => {
    if (router.query.id) {
      getTasks(projectId)
      setProjectId(router.query.id);
    }
  }, [router.query.id]);

  const getTasks = async (projectId) => {
    const newTasks = (await TaskService.getAll(projectId)).data;
    setTasks(newTasks);
  };

  return (
    <>
      <NavBar />
      <Container>
        <ProjectWrapper>
        <div className='row'>
          <h1 className='ml-3'>Tasks</h1>
          <Link href={`/project/${projectId}/task/new`}>
            <a className='mx-2 font-weight-bold ml-auto my-auto'>Create task</a>
          </Link>
          </div>
          {tasks && <TaskList tasks={tasks} projectId={projectId}/>}
        </ProjectWrapper>
      </Container>
    </>
  );
};

export default withAuth(Tasks);
