import Navbar from '../components/util/navbar'
import Container from '../components/util/container'
import { useState } from 'react'

const Register = () => {
  const [registerInfo, setRegisterInfo] = useState({
    username: "",
    password1: "",
    password2: "",
    email: "",
    githubUsername: ""
  })

  const onChange = name => event => {
    setRegisterInfo({ ...registerInfo, [name]: event.target.value })
  }

  const handleSubmit = event => {
    event.preventDefault()

  }
  return (
    <>
      <Navbar />
      <Container>
        <form onSubmit={handleSubmit} style={{ maxWidth: 400 }} className=" mx-auto px-5 py-4">
          <h2 className="form-group text-center">REGISTER</h2>

          <div className="form-group">
            <input className="form-control" value={registerInfo.username} onChange={onChange('username')} placeholder="Username"></input>
          </div>

          <div className="form-group">
            <input className="form-control" value={registerInfo.email} onChange={onChange('email')} placeholder="Email"></input>
          </div>

          <div className="form-group">
            <input type="password" className="form-control" value={registerInfo.password1} onChange={onChange('password1')} placeholder="Password"></input>
          </div>

          <div className="form-group">
            <input type="password" className="form-control" value={registerInfo.password2} onChange={onChange('password2')} placeholder="Confirm password"></input>
          </div>

          <div className="form-group">
            <input className="form-control" value={registerInfo.githubUsername} onChange={onChange('githubUsername')} placeholder="Github username"></input>
          </div>

          <div className="form-gropup">
            <input type="submit" className="btn btn-success w-100" value="Register" />
          </div>

        </form>
      </Container>
    </>
  )
}

export default Register