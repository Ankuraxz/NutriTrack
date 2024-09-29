import React, { createContext, useContext, useState } from "react";
import { supabase } from "../supabase";

const AuthContext = createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  // Add a function to set the user when they sign in

  const signIn = (userData) => {
    setUser({
      ...userData,
      email: userData.email, // Assuming your user data has an email property
    });
  };

  // Add a function to sign out
  const signOut = async () => {
    try {
      await supabase.auth.signOut(); // Sign out the user using Supabase's signOut method
      setUser(null);
    } catch (error) {
      console.error("Error signing out:", error.message);
    }
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export { AuthProvider, useAuth, AuthContext };
