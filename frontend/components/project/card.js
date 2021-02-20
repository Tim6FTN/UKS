import { faStar, faUser } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import Link from 'next/link'


const ProjectCard = ({ project }) => {
  return (
    <>
      <div className="card bg-light mb-3">
        <div className="card-header">

          <FontAwesomeIcon icon={faUser} className="mr-2"></FontAwesomeIcon>
          {project.owner.username}</div>
        <div className="card-body">
          <h5 className="card-title"><Link href={`/project/${project.id}`}>{project.name}</Link></h5>

        </div>
        <div className="card-footer">
          <p className="card-text">
            <FontAwesomeIcon icon={faStar} className="mr-2" ></FontAwesomeIcon>
            {project.stars.length}
          </p>
        </div>
      </div>
    </>
  )
}

export default ProjectCard