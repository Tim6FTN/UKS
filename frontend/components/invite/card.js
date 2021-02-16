const InviteCard = ({ invite, accept, decline }) => {
  return (
    <div className="card mx-auto" style={{ maxWidth: 700 }}>
      <div className="card-body d-flex align-items-center">
        <h3>{invite.project.name}</h3>
        <button
          className="btn btn-success ml-auto"
          onClick={() => accept(invite.id)}
        >
          Accept
        </button>
        <button
          className="btn btn-danger ml-3"
          onClick={() => decline(invite.id)}
        >
          Decline
        </button>
      </div>
    </div>
  );
};

export default InviteCard;
