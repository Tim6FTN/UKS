import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import ProjectWrapper from '../../../../../components/project/wrapper';
import TaskService from '../../../../../services/taskService';
import LittleLabel from '../../../../../components/task/littleLabel';
import Link from 'next/link';
import { useContext } from 'react';
import { ProjectContext } from '../../../../../contexts/projectContext';
import { UserContext } from '../../../../../contexts/userContext';

const Task = () => {
  const [task, setTask] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [projectId, setProjectId] = useState(null);
  const { user } = useContext(UserContext);
  const { project } = useContext(ProjectContext);
  const router = useRouter();

  useEffect(() => {
    if (router.query.taskId && router.query.id) {
      getTask(router.query.id, router.query.taskId);
    }
  }, [router.query.taskId]);

  const getTask = async (paramProjectId, paramTaskId) => {
    const newTask = (await TaskService.get(paramProjectId, paramTaskId)).data;
    setTask(newTask);
    setProjectId(paramProjectId);
    setTaskId(paramTaskId);
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat('en', { dateStyle: 'medium', timeStyle: 'medium' }).format(date);
  };

  const handleTaskStateChange = async () => {
    let updatedTask;
    if (task.state === 'Open') {
      updatedTask = (await TaskService.closeTask(projectId, taskId)).data;
    } else {
      updatedTask = (await TaskService.openTask(projectId, taskId)).data;
    }
    setTask(updatedTask);
  };

  return (
    <>
      <ProjectWrapper>
        {task && (
          <div className='row'>
            <div className='col-sm-9'>
              <div className='card'>
                <div className='card-body'>
                  <div className='card-title'>
                    <p className='h3'>{task.title}</p>
                  </div>
                  <div className='card-text'>
                    <hr />
                    <div className='row ml-1'>
                      <div className='col-sm-3'>
                        <div className='row'>
                          <span className='h5'>Author</span>
                        </div>
                        <div className='row'>
                          <span>{task.author.username}</span>
                        </div>
                      </div>
                      <div className='col-sm-4'>
                        <div className='row'>
                          <span className='h5'>Date opened:</span>
                        </div>
                        <div className='row'>
                          <span>{formatDate(task.date_opened)}</span>
                        </div>
                      </div>
                      <div className='col-sm-4'>
                        {task.date_closed && (
                          <>
                            <div className='row'>
                              <span className='h5'>Date closed</span>
                            </div>
                            <div className='row'>
                              <span>{formatDate(task.date_closed)}</span>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                    <hr />
                    <div className='ml-2'>{task.description}</div>
                    {task.labelsInfo && task.labelsInfo.length > 0 && (
                      <>
                        <hr />
                        <div className='row'>
                          <div className='col-sm-12'>
                            <span className='h5'>Labels</span>
                          </div>
                          <div className='row'>
                            <div className='col-sm-12'>
                              {task.labelsInfo.map((label) => (
                                <>
                                  <LittleLabel
                                    key={label.id}
                                    name={label.name}
                                    color={label.color}></LittleLabel>
                                </>
                              ))}
                            </div>
                          </div>
                        </div>
                      </>
                    )}
                    <hr />
                    <div className='row d-flex align-items-center'>
                      <div className='col-sm-4 mt-1'>
                        <span className='h5'>Status:</span>
                        <span>{task.task_status}</span>
                      </div>
                      <div className='col-sm-4 mt-1'>
                        <span className='h5 ml-3 mt-3'>Prioritiy:</span>
                        <span>{task.priority}</span>
                      </div>
                      <div className='col-sm-4'>
                        <span className='h5 ml-3 mt-3'>Milestone:</span>
                        <span>{task.milestoneInfo?.title}</span>
                      </div>
                    </div>
                    <div className='row'>
                      {user &&
                        (user?.id === project.owner.id ||
                          project?.collaborators?.some((collab) => collab.id == user.id)) && (
                          <div className='ml-auto mr-5 mt-3'>
                            <Link
                              className='ml-auto'
                              href={`/project/${projectId}/task/${taskId}/edit`}>
                              <button
                                type='button'
                                className='btn btn-secondary'
                                style={{ minWidth: '80px' }}>
                                Edit
                              </button>
                            </Link>
                          </div>
                        )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className='col-sm-3'>
              <div className='row mt-3'>
                <div className='col-sm-12 text-center'>
                  <h1 style={{ minHeight: '75px' }}>{task.state}</h1>
                </div>
              </div>
              <div className='row'>
                {user &&
                  (user?.id === project.owner.id ||
                    project?.collaborators?.some((collab) => collab.id == user.id)) && (
                    <>
                      {task.state === 'Open' ? (
                        <button
                          type='button'
                          className='btn btn-danger btn-block'
                          onClick={handleTaskStateChange}>
                          Close
                        </button>
                      ) : (
                        <button
                          type='button'
                          className='btn btn-success btn-block'
                          onClick={handleTaskStateChange}>
                          Open
                        </button>
                      )}
                    </>
                  )}
              </div>
              {task.assignees && task.assignees.length > 0 && (
                <>
                  <div className='row mt-3'>
                    <span className='h5'>Assignees:</span>
                  </div>
                  <div className='row'>
                    <ul>
                      {task.assignees.map((user) => (
                        <li key={user}>{user}</li>
                      ))}
                    </ul>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </ProjectWrapper>
    </>
  );
};

export default Task;
