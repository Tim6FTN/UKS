import Link from "next/link";
import { useRouter } from "next/router";
import { useContext, useEffect, useState } from "react";
import { UserContext } from "../../contexts/userContext";
const Navbar = () => {
  const router = useRouter();
  const { user, resetUser } = useContext(UserContext);

  const logout = (event) => {
    event.preventDefault();
    localStorage.removeItem("token");
    resetUser();
    setTokenExists(false);
    router.push("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <div className="collapse navbar-collapse" id="navbarNav">
          <Link href="/">
            <a className="navbar-brand">Home</a>
          </Link>
          {user && (
            <ul className="navbar-nav">
              <li
                className={`nav-item ${
                  router.pathname == "/project" ? "active" : ""
                }`}
              >
                <Link href="/project">
                  <a className="nav-link">Projects</a>
                </Link>
              </li>
            </ul>
          )}

          <ul className="navbar-nav ml-auto">
            {!user && (
              <li
                className={`nav-item ${
                  router.pathname == "/login" ? "active" : ""
                }`}
              >
                <Link href="/login">
                  <a className="nav-link">Login</a>
                </Link>
              </li>
            )}
            {!user && (
              <li
                className={`nav-item ${
                  router.pathname == "/register" ? "active" : ""
                }`}
              >
                <Link href="/register">
                  <a className="nav-link">Register</a>
                </Link>
              </li>
            )}

            {user && (
              <li
                className={`nav-item ${
                  router.pathname === "profile" ? "active" : ""
                }`}
              >
                <Link href="/profile">
                  <a className="nav-link">{user?.username}</a>
                </Link>
              </li>
            )}
            {user && (
              <li className="nav-item">
                <a className="nav-link" href="#" onClick={logout}>
                  Logout
                </a>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
