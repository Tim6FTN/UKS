import "bootstrap/dist/css/bootstrap.min.css";
import Container from "../components/util/container";
import Navbar from "../components/util/navbar";
import { ProjectProvider } from "../contexts/projectContext";
import { UserProvider } from "../contexts/userContext";

function MyApp({ Component, pageProps }) {
  return (
    <div>
      <UserProvider>
        <ProjectProvider>
          <Navbar />
          <Container>
            <Component {...pageProps} />
          </Container>
        </ProjectProvider>
      </UserProvider>
    </div>
  );
}

export default MyApp;
