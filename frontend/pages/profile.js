import { useEffect, useState } from "react";
import InviteCard from "../components/invite/card";
import Container from "../components/util/container";
import Navbar from "../components/util/navbar";
import withAuth from "../components/util/withAuth";
import InviteService from "../services/inviteService";

const Profile = () => {
  const [invites, setInvites] = useState([]);

  useEffect(() => {
    InviteService.getAll().then((response) => setInvites(response.data));
  }, []);

  const accept = (inviteId) => {
    if (window.confirm("Are you sure you want to accept this invite?"))
      InviteService.accept(inviteId).then((response) =>
        setInvites(invites.filter((invite) => invite.id !== inviteId))
      );
  };

  const decline = (inviteId) => {
    if (window.confirm("Are you sure you want to decline this invite?"))
      InviteService.decline(inviteId).then((response) =>
        setInvites(invites.filter((invite) => invite.id !== inviteId))
      );
  };

  return (
    <>
      <h2 className="text-center">My profile</h2>
      <h2 className="text-center">
        {invites.length ? "Pending invites:" : "No pending invites"}
      </h2>

      {invites.map((invite) => (
        <InviteCard
          key={invite.id}
          invite={invite}
          accept={accept}
          decline={decline}
        />
      ))}
    </>
  );
};

export default withAuth(Profile);
