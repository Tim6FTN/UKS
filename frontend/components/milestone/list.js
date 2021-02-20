import Link from "next/link";
import LittleLabel from "../task/littleLabel";

const MilestoneList = ({ milestones, projectId }) => {
  return (
    <>
      <ul className="list-group">
        {milestones.map((milestone) => (
          <li className="list-group-item" key={milestone.title}>
            <div className="row">
              <Link href={`/project/${projectId}/milestone/${milestone.id}`}>
                <a
                  className="mt-2 font-weight-bold"
                  style={{ textDecorationLine: "none" }}
                >
                  {milestone.title}
                </a>
              </Link>
              {milestone.labels &&
                milestone.labels.map((label) => (
                  <LittleLabel
                    key={label.id}
                    name={label.name}
                    color={label.color}
                  />
                ))}
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default MilestoneList;
