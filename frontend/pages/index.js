import { useEffect, useState } from 'react'
import RepositoryCard from '../components/repository/card'
import Container from '../components/util/container'
import Navbar from '../components/util/navbar'
import RepositoryService from '../services/repositoryService'


const Home = () => {
  const [searchValue, setSearchValue] = useState("")
  const [repositories, setRepositories] = useState([])

  useEffect(() => {
    RepositoryService.getTopFive().then(response => setRepositories(response.data))
  }, [])

  const repositoryCards = () =>
    repositories.map(repository => <RepositoryCard key={repository.id} repository={repository} />)

  const handleSubmit = (event) => {
    event.preventDefault()
    RepositoryService.search(searchValue).then(response => setRepositories(response.data))
  }
  return (
    <div>
      <Navbar />

      <Container>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input type="search" className="form-control" value={searchValue} onChange={(event) => setSearchValue(event.target.value)} placeholder="Search..." />
          </div>
        </form>
        <div className="card-deck">
          {repositoryCards()}
        </div>
      </Container>
    </div>
  )
}

export default Home