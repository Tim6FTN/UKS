import Navbar from "../components/util/navbar";
import Container from "../components/util/container";
import { useEffect, useState } from "react";
import UserService from "../services/userService";
import { useRouter } from "next/router";

const Register = () => {
  const [registerInfo, setRegisterInfo] = useState({
    username: "",
    password1: "",
    password2: "",
    email: "",
    github_username: "",
  });

  const [error, setError] = useState(null)

  const router = useRouter();

  const onChange = (name) => (event) => {
    setRegisterInfo({ ...registerInfo, [name]: event.target.value });
  };

  useEffect(() => {
    if(registerInfo.password1 !== registerInfo.password2){
      setError('Passwords must match')
    }else {
      setError(null)
    }
  }, [registerInfo])

  const handleSubmit = async (event) => {
    event.preventDefault();
    await UserService.register({
      ...registerInfo,
      password: registerInfo.password1,
    });
    router.push("/login");
  };
  return (
    <>
      <Navbar />
      <Container>
        <form
          onSubmit={handleSubmit}
          style={{ maxWidth: 400 }}
          className=" mx-auto px-5 py-4"
        >
          <h2 className="form-group text-center">REGISTER</h2>

          <div className="form-group">
            <input
              className="form-control"
              value={registerInfo.username}
              onChange={onChange("username")}
              placeholder="Username"
            ></input>
          </div>

          <div className="form-group">
            <input
              className="form-control"
              value={registerInfo.email}
              onChange={onChange("email")}
              placeholder="Email"
            ></input>
          </div>

          <div className="form-group">
            <input
              type="password"
              className="form-control"
              value={registerInfo.password1}
              onChange={onChange("password1")}
              placeholder="Password"
            ></input>
            {error && <small className='text-danger'>{error}</small>}
          </div>

          <div className="form-group">
            <input
              type="password"
              className="form-control"
              value={registerInfo.password2}
              onChange={onChange("password2")}
              placeholder="Confirm password"
            ></input>
            {error && <small className='text-danger'>{error}</small>}
          </div>

          <div className="form-group">
            <input
              className="form-control"
              value={registerInfo.github_username}
              onChange={onChange("github_username")}
              placeholder="Github username"
            ></input>
          </div>

          <div className="form-gropup">
            <input
              disabled={error}
              type="submit"
              className="btn btn-success w-100"
              value="Register"
            />
          </div>
        </form>
      </Container>
    </>
  );
};

export default Register;
