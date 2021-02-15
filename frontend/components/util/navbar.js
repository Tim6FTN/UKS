import Link from 'next/link'
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
const Navbar = () => {

  const router = useRouter()
  const [tokenExsists, setTokenExists] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('token')
    setTokenExists(Boolean(token))
  }, [])

  const logout = event => {
    event.preventDefault()
    localStorage.removeItem('token')
    setTokenExists(false)
  }

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarNav">
          <Link href="/">
            <a className="navbar-brand">Home</a>

          </Link>
          <ul className="navbar-nav">
            <li className={`nav-item ${router.pathname == '/project' ? "active" : ""}`}>
              <Link href="/project">
                <a className="nav-link">Projects</a>
              </Link>
            </li>
          </ul>
          <ul className="navbar-nav ml-auto">
            {!tokenExsists &&
              <li className={`nav-item ${router.pathname == '/login' ? "active" : ""}`}>
                <Link href="/login">
                  <a className="nav-link">Login</a>
                </Link>
              </li>
            }
            {!tokenExsists &&
              <li className={`nav-item ${router.pathname == '/register' ? "active" : ""}`}>
                <Link href="/register">
                  <a className="nav-link" >Register</a>
                </Link>
              </li>
            }

            {tokenExsists &&
              <li className={`nav-item ${router.pathname === 'profile' ? 'active' : ''}`}>
                <Link href="/profile">
                  <a className="nav-link">Profile</a>
                </Link>
              </li>
            }
            {tokenExsists &&
              <li className="nav-item">
                <a className="nav-link" href="#" onClick={logout}>Logout</a>
              </li>
            }


          </ul>
        </div>
      </div>
    </nav>
  )
}

export default Navbar;