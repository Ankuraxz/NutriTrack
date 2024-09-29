import { useRef, useState } from "react";
import { Link } from "react-router-dom";
import logo from "../../assets/logo_icon.png"

const Navbar = () => {

  const [toggle, setToggle] = useState(false)
  const navMenu = useRef(null)

  const closeOpenMenus = (e)=>{
    if(navMenu.current && toggle && !navMenu.current.contains(e.target)){
      setToggle(false)
    }
  }
  document.addEventListener('mousedown',closeOpenMenus)

  return (
    <div className="navbar bg-base-300">
      <div className="navbar-start z-20">
        <Link to="/home" className="hidden sm:block"><img src={logo} alt="logo" className="w-16 ml-16 h-16"/></Link>

        {/* MOBILE NAVBAR */}
        <div ref={navMenu} className='sm:hidden flex flex-1 justify-end items-center relative'>

          {/*Hamburger icon*/}
          <div id="menu-icon" className={`${toggle ? 'close' : ''} cursor-pointer z-20 absolute left-0`} 
            onClick={()=>setToggle(!toggle)}>
            <div className="bar bg-info"></div>
            <div className="bar bg-info"></div>
            <div className="bar bg-info"></div>
          </div>

          <div className={`${!toggle ? 'hidden' : 'block'} absolute -top-5 left-2 backdrop-blur-lg rounded-md min-w-[210px] bg-base-200`}>

            <ul className='flex flex-col gap-3 pt-6 pb-3 pl-10'>
              <li className="hover:text-gray-500 text-[18px] font-medium cursor-pointer">
                <Link to="/home" onClick={()=>setToggle(false)}>Home</Link>
              </li>
              <li className="hover:text-gray-500 text-[18px] font-medium cursor-pointer">
                <Link to="/userinfo" onClick={()=>setToggle(false)}>User Information</Link>
              </li>
              <li className="hover:text-gray-500 text-[18px] font-medium cursor-pointer">
                <Link to="/mealgenerator" onClick={()=>setToggle(false)}>Meal Generator</Link>
              </li>
              <li className="hover:text-gray-500 text-[18px] font-medium cursor-pointer">
                <Link to="/grocerygenerator" onClick={()=>setToggle(false)}>Grocery Generator</Link>
              </li>
              <li className="hover:text-gray-500 text-[18px] font-medium cursor-pointer">
                <Link to="/chat" onClick={()=>setToggle(false)}>calorie counter</Link>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div className="navbar-center sm:pl-[13rem]">
        <Link to="/home" className="text-3xl font-bold tracking-wide relative inline cursor-pointer before:bg-blue-500 before:absolute before:-bottom-1 before:block before:h-[2px] before:w-full before:origin-bottom-right before:scale-x-0 before:transition before:duration-300 before:ease-in-out hover:before:origin-bottom-left hover:before:scale-x-100">
          NutriTrack
        </Link>
      </div>
      <div className="navbar-end"></div>
    </div>
  );
};

export default Navbar;