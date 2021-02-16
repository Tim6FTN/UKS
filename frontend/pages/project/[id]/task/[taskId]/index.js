import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import NavBar from '../../../../../components/util/navbar';
import Container from '../../../../../components/util/container';
import ProjectWrapper from '../../../../../components/project/wrapper';

const Task = () => {
  const [taskId, setTaskId] = useState(null);
  const router = useRouter();
  useEffect(() => {
    if (router.query.taskId) {
      setTaskId(router.query.taskId);
    }
  }, [router.query.taskId]);

  return (
    <>
      <NavBar />
      <Container>
        <ProjectWrapper>
          <h3>RIPPP{taskId}</h3>
        </ProjectWrapper>
      </Container>
    </>
  );
};

export default Task;
