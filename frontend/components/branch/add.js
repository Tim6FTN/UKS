import { useState } from "react";

const BranchAdd = ({ handleAdd }) => {
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen((open) => !open);
  };

  const [branch, setBranch] = useState({ name: "" });

  const handleChange = (name) => (e) => {
    setBranch({ ...branch, [name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault()
    handleAdd(branch)
    setBranch({name: ''})
    handleToggle()
  }

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
            value={branch.name}
            onChange={handleChange("name")}
            placeholder="name"
          ></input>
          <button className="btn btn-primary" type='submit'>
            Add
          </button>
        </form>
      )}
    </div>
  );
};

export default BranchAdd;
