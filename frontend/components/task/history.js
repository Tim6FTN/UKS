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
        {items.map((item) => {
          if (item.author) {
            return (
              <div className="mx-1 my-3 p-1 p-2">
                <div>
                  --- [{formatDate(item.timestamp)}]{" "}
                  <b>{item.author.username}</b> commented: {item.text}
                </div>
              </div>
            );
          } else if (item) {
          }
        })}
      </div>
    </div>
  );
};

export default History;
