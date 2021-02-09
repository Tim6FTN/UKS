import { useEffect, useState } from "react"
import UserService from "../../services/userService"
import RepositoryService from '../../services/repositoryService'
import Navbar from "../../components/util/navbar"

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

  const onSubmit = (event) => {
    event.preventDefault()
    RepositoryService.create(repository)
  }
  return (
    <>
      <Navbar />
      <h1>Create a new repository</h1>

      <form onSubmit={onSubmit}>
        <div className="form-group">
          <select
            className="form-select"
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
    </>
  )
}

export default NewRepository