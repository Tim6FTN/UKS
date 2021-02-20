import { useContext, useState, useEffect } from "react";
import { ProjectContext } from "../../../../../contexts/projectContext";
import { useRouter } from "next/router";
import ProjectWrapper from "../../../../../components/project/wrapper";
import MilestoneService from "../../../../../services/milestoneService";
import LittleLabel from "../../../../../components/task/littleLabel";
import Link from "next/link";

const Milestone = () => {
  const [milestone, setMilestone] = useState(null);
  const [milestoneId, setMilestoneId] = useState(null);
  const { project } = useContext(ProjectContext);
  const router = useRouter();

  useEffect(() => {
    if (router.query.milestoneId && router.query.id) {
      getMilestone(router.query.id, router.query.milestoneId);
    }
  }, [router.query.milestoneId, router.query.id]);

  const getMilestone = async (paramProjectId, paramMilestoneId) => {
    const newMilestone = (
      await MilestoneService.get(paramProjectId, paramMilestoneId)
    ).data;
    setMilestone(newMilestone);
    setMilestoneId(paramMilestoneId);
  };

  const handleDelete = async () => {
    await MilestoneService.remove(project.id, milestoneId);
    router.push(`/project/${project.id}/milestone`);
  };

  return (
    <>
      <ProjectWrapper>
        {milestone && (
          <div className="row">
            <div className="col">
              <div className="card">
                <div className="card-body">
                  <div className="card-title d-flex justify-content-between align-items-center">
                    <div className="col-sm-4">
                      <p className="h3">{milestone.title}</p>
                    </div>
                    <div className="col-sm-2">
                      <div className="row">
                        <span className="h5">Start date:</span>
                      </div>
                      <div className="row">
                        <span>{milestone.start_date}</span>
                      </div>
                    </div>
                    <div className="col-sm-2">
                      <div className="row">
                        <span className="h5">Due date</span>
                      </div>
                      <div className="row">
                        <span>{milestone.due_date}</span>
                      </div>
                    </div>

                    <Link
                      className="ml-auto"
                      href={`/project/${project.id}/milestone/${milestoneId}/edit`}
                    >
                      <button
                        type="button"
                        className="btn btn-secondary"
                        style={{ minWidth: "80px" }}
                      >
                        Edit
                      </button>
                    </Link>
                    <button
                      type="button"
                      className="btn btn-danger"
                      onClick={handleDelete}
                    >
                      Delete
                    </button>
                  </div>
                  <div className="card-text">
                    <hr />
                    <div className="ml-2">{milestone.description}</div>
                    {milestone.labels && milestone.labels.length > 0 && (
                      <div className="row">
                        <div className="col-sm-12">
                          <span className="h5">Labels</span>
                        </div>
                        <div className="row">
                          <div className="col-sm-12">
                            {milestone.labels.map((label) => (
                              <LittleLabel
                                key={label.id}
                                name={label.name}
                                color={label.color}
                              ></LittleLabel>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                    <hr />
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="col card mt-2">
          {milestone?.task_set && milestone.task_set.length > 0 && (
            <>
              <h4 className="text-center mt-2">Tasks</h4>

              {milestone.task_set.map((task) => (
                <div key={task.id}>
                  <div className="d-flex justify-content-between align-items-center">
                    <Link href={`/project/${project.id}/task/${task.id}`}>
                      <a
                        className="mt-2 font-weight-bold"
                        style={{ textDecorationLine: "none" }}
                      >
                        {task.title}
                      </a>
                    </Link>
                    <span
                      className={`badge badge-pill px-2 py-1 ${
                        task.state === "Open" ? "bg-info" : "bg-danger"
                      }`}
                    >
                      {task.state}
                    </span>
                  </div>
                  <hr />
                </div>
              ))}
            </>
          )}
        </div>
      </ProjectWrapper>
    </>
  );
};

export default Milestone;
