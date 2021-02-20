import { useState, createContext, useEffect } from "react";

export const UserContext = createContext(null);

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (user) localStorage.setItem("profile", JSON.stringify(user));
  }, [user]);

  useEffect(() => {
    setUser(JSON.parse(localStorage.getItem("profile")));
  }, []);

  const createUser = (newUser) => {
    setUser({ ...newUser });
    localStorage.setItem("profile", JSON.stringify({ ...newUser }));
  };

  const resetUser = () => {
    setUser(null);
    localStorage.removeItem("profile");
  };

  return (
    <UserContext.Provider value={{ user, createUser, resetUser }}>
      {children}
    </UserContext.Provider>
  );
};
