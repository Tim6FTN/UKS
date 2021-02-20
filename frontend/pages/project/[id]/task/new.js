import { useState, useEffect, useContext } from 'react';
import ProjectWrapper from '../../../../components/project/wrapper';
import withAuth from '../../../../components/util/withAuth';
import TaskService from '../../../../services/taskService';
import ProjectService from '../../../../services/projectService';
import { useRouter } from 'next/router';
import { ProjectContext } from '../../../../contexts/projectContext';

const TaskForm = () => {
  const [newTask, setNewTask] = useState({});
  const [projectId, setProjectId] = useState(null);
  const {project} = useContext(ProjectContext);
  const priorities = ['Low', 'Medium', 'High'];
  const router = useRouter();

  useEffect(() => {
    if (router.query.id) {
      getInitialData(router.query.id);
    }
  }, [router.query.id]);

  const getInitialData = async (projectParamId) => {
    setProjectId(projectParamId);
  }

  const handleSubmit = async () => {
    console.log(newTask);
    await TaskService.create(projectId, newTask);
    router.push(`/project/${projectId}/task`);
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
      <ProjectWrapper>
        <div className='row'>
          <div className='col-sm-8'>
            <div className='card'>
              <div className='card-body'>
                <div className='card-title'>
                  <p className='h3'>New task</p>
                </div>
                <div className='card-text'>
                  <span>Title: </span>
                  <input
                    type='text'
                    className='form-control mb-4'
                    onChange={handleChange('title')}
                    required></input>
                  <span>Description: </span>
                  <textarea
                    className='form-control'
                    rows='8'
                    onChange={handleChange('description')}></textarea>
                  <div className='text-right mt-3'>
                    <button className='btn btn-primary' onClick={handleSubmit}>
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
              <select className='custom-select' onChange={handleChange('priority')}>
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
              <select className='custom-select' onChange={handleMultiSelect('assignees')} multiple>
                {project?.collaborators &&
                  [project.owner, ...project.collaborators].map((user) => (
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
              <select className='custom-select' onChange={handleMultiSelect('label')} multiple>
                {project?.labels &&
                  project.labels.map((label) => (
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
              <select className='custom-select' onChange={handleSelect('milestone')}>
                <option key='' value=''></option>
                {project?.milestone &&
                  project.milestone.map((milestone) => (
                    <option key={milestone.id} value={milestone.id}>
                      {milestone.title}
                    </option>
                  ))}
              </select>
            </div>
          </div>
        </div>
      </ProjectWrapper>
    </>
  );
};

export default withAuth(TaskForm);
