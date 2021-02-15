import Container from "../components/util/container";
import Navbar from "../components/util/navbar";
import withAuth from "../components/util/withAuth";

const Profile = () => {
  return (
    <>
      <Navbar />
      <Container>Profile</Container>
    </>
  );
};

export default withAuth(Profile);
