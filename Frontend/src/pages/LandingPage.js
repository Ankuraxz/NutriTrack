import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { supabase } from "../supabase";
import berry from '../assets/images/berry.png'
import spinach from '../assets/images/spinach.png'

export default function Landing() {

  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSignIn = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${process.env.REACT_APP_BASE_URL}/home`,
        // skipBrowserRedirect: false,
      },
    });
  };

  const [offsetX, setOffsetX] = useState(0);
  const [offsetY, setOffsetY] = useState(0);

  useEffect(() => {
    const handleMouseMove = (e) => {
      const { clientX, clientY } = e;
      const { left, top, width, height } = e.target.getBoundingClientRect();
      const centerX = left + width / 2;
      const centerY = top + height / 2;
      const offsetY = (clientY - centerY) / 30;
      const offsetX = (clientX - centerX) / 30;
      setOffsetX(offsetX);
      setOffsetY(offsetY);
    };

    document?.addEventListener('mousemove', handleMouseMove);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="relative bg-[url('assets/bg.svg')] bg-cover">
        <div className="absolute top-3 sm:top-0 right-3 sm:right-0 blur-sm max-sm:w-[150px]" style={{ transform: `translate(${offsetX}px, ${offsetY}px)` }}>
          <img src={berry} alt="berry" width={180} className="object-cover"/>
        </div>
        <div className="absolute -left-32 sm:-left-20 -bottom-40 sm:-bottom-32 blur-sm max-sm:w-[350px]" style={{ transform: `translate(${offsetX}px, ${offsetY}px)` }}>
          <img src={spinach} alt="spinach" className="object-cover"/>
        </div>

        <div className="w-full h-screen flex flex-col justify-center items-center relative z-10">
          <h1 className="font-bold text-stone-900 text-6xl sm:text-7xl lg:text-9xl -mt-20 bg-gradient-to-r from-green-400 via-green-600 to-green-400 bg-clip-text text-transparent">
            NutriTrack
          </h1>
          <p className="text-2xl text-stone-900 sm:text-3xl font-semibold text-center mt-4 px-4">
            Unlock the Secrets to Balanced Meals and Effortless Planning
          </p>
          <button
            className="mt-8 px-6 py-4 text-xl font-medium text-white bg-black rounded-lg border-none hover:scale-105 transition-all duration-200"
            onClick={user ? () => navigate("/home") : handleSignIn}
          >
            {user ? `Welcome, ${user.email}` : "Get started"}
          </button>
        </div>
    </div>
  );
}
