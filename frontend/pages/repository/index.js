import { useEffect, useState } from "react"
import RepositoryService from '../../services/repositoryService'
import Link from 'next/link'
import Navbar from "../../components/util/navbar"
import Container from "../../components/util/container"
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'

import { faBook, faLock } from '@fortawesome/free-solid-svg-icons'



const Repositories = () => {

  const [repositories, setRepositories] = useState([])

  useEffect(() => {
    RepositoryService.getAll().then(response => setRepositories(response.data))
  }, [])

  const links = () => repositories.map(repository =>
    <tr key={repository.id}>
      <td>{repository.isPublic ? <FontAwesomeIcon className="m-2" icon={faBook} size="2x" /> : <FontAwesomeIcon className="m-2" icon={faLock} size="2x" />}</td>
      <td><span className="h5"><Link key={repository.id} href={`/repository/${repository.id}`}>{repository.name}</Link></span></td>
    </tr>)
  return <>
    <Navbar />
    <Container>
      <div className="row">
        <div className="col text-center">
          <h1>REPOSITORIES</h1>
        </div>
        <div className="col text-center">
          <Link href="/repository/new">
            <button className="btn btn-success">
              New repository
        </button>
          </Link>
        </div>
      </div>

      <table>
        <tbody>
          {links()}
        </tbody>
      </table>


    </Container>
  </>
}

export default Repositories