import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import Invite from "../../../components/repository/invite"
import Container from "../../../components/util/container"
import Navbar from "../../../components/util/navbar"
import RepositoryService from '../../../services/repositoryService'

const Repository = () => {
  const router = useRouter()
  const emptyRepository = {
    id: null,
    name: null,
    owner: {
      id: null,
      username: null
    },
    description: null,
    stars: [],
    users: [],
    isPublic: true
  }

  const [repository, setRepository] = useState(emptyRepository)

  useEffect(async () => {
    if (router.query.id) {
      const repositoryResponse = await RepositoryService.getById(router.query.id)
      if (repositoryResponse.data) {
        setRepository(repositoryResponse.data)
      }
    }
  }, [router.query.id])

  const getProject = () => {
    console.log(repository.project)
    if (repository.project) {
      router.push(`/repository/${router.query.id}/project/${repository.project}/edit`)
    } else {
      router.push(`/repository/${router.query.id}/project/new`)
    }

  }

  return <>
    <Navbar />
    <Container>
      <h2 className="text-center">{`${repository.owner.username} / ${repository.name}`}</h2>

      <div className="row bg-light">
        <div className="col text-center">
          <button className="btn btn-secondary" > Code </button>
        </div>
        <div className="col text-center">
          <button className="btn btn-secondary" > Tasks </button>
        </div>
        <div className="col text-center">
          <button className="btn btn-secondary" onClick={getProject}> Project </button>
        </div>
        <div className="col text-center">
          <button className="btn btn-secondary" > Wiki </button>
        </div>
      </div>

      <div className="row bg-light">
        <div className="col">
          <Invite />
        </div>
      </div>
    </Container>
  </>
}

export default Repository