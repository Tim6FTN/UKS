import { useEffect, useState } from "react"
import RepositoryService from '../../services/repositoryService'
import Link from 'next/link'
import Navbar from "../../components/util/navbar"


const Repositories = () => {

  const [repositories, setRepositories] = useState([])

  useEffect(() => {
    RepositoryService.getAll().then(response => setRepositories(response.data))
  }, [])

  const links = () => repositories.map(repository => <Link key={repository.id} href={`/repository/${repository.id}`}>{repository.name}</Link>)
  return <>
    <Navbar />
    <h1>REPOSITORIES</h1>

    {links()}
  </>
}

export default Repositories