import CommitAdd from "./add";

const CommitList = ({ commits, handleAdd }) => {
  return (
    <>
      <h1>Commits</h1>
      <ul className="list-group">
        {commits.map((commit) => (
          <li className="list-group-item" key={commit.id}>
            <div className='font-weight-bold'>{commit.hash}</div>
            <div>{new Date(commit.timestamp).toString().split(" (")[0]}</div>
            <div className="mt-2">{commit.message}</div>
          </li>
        ))}
      </ul>
      <CommitAdd handleAdd={handleAdd} />
    </>
  );
};

export default CommitList;
