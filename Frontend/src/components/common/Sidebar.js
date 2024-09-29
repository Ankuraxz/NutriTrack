import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { supabase } from "../../supabase";
import { AiFillHome } from "react-icons/ai";
import { FaUserEdit, FaUser } from "react-icons/fa";
import { GiBowlOfRice } from "react-icons/gi";
import { MdLocalGroceryStore } from "react-icons/md";
import { IoChatbubbles } from "react-icons/io5";
import { MdFastfood } from "react-icons/md";

const Sidebar = () => {
  const navigate = useNavigate();
  const { signOut } = useAuth();

  return (
    <div className="min-w-[13rem] pt-2 h-[100%] flex flex-col gap-1 border-r border-base-300">
      <Link
        to="/home"
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>Home</div>
        <div>
          <AiFillHome className="text-2xl" />
        </div>
      </Link>
      <Link
        to="/userinfo"
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>User Information</div>
        <div>
          <FaUserEdit className="text-2xl" />
        </div>
      </Link>
      <Link
        to="/mealgenerator"
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>Meal Plan</div>
        <div>
          <GiBowlOfRice className="text-2xl" />
        </div>
      </Link>
      <Link
        to="/grocerygenerator"
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>Grocery List</div>
        <div>
          <MdLocalGroceryStore className="text-2xl" />
        </div>
      </Link>
      <Link
        to="/calorie"
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>Calorie Counter</div>
        <div>
          <MdFastfood className="text-2xl" />
        </div>
      </Link>
      <div
        onClick={async () => {
          await supabase.auth.signOut();
          signOut();
          navigate("/");
        }}
        className="flex items-center justify-between text-lg py-[0.5rem] px-[0.7rem] hover:bg-base-200 transition-all duration-100 cursor-pointer"
      >
        <div>Logout</div>
        <div>
          <FaUser className="text-2xl" />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
