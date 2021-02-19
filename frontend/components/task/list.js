import Link from 'next/link';
import LittleLabel from './littleLabel';

const TaskList = ({ tasks, projectId }) => {
  return (
    <>
      <ul className='list-group'>
        {tasks.map((task) => (
          <li className='list-group-item' key={task.title}>
            <div className='row'>
              <Link href={`/project/${projectId}/task/${task.id}`}>
                <a className='mt-2 font-weight-bold' style={{ textDecorationLine: 'none' }}>
                  {task.title}
                </a>
              </Link>
              {task.labelsInfo &&
                task.labelsInfo.map((label) => (
                  <LittleLabel key={label.id} name={label.name} color={label.color} />
                ))}
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default TaskList;
