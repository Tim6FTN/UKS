import { useEffect, useState } from "react"
import RepositoryService from '../../services/repositoryService'
import Navbar from "../../components/util/navbar"
import UserService from '../../services/userService'
import { useRouter } from "next/router";
import Container from '../../components/util/container'

const NewRepository = () => {
  const emptyRepository = {
    name: "",
    owner: {
      id: undefined,
      username: null
    },
    description: "",
    isPublic: true
  }

  const router = useRouter()
  const [repository, setRepository] = useState(emptyRepository)
  const [users, setUsers] = useState([])

  useEffect(async () => {
    const usersReponse = await UserService.getAll();
    setUsers(usersReponse.data)
  }, [])

  const handleSelect = (event) => {
    const selectedUser = users.find(user => user.id == event.target.value)
    setRepository({ ...repository, owner: selectedUser });
  };



  const onSubmit = async (event) => {
    event.preventDefault()
    const response = await RepositoryService.create(repository)
    if (response.status === 200) router.push('/repository')
  }
  return (
    <>
      <Navbar />
      <Container>
        <h1>Create a new repository</h1>

        <form onSubmit={onSubmit}>
          <div className="form-group">
            <select
              className="custom-select"
              onChange={handleSelect}
              value={repository.owner.id}
            >
              <option value="" defaultValue>Select user</option>
              {users.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.username}
                </option>
              ))}
            </select>
          </div>
          <div className="form-group">
            <label>Repository name</label>
            <input type="text" className="form-control" value={repository.name} onChange={(event) => setRepository({ ...repository, name: event.target.value })} />
          </div>
          <div className="form-group">
            <label>Description</label>
            <input type="text" className="form-control" value={repository.description} onChange={(event) => setRepository({ ...repository, description: event.target.value })} />
          </div>

          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              checked={repository.isPublic}
              onChange={(event) =>
                setRepository({ ...repository, isPublic: event.target.checked })
              }
            />
            <label className="form-check-label">Is public?</label>
          </div>
          <div className="form-group">
            <input type="submit" className="btn btn-success" value="Create repository" />
          </div>
        </form>
      </Container>
    </>
  )
}

export default NewRepository