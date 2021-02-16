import { useRouter } from "next/router";
import { useEffect, useState } from "react";

export default function withAuth(Component) {
  const withAuth = (props) => {
    const router = useRouter()
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    useEffect(() => {
      const token = localStorage.getItem("token");
      setIsLoggedIn(token);
      if(!token) {
        router.push('/login')
      }
    }, []);

    if (isLoggedIn) {
      return <Component {...props} />;
    } else {
      return null;
    }
  };

  return withAuth;
}
