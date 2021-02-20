import Link from "next/link";
import LittleLabel from "./littleLabel";

const TaskList = ({ tasks, projectId }) => {
  return (
    <>
      <ul className="list-group">
        {tasks.map((task) => (
          <li className="list-group-item" key={task.title}>
            <div className="row ml-1">
              <Link href={`/project/${projectId}/task/${task.id}`}>
                <a
                  className="font-weight-bold"
                  style={{ textDecorationLine: "none" }}
                >
                  {task.title}
                </a>
              </Link>
              {task.labelsInfo &&
                task.labelsInfo.map((label) => (
                  <LittleLabel
                    key={label.id}
                    name={label.name}
                    color={label.color}
                  />
                ))}
                <div style={{flexGrow: 1}}/>
              <div className='mr-2'>{task.state}</div>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default TaskList;
