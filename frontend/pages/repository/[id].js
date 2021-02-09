import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import Navbar from "../../components/util/navbar"
import RepositoryService from '../../services/repositoryService'

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

  return <>
    <Navbar />
    <h2>{`${repository.owner.username} / ${repository.name}`}</h2>

    <div className="row bg-light">
      <div className="col text-center">
        Code
      </div>
      <div className="col text-center">
        Tasks
      </div>
      <div className="col text-center">
        Project
      </div>
      <div className="col text-center">
        Wiki
      </div>
    </div>
  </>
}

export default Repository