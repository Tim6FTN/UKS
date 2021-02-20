import { useState } from "react";

const CommitAdd = ({ handleAdd }) => {
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen((open) => !open);
  };

  const [commit, setCommit] = useState({ hash: "", message: "" });

  const handleChange = (name) => (e) => {
    setCommit({ ...commit, [name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleAdd(commit);
    setCommit({ hash: "", message: "" })
    handleToggle()
  };

  return (
    <div className="my-2">
      <button className="btn btn-primary" onClick={handleToggle}>
        New
      </button>
      {open && (
        <form onSubmit={handleSubmit}>
          <input
            required
            type="text"
            className="form-control my-2"
            value={commit.hash}
            onChange={handleChange("hash")}
            placeholder="hash"
          ></input>

          <textarea
            required
            value={commit.message}
            className="form-control my-2"
            onChange={handleChange("message")}
            placeholder="message"
          ></textarea>
          <button className="btn btn-primary" type='submit'>
            Add
          </button>
        </form>
      )}
    </div>
  );
};

export default CommitAdd;
