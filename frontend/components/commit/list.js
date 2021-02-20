import { faFolderMinus, faFolderPlus, faMinusSquare, faPlusSquare } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const CommitList = ({ commits, handleAdd }) => {
  return (
    <>
      <h1>Commits</h1>
      <ul className="list-group">
        {commits.map((commit) => (
          <li className="list-group-item" key={commit.id}>
            <a href={commit.url}>{commit.hash_id}</a>
            <div>
              <b>{commit.author_username}</b>{" "}
              {new Date(commit.timestamp).toString().split(" (")[0]}
            </div>
            <div className="mt-2">{commit.message}</div>
            <div className="mt-2 pt-2 border-top border-dark row">
              <div className="col-2">
                <FontAwesomeIcon icon={faPlusSquare} className="mr-2" />
                {commit.commit_meta_data.line_additions_count}
                <FontAwesomeIcon icon={faMinusSquare} className="mx-2" />
                {commit.commit_meta_data.line_deletions_count}
              </div>
              <div className="col-10 text-left">
                <FontAwesomeIcon icon={faFolderPlus} className="mr-2" />
                {commit.commit_meta_data.file_additions_count}
                <FontAwesomeIcon icon={faFolderMinus} className="mx-2" />
                {commit.commit_meta_data.file_deletions_count}
              </div>
            </div>
          </li>
        ))}
      </ul>
    </>
  );
};

export default CommitList;
