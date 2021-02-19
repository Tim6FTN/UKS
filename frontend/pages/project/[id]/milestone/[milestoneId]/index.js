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
  const [projectId, setProjectId] = useState(null);
  const { project } = useContext(ProjectContext);
  const router = useRouter();

  useEffect(() => {
    if (router.query.milestoneId && router.query.id) {
      getMilestone(router.query.id, router.query.milestoneId);
    }
  }, [router.query.milestoneId]);

  const getMilestone = async (paramProjectId, paramMilestoneId) => {
    const newMilestone = (
      await MilestoneService.get(paramProjectId, paramMilestoneId)
    ).data;
    setMilestone(newMilestone);
    setProjectId(paramProjectId);
    setMilestoneId(paramMilestoneId);
  };

  return (
    <>
      <ProjectWrapper>
        {milestone && (
          <div className="row">
            <div className="col-sm-9">
              <div className="card">
                <div className="card-body">
                  <div className="card-title">
                    <p className="h3">{milestone.title}</p>
                  </div>
                  <div className="card-text">
                    <hr />
                    <div className="row ml-1">
                      <div className="col-sm-4">
                        <div className="row">
                          <span className="h5">Start date:</span>
                        </div>
                        <div className="row">
                          <span>{milestone.start_date}</span>
                        </div>
                      </div>
                      <div className="col-sm-4">
                        <div className="row">
                          <span className="h5">Due date</span>
                        </div>
                        <div className="row">
                          <span>{milestone.due_date}</span>
                        </div>
                      </div>
                    </div>
                    <hr />
                    <div className="ml-2">{milestone.description}</div>
                    {milestone.labels && milestone.labels.length > 0 && (
                      <>
                        <hr />
                        <div className="row">
                          <div className="col-sm-12">
                            <span className="h5">Labels</span>
                          </div>
                          <div className="row">
                            <div className="col-sm-12">
                              {milestone.labels.map((label) => (
                                <>
                                  <LittleLabel
                                    key={label.id}
                                    name={label.name}
                                    color={label.color}
                                  ></LittleLabel>
                                </>
                              ))}
                            </div>
                          </div>
                        </div>
                      </>
                    )}
                    <hr />

                    <div className="row">
                      <div className="ml-auto mr-5 mt-3">
                        <Link
                          className="ml-auto"
                          href={`/project/${projectId}/milestone/${milestoneId}/edit`}
                        >
                          <button
                            type="button"
                            className="btn btn-secondary"
                            style={{ minWidth: "80px" }}
                          >
                            Edit
                          </button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-sm-3">
              {milestone.task_set && milestone.task_set.length > 0 && (
                <>
                  <div className="row mt-3">
                    <span className="h5">Tasks:</span>
                  </div>
                  <div className="row">
                    <ul>
                      {milestone.task_set.map((task) => (
                        <li key={task.id}>{task.title}</li>
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

export default Milestone;
