import { useRouter } from "next/router";
import { useContext, useState } from "react";
import Container from "../components/util/container";
import Navbar from "../components/util/navbar";
import { UserContext } from "../contexts/userContext";
import UserService from "../services/userService";

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const [errorMessage, setErrorMessage] = useState("");

  const router = useRouter();
  const { createUser } = useContext(UserContext);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      let response = await UserService.login(credentials);
      localStorage.setItem("token", response.data.token);
      response = await UserService.profile();
      createUser(response.data);
      router.push("/project");
    } catch (error) {
      setErrorMessage("Incorrect username or password");
    }
  };

  const handleChange = (name) => (event) => {
    setCredentials({ ...credentials, [name]: event.target.value });
  };

  return (
    <>      
        <form
          onSubmit={handleSubmit}
          style={{ maxWidth: 400 }}
          className=" mx-auto px-5 py-4"
        >
          <h2 className="form-group text-center">LOGIN</h2>
          <div className="mt-2">
            <input
              className="form-control"
              value={credentials.username}
              onChange={handleChange("username")}
              placeholder="Username"
            />
          </div>

          <div className="form-group mt-2">
            <input
              type="password"
              className="form-control"
              value={credentials.password}
              onChange={handleChange("password")}
              placeholder="Password"
            />
          </div>

          <div className="form-group">
            <input
              type="submit"
              className="btn btn-success w-100"
              value="Login"
            />
          </div>
          <small className="text-danger">{errorMessage}</small>
        </form>
    </>
  );
};

export default Login;
