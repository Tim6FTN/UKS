import Link from 'next/link'

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link href="/project">
                <a className="nav-link">Project</a>
              </Link>
            </li>

            <li className="nav-item">
              <Link href="/repository">
                <a className="nav-link">Repository</a>
              </Link>
            </li>
            <li className="nav-item">
              <Link href="/label">
                <a className="nav-link">Label</a>
              </Link>
            </li>

          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar;