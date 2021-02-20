import { formatDate } from "../../pages/project/[id]/task/[taskId]/index";

const History = ({ comments = [], changes = [] }) => {
  const items = [...comments, ...changes];
  return (
    <div className="row mt-2 pt-2 border-top border-dark ml-auto">
      <div className="col">
        {items.map((item) => {
          if (item.author) {
            return (
              <div className="mx-1 my-3 p-1 border-dark border p-2">
                <div className="border-bottom">
                  [{formatDate(item.timestamp)}] <b>{item.author.username}</b>{" "}
                  commented:
                </div>
                <div>{item.text}</div>
              </div>
            );
          }
        })}
      </div>
    </div>
  );
};

export default History;
