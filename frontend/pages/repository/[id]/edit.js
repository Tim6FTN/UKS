import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import Container from "../../../components/util/container"
import Navbar from "../../../components/util/navbar"
import RepositoryService from "../../../services/repositoryService"

const EditRepository = () => {

  const [repository, setRepository] = useState({ name: "", description: "" })
  const router = useRouter()

  useEffect(() => {
    if (router.query.id)
      RepositoryService.getById(router.query.id).then(response => setRepository(response.data))
  }, [router.query.id])

  const handleSubmit = (event) => {
    event.preventDefault()
    RepositoryService.update(router.query.id, repository)
  }
  return (
    <div>
      <Navbar />
      <Container>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <span>Repository name</span>
            <input className="form-control" value={repository.name} onChange={event => setRepository({ ...repository, name: event.target.value })} />
          </div>

          <div className="form-group">
            <span>Description</span>
            <textarea className="form-control" rows={10} value={repository.description} onChange={event => setRepository({ ...repository, description: event.target.value })} />
          </div>

          <input type="submit" className="btn btn-success" value="Submit" />
        </form>
      </Container>
    </div>
  )
}

export default EditRepository