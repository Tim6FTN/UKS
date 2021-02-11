import Link from 'next/link'
import { useRouter } from 'next/router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
const Navbar = () => {

  const router = useRouter()

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarNav">
          <Link href="/">
            <a className="navbar-brand">Home</a>

          </Link>
          <ul className="navbar-nav">
            <li className={`nav-item ${router.pathname == '/repository' ? "active" : ""}`}>
              <Link href="/repository">
                <a className="nav-link">Repositories</a>
              </Link>
            </li>
            <li className={`nav-item ${router.pathname == '/label' ? "active" : ""}`}>
              <Link href="/label">
                <a className="nav-link">Labels</a>
              </Link>
            </li>

          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar;