import React, { useContext, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import UserInfo from "./pages/UserInfo";
import MealGenerator from "./pages/MealGenerator";
import GroceryGenerator from "./pages/GroceryGenerator";
import Chat from "./pages/Chat";
import Calories from "./pages/calories";
import FloatingChatIcon from "./components/common/FloatingChatIcon"; // Import the FloatingChatIcon

import { supabase } from "./supabase";
import { AuthContext } from "./context/AuthContext";

function App() {
  const { user, signIn } = useContext(AuthContext);
  const isLoggedIn = user !== null;

  useEffect(() => {
    async function getUser() {
      const { data } = await supabase.auth.getUser();
      if (data.user) {
        signIn(data.user);
      }
    }
    getUser();
  }, [signIn]);

  return (
    <>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        {isLoggedIn && (
          <Route path="" element={<Dashboard />}>
            <Route path="home" element={<Home />} />
            <Route path="userinfo" element={<UserInfo />} />
            <Route path="mealgenerator" element={<MealGenerator />} />
            <Route path="grocerygenerator" element={<GroceryGenerator />} />
            <Route path="chat" element={<Chat />} />
            <Route path="calorie" element={<Calories />} />
          </Route>
        )}
      </Routes>
      <FloatingChatIcon /> {/* Add the floating chat icon */}
    </>
  );
}

export default App;

