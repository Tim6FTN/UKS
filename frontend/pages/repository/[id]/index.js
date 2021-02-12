import { faEdit, faStar } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import { useRouter } from "next/router"
import { useEffect, useState } from "react"
import ReactMarkdown from "react-markdown"
import Container from "../../../components/util/container"
import Navbar from "../../../components/util/navbar"
import RepositoryService from '../../../services/repositoryService'
import Link from 'next/link'

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
  const [starColor, setStarColor] = useState("black")
  useEffect(async () => {
    if (router.query.id) {
      const repositoryResponse = await RepositoryService.getById(router.query.id)
      if (repositoryResponse.data) {
        //Change 1 to logged user id
        if (repositoryResponse.data.stars.some(user => user.id === 1))
          setStarColor("orange")
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

  const tryDelete = () => {
    if (window.confirm("Are you sure you want to delete this repository?"))
      RepositoryService.remove(repository.id).then(response => router.push("/repository"))
  }

  const addStar = () => {
    if (starColor === "black") {
      RepositoryService.addStar(repository.id)
        .then(response => {
          setStarColor("orange");
          setRepository({ ...repository, stars: [...repository.stars, {}] })
        });
    }
  }


  return (<>
    <Navbar />
    <Container>
      <div className="d-flex justify-content-center align-items-center">
        <FontAwesomeIcon onClick={() => router.push(`/repository/${router.query.id}/edit`)} icon={faEdit} className="mr-2" style={{ cursor: "pointer" }} />
        <h3 className="text-center">{`${repository.owner.username} / ${repository.name}`}</h3>
        <FontAwesomeIcon color={starColor} onClick={addStar} icon={faStar} className="ml-2 mr-1" style={{ cursor: "pointer" }} />
        <span>
          {repository.stars.length}
        </span>
      </div>


      <div className="row bg-light">
        <div className="col text-center">
          <Link href={`/repository/${router.query.id}/code`}>
            <a className="btn btn-secondary" > Code </a>
          </Link>
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
        <div className="col text-center">
          <Link href={`/repository/${router.query.id}/invite`}>
            <a className="btn btn-secondary" > Invite users </a>
          </Link>
        </div>
        <div className="col text-center">
          <button className="btn btn-danger" onClick={tryDelete}>Delete</button>
        </div>
      </div>

      <ReactMarkdown>
        {repository.description}
      </ReactMarkdown>
    </Container>
  </>
  )
}


export default Repository