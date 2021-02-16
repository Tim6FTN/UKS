import { useState } from 'react';
import Container from '../../../../components/util/container';
import NavBar from '../../../../components/util/navbar';
import ProjectWrapper from '../../../../components/project/wrapper';
import withAuth from '../../../../components/util/withAuth';

const TaskForm = () => {
  const [newTask, setNewTask] = useState({});

  return (
    <>
      <NavBar />
      <Container>
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
                    <input type='text' className='form-control mb-4' required></input>
                    <span>Description: </span>
                    <textarea className='form-control' rows='8'></textarea>
                    <div className='text-right mt-3'>
                      <button className='btn btn-primary'>Submit</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className='col-sm-4'>
              <div className='row'>
                <div>Assignee:</div>
              </div>
              <div className='row'>
                <select className='custom-select' multiple>
                  <option>Username1</option>
                  <option>Username2</option>
                  <option>Username3</option>
                  <option>Username3</option>
                </select>
              </div>
              <div className='row mt-2'>
                <div>Labels</div>
              </div>
              <div className='row'>
                <select className='custom-select' multiple>
                  <option>Label</option>
                  <option>Label2</option>
                  <option>Label4</option>
                  <option>Label5</option>
                </select>
              </div>
              <div className='row mt-2'>
                <div>Milestone</div>
              </div>
              <div className='row'>
                <select className='custom-select'>
                  <option>Milestone</option>
                  <option>Milestone2</option>
                  <option>Milestone4</option>
                  <option>Milestone5</option>
                </select>
              </div>
            </div>
          </div>
        </ProjectWrapper>
      </Container>
    </>
  );
};

export default withAuth(TaskForm);
