import { useRouter } from "next/router"
import { useState } from "react"
import Container from "../components/util/container"
import Navbar from "../components/util/navbar"
import UserService from "../services/userService"

const Login = () => {

  const [credentials, setCredentials] = useState({ username: "", password: "" })
  const router = useRouter()

  const handleSubmit = event => {
    event.preventDefault()
    UserService.login(credentials).then(response => {
      localStorage.setItem('token', response.data.token)
      router.push('/project')
    })
  }

  return (
    <>
      <Navbar />
      <Container>
        <form onSubmit={handleSubmit} style={{ maxWidth: 400 }} className=" mx-auto px-5 py-4">
          <h2 className="form-group text-center">LOGIN</h2>
          <div className="mt-2">
            <input className="form-control" value={credentials.username} onChange={event => setCredentials({ ...credentials, username: event.target.value })} placeholder="Username" />
          </div>

          <div className="form-group mt-2">
            <input type="password" className="form-control" value={credentials.password} onChange={event => setCredentials({ ...credentials, password: event.target.value })} placeholder="Password" />
          </div>

          <div className="form-group">
            <input type="submit" className="btn btn-success w-100" value="Login" />
          </div>
        </form>
      </Container>
    </>
  )
}

export default Login