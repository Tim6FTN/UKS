import { useEffect, useState } from "react";

const Form = ({ project, setProject, onSubmit }) => {

  const submitForm = (event) => {
    event.preventDefault();
    onSubmit();
  };
  return (
    <form onSubmit={submitForm}>
      <label>Project board name</label>
      <div className="form-group">
        <input
          type="text"
          className="form-control"
          value={project.name}
          onChange={(event) =>
            setProject({ ...project, name: event.target.value })
          }
          placeholder="Project board name"
        />
      </div>

      <div className="form-group">
        <label>
          Description <span className="text-secondary">(optional)</span>
        </label>
        <textarea
          className="form-control"
          value={project.description}
          onChange={(event) =>
            setProject({ ...project, description: event.target.value })
          }
          rows={5}
        ></textarea>
      </div>

      <div className="form-group">
        <input type="submit" className="btn btn-success" value="Submit" />
      </div>
    </form>
  );
};

export default Form;