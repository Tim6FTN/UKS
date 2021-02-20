import { formatDate } from "../../pages/project/[id]/task/[taskId]/index";

const History = ({ comments = [], changes = [] }) => {
  const sortFunction = (a, b) => {
    var dateA = new Date(a.timestamp).getTime();
    var dateB = new Date(b.timestamp).getTime();
    return dateA > dateB ? 1 : -1;
  };
  const items = [...comments, ...changes].sort(sortFunction);
  return (
    <div className="row mt-2 pt-2 border-top border-dark mx-1">
      <div className="col">
        {items.map((item, i) => {
          if (item.author) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2 card">
                <div className='card-body'>
                  [{formatDate(item.timestamp)}]{" "}
                  <b>{item.author.username}</b> commented: {item.text}
                </div>
              </div>
            );
          } else if (item.closing_commit) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  closed this task with commit:{" "}
                  <a href={item.closing_commit.url} target="blank">
                    {item.closing_commit.hash_id}
                  </a>
                </div>
              </div>
            );
          } else if (item.referenced_commit) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  referenced this task with commit:{" "}
                  <a href={item.referenced_commit.url} target="blank">
                    {item.referenced_commit.hash_id}
                  </a>
                </div>
              </div>
            );
          } else if (item.label) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  changed labels on this task
                </div>
              </div>
            );
          } else if (item.old_priority) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  changed prority on this task from <b>{item.old_priority}</b>{" "}
                  to <b>{item.new_priority}</b>
                </div>
              </div>
            );
          } else if (item.new_state) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  changed state for this task to <b>{item.new_state}</b>{" "}
                </div>
              </div>
            );
          } else if (item.milestone) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  assigned milestone <b>{item.milestone.title}</b> to this task
                </div>
              </div>
            );
          } else if (item.assignees && item.assignees.length > 0 && item.change_type === "Create") {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  assigned users [{item.assignees.map(ass => ass.username).join(', ')}] to this task
                </div>
              </div>
            );
          }else if (item.assignees && item.assignees.length === 0) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  removed assigned users from this task
                </div>
              </div>
            );
          }
          else if (item.new_status) {
            return (
              <div key={i} className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}] <b>{item.user.username}</b>{" "}
                  changed status of this task from <b>{item.old_status}</b> to <b>{item.new_status}</b>{" "}
                </div>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
};

export default History;
