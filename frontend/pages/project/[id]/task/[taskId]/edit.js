import { useState, useEffect } from 'react';
import Container from '../../../../../components/util/container';
import NavBar from '../../../../../components/util/navbar';
import ProjectWrapper from '../../../../../components/project/wrapper';
import TaskService from '../../../../../services/taskService';
import { useRouter } from 'next/router';

const EditTask = () => {
  const [newTask, setNewTask] = useState({});
  const [projectId, setProjectId] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [task, setTask] = useState(null);
  const collaborators = [
    {
      id: 1,
      username: 'Author1',
    },
    {
      id: 2,
      username: 'Author2',
    },
    {
      id: 3,
      username: 'Author3',
    },
  ];
  const milestones = [
    {
      id: 1,
      title: 'Milestone1',
    },
    {
      id: 2,
      title: 'Milestone2',
    },
    {
      id: 3,
      title: 'Milestone3',
    },
  ];
  const labels = [
    {
      id: 1,
      name: 'Label1',
    },
    {
      id: 2,
      name: 'Labe2',
    },
    {
      id: 3,
      name: 'Label3',
    },
    {
      id: 4,
      name: 'Label4',
    },
  ];
  const priorities = ['Low', 'Medium', 'High'];
  const router = useRouter();

  useEffect(() => {
    if (router.query.taskId && router.query.id) {
      getTask(router.query.id, router.query.taskId);
    }
  }, [router.query.taskId]);

  const getTask = async (paramProjectId, paramTaskId) => {
    const taskCurrentState = (await TaskService.get(paramProjectId, paramTaskId)).data;
    setTask(taskCurrentState);
    setProjectId(paramProjectId);
    setTaskId(paramTaskId);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(newTask);
    await TaskService.patch(projectId, taskId, newTask);
    router.push(`/project/${projectId}/task/${taskId}`);
  };

  const handleChange = (name) => (e) => {
    setNewTask({ ...newTask, [name]: e.target.value });
  };

  const handleMultiSelect = (name) => (e) => {
    const selectedValues = Array.from(e.target.selectedOptions, (option) => option.value);
    switch (name) {
      case 'assignees':
        setNewTask({ ...newTask, assignees: selectedValues });
        break;
      case 'label':
        setNewTask({ ...newTask, labels: selectedValues.map((val) => +val) });
        break;
      default:
        break;
    }
  };

  const handleSelect = (name) => (e) => {
    const selectedValue = e.target.value;
    switch (name) {
      case 'milestone':
        if (selectedValue === '') {
          const newState = { ...newTask };
          delete newState.milestone;
          setNewTask({ ...newState });
        } else {
          setNewTask({ ...newTask, milestone: +selectedValue });
        }
        break;
      case 'priority':
        setNewTask({ ...newTask, priority: selectedValue });
      default:
        break;
    }
  };

  return (
    <>
      <NavBar />
      <Container>
        <ProjectWrapper>
          {task && (
            <form onSubmit={handleSubmit}>
              <div className='row'>
                <div className='col-sm-8'>
                  <div className='card'>
                    <div className='card-body'>
                      <div className='card-title'>
                        <p className='h3'>Edit task</p>
                      </div>
                      <div className='card-text'>
                        <span>Title: </span>
                        <input
                          type='text'
                          className='form-control mb-4'
                          onChange={handleChange('title')}
                          defaultValue={task.title}
                          required></input>
                        <span>Description: </span>
                        <textarea
                          className='form-control'
                          rows='8'
                          onChange={handleChange('description')}
                          defaultValue={task.description}></textarea>
                        <div className='text-right mt-3'>
                          <button type='submit' className='btn btn-primary'>
                            Submit
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className='col-sm-4'>
                  <div className='row'>
                    <div>Priority</div>
                  </div>
                  <div className='row'>
                    <select
                      className='custom-select'
                      onChange={handleChange('priority')}
                      defaultValue={task.priority}>
                      <option value='NotAssigned'>Not assigned</option>
                      {priorities &&
                        priorities.map((priority) => (
                          <option key={priority} value={priority}>
                            {priority}
                          </option>
                        ))}
                    </select>
                  </div>
                  <div className='row'>
                    <div>Assignee:</div>
                  </div>
                  <div className='row'>
                    <select
                      className='custom-select'
                      onChange={handleMultiSelect('assignees')}
                      defaultValue={task.assignees}
                      multiple>
                      {collaborators &&
                        collaborators.map((user) => (
                          <option key={user.id} value={user.username}>
                            {user.username}
                          </option>
                        ))}
                    </select>
                  </div>
                  <div className='row mt-2'>
                    <div>Labels</div>
                  </div>
                  <div className='row'>
                    <select
                      className='custom-select'
                      onChange={handleMultiSelect('label')}
                      multiple
                      defaultValue={task.labelsInfo.map((label) => label.id)}>
                      {labels &&
                        labels.map((label) => (
                          <option key={label.id} value={label.id}>
                            {label.name}
                          </option>
                        ))}
                    </select>
                  </div>
                  <div className='row mt-2'>
                    <div>Milestone</div>
                  </div>
                  <div className='row'>
                    <select
                      defaultValue={task.milestone}
                      className='custom-select'
                      onChange={handleSelect('milestone')}>
                      <option key='' value=''></option>
                      {milestones &&
                        milestones.map((milestone) => (
                          <option key={milestone.id} value={milestone.id}>
                            {milestone.title}
                          </option>
                        ))}
                    </select>
                  </div>
                </div>
              </div>
            </form>
          )}
        </ProjectWrapper>
      </Container>
    </>
  );
};

export default EditTask;
