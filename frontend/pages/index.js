import { useEffect, useState } from 'react'
import ProjectCard from '../components/project/card'
import Container from '../components/util/container'
import Navbar from '../components/util/navbar'
import ProjectService from '../services/projectService'
import RepositoryService from '../services/repositoryService'


const Home = () => {
  const [searchValue, setSearchValue] = useState("")
  const [projects, setProjects] = useState([])

  useEffect(() => {
    ProjectService.getTopFive().then(response => setProjects(response.data))
  }, [])

  const repositoryCards = () =>
    projects.map(project => <ProjectCard key={project.id} project={project} />)

  const handleSubmit = (event) => {
    event.preventDefault()
    ProjectService.search(searchValue).then(response => setProjects(response.data))
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