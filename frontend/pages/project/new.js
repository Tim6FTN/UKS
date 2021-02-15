import { useEffect, useState } from "react"
import RepositoryService from '../../services/repositoryService'
import Navbar from "../../components/util/navbar"
import UserService from '../../services/userService'
import { useRouter } from "next/router";
import Container from '../../components/util/container'
import ProjectService from "../../services/projectService";



const NewRepository = () => {

  const emptyProject = {
    name: "",
    repositoryUrl: "",
    description: "",
    isPublic: true
  }

  const router = useRouter()
  const [project, setProject] = useState(emptyProject)


  const onSubmit = async (event) => {
    event.preventDefault()
    const response = await ProjectService.create(project)
    if (response.status === 200) router.push('/project')
  }
  return (
    <>
      <Navbar />
      <Container>
        <h1>Create a new project</h1>

        <form onSubmit={onSubmit}>
          <div className="form-group">
            <label>Project name</label>
            <input type="text" className="form-control" value={project.name} onChange={(event) => setProject({ ...project, name: event.target.value })} />
          </div>
          <div className="form-group">
            <label>Repository URL</label>
            <input type="text" className="form-control" value={project.repositoryUrl} onChange={(event) => setProject({ ...project, repositoryUrl: event.target.value })} />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea className="form-control" rows={10} value={project.description} onChange={(event) => setProject({ ...project, description: event.target.value })} ></textarea>
          </div>

          <div className="form-check">
            <input
              className="form-check-input"
              type="checkbox"
              checked={project.isPublic}
              onChange={(event) =>
                setProject({ ...project, isPublic: event.target.checked })
              }
            />
            <label className="form-check-label">Is public?</label>
          </div>
          <div className="form-group">
            <input type="submit" className="btn btn-success" value="Create project" />
          </div>
        </form>
      </Container>
    </>
  )
}

export default NewRepository