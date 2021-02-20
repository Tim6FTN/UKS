import { useRouter } from "next/router";
import { useContext, useEffect } from "react";
import { useState } from "react";
import ProjectWrapper from "../../../../../components/project/wrapper";
import { ProjectContext } from "../../../../../contexts/projectContext";
import MilestoneService from "../../../../../services/milestoneService";

const MilestoneEdit = () => {
  const [milestone, setMilestone] = useState({
    title: "",
    description: "",
    due_date: "2021-02-21",
    label_ids: [],
    project_id: "",
  });
  const router = useRouter();

  const { project } = useContext(ProjectContext);
  useEffect(() => {
    const getResponse = async (milestoneId) => {
      try {
        const milestoneResponse = await MilestoneService.get(
          project.id,
          milestoneId
        );
        setMilestone({
          title: milestoneResponse.data.title,
          description: milestoneResponse.data.description,
          due_date: milestoneResponse.data.due_date,
          label_ids: milestoneResponse.data.labels.map((label) => label.id),
          project_id: project.id,
        });
      } catch (error) {
        alert(error);
      }
    };
    if (router.query.milestoneId && project.id)
      getResponse(router.query.milestoneId);
  }, [router.query.milestoneId, project.id]);

  const handleTextChange = (name) => (event) => {
    setMilestone({ ...milestone, [name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    await MilestoneService.update(
      project.id,
      router.query.milestoneId,
      milestone
    );
    router.push(`/project/${project.id}/milestone`);
  };

  const handleSetLabels = (event) => {
    const labelIds = Array.from(
      event.target.selectedOptions,
      (option) => +option.value
    );
    const selectedLabels = project.labels.filter((label) =>
      labelIds.includes(label.id)
    );
    setMilestone({
      ...milestone,
      label_ids: selectedLabels.map((label) => label.id),
    });
  };

  return (
    <>
      <ProjectWrapper>
        <form onSubmit={handleSubmit} className="mt-2">
          <div className="d-flex justify-content-between">
            <h2>Edit milestone</h2>
            <input className="btn btn-success" type="submit" value="Submit" />
          </div>
          <div className="form-row mt-2">
            <div className="col">
              <input
                className="form-control"
                value={milestone.title}
                onChange={handleTextChange("title")}
                placeholder="Title"
                required
              />
            </div>
            <div className="col">
              <input
                className="form-control"
                type="date"
                value={milestone.due_date}
                onChange={handleTextChange("due_date")}
                id="example-date-input"
              />
            </div>
          </div>

          <div className="form-row mt-2">
            <div className="col">
              <textarea
                className="form-control"
                value={milestone.description}
                onChange={handleTextChange("description")}
                rows={5}
                placeholder="Description..."
              ></textarea>
            </div>
            <div className="col">
              <select
                className="custom-select h-100"
                multiple
                onChange={handleSetLabels}
                value={milestone.label_ids}
              >
                {project.labels?.map((label) => (
                  <option key={label.id} value={label.id}>
                    {label.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </form>
      </ProjectWrapper>
    </>
  );
};

export default MilestoneEdit;
