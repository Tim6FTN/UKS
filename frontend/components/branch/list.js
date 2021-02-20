import BranchAdd from "./add";

const BranchList = ({ branches, active, handleChange, handleAdd }) => {
  return (
    <>
      <h1>Branches</h1>
      <div className="form-group">
        <select
          className="custom-select"
          onChange={handleChange}
          value={active}
        >
          <option key='' value=''></option>
          {branches.map((branch) => (
            <option key={branch.id} value={branch.id}>
              {branch.name}
            </option>
          ))}
        </select>
      </div>
    </>
  );
};

export default BranchList;
