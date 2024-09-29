import { FaHeartPulse } from "react-icons/fa6";
import { FaArrowRight } from "react-icons/fa";
import { MdOutlineMoreTime } from "react-icons/md";
import Tilt from 'react-parallax-tilt'
import { useNavigate } from "react-router-dom";

const Home = () => {

  const navigate = useNavigate();

  return (
    <section className="overflow-y-auto overflow-x-hidden w-full">
    <div className="py-16">
        <div className="mx-auto px-6 max-w-6xl text-gray-500">
            <div className="relative">
                <div className="relative z-10 grid gap-3 grid-cols-6">
                  <div className='absolute bottom-20 right-32 h-[340px] w-[400px] rounded-full blur-[130px] bg-info'></div>
                  <div className='absolute top-20 left-32 h-[240px] w-[300px] rounded-full blur-[130px] bg-error'></div>
                    <Tilt tiltMaxAngleX={5} tiltMaxAngleY={5} perspective={1000} scale={1}
                     className="col-span-full lg:col-span-2 overflow-hidden flex relative p-8 rounded-xl bg-secondary bg-opacity-70">
                        <div className="size-fit m-auto relative">
                            <div className="relative h-24 w-56 flex items-center">
                                <svg className="absolute inset-0 size-full text-green-600" viewBox="0 0 254 104" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M112.891 97.7022C140.366 97.0802 171.004 94.6715 201.087 87.5116C210.43 85.2881 219.615 82.6412 228.284 78.2473C232.198 76.3179 235.905 73.9942 239.348 71.3124C241.85 69.2557 243.954 66.7571 245.555 63.9408C249.34 57.3235 248.281 50.5341 242.498 45.6109C239.033 42.7237 235.228 40.2703 231.169 38.3054C219.443 32.7209 207.141 28.4382 194.482 25.534C184.013 23.1927 173.358 21.7755 162.64 21.2989C161.376 21.3512 160.113 21.181 158.908 20.796C158.034 20.399 156.857 19.1682 156.962 18.4535C157.115 17.8927 157.381 17.3689 157.743 16.9139C158.104 16.4588 158.555 16.0821 159.067 15.8066C160.14 15.4683 161.274 15.3733 162.389 15.5286C179.805 15.3566 196.626 18.8373 212.998 24.462C220.978 27.2494 228.798 30.4747 236.423 34.1232C240.476 36.1159 244.202 38.7131 247.474 41.8258C254.342 48.2578 255.745 56.9397 251.841 65.4892C249.793 69.8582 246.736 73.6777 242.921 76.6327C236.224 82.0192 228.522 85.4602 220.502 88.2924C205.017 93.7847 188.964 96.9081 172.738 99.2109C153.442 101.949 133.993 103.478 114.506 103.79C91.1468 104.161 67.9334 102.97 45.1169 97.5831C36.0094 95.5616 27.2626 92.1655 19.1771 87.5116C13.839 84.5746 9.1557 80.5802 5.41318 75.7725C-0.54238 67.7259 -1.13794 59.1763 3.25594 50.2827C5.82447 45.3918 9.29572 41.0315 13.4863 37.4319C24.2989 27.5721 37.0438 20.9681 50.5431 15.7272C68.1451 8.8849 86.4883 5.1395 105.175 2.83669C129.045 0.0992292 153.151 0.134761 177.013 2.94256C197.672 5.23215 218.04 9.01724 237.588 16.3889C240.089 17.3418 242.498 18.5197 244.933 19.6446C246.627 20.4387 247.725 21.6695 246.997 23.615C246.455 25.1105 244.814 25.5605 242.63 24.5811C230.322 18.9961 217.233 16.1904 204.117 13.4376C188.761 10.3438 173.2 8.36665 157.558 7.52174C129.914 5.70776 102.154 8.06792 75.2124 14.5228C60.6177 17.8788 46.5758 23.2977 33.5102 30.6161C26.6595 34.3329 20.4123 39.0673 14.9818 44.658C12.9433 46.8071 11.1336 49.1622 9.58207 51.6855C4.87056 59.5336 5.61172 67.2494 11.9246 73.7608C15.2064 77.0494 18.8775 79.925 22.8564 82.3236C31.6176 87.7101 41.3848 90.5291 51.3902 92.5804C70.6068 96.5773 90.0219 97.7419 112.891 97.7022Z" fill="currentColor"></path>
                                </svg>
                                <span className="w-fit block mx-auto text-5xl font-semibold text-transparent bg-clip-text bg-gradient-to-br from-blue-400 to-pink-400">100%</span>
                            </div>
                            <h2 className="mt-6 text-center font-bold text-base-content text-4xl">Customizable</h2>
                            <h2 className="text-center font-bold text-base-content text-4xl">Meal Plans</h2>
                        </div>
                    </Tilt>
                    <Tilt tiltMaxAngleX={5} tiltMaxAngleY={5} perspective={1000} scale={1}
                     className="col-span-full sm:col-span-3 lg:col-span-2 overflow-hidden relative p-8 rounded-xl bg-secondary bg-opacity-70">
                        <div>
                            <div className="relative aspect-square rounded-full size-32 flex items-center justify-center border mx-auto dark:bg-white/5 dark:border-white/10 before:absolute before:-inset-2 before:border dark:before:border-white/5 dark:before:bg-white/5 before:rounded-full">
                              <FaHeartPulse className="text-8xl text-red-600 mt-2 ml-1"/>
                            </div>
                            <div className="mt-6 text-center relative z-10 space-y-2">
                                <h2 className="text-3xl font-medium text-base-content">Invest In Your Health</h2>
                                <p className="text-base-content">Our customizable meal plans and grocery lists make it easy for you to stick to a deliciously healthy life even during the busiest of weeks.</p>
                            </div>
                        </div>
                    </Tilt>
                    <Tilt tiltMaxAngleX={5} tiltMaxAngleY={5} perspective={1000} scale={1}
                     className="col-span-full sm:col-span-3 lg:col-span-2 overflow-hidden relative p-8 rounded-xl bg-secondary bg-opacity-70">
                        <div>
                            <div className="pt-0 lg:px-6">
                            <svg className="w-full" viewBox="0 0 386 123" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <rect width="386" height="123" rx="10"></rect>
                                    <path fillRule="evenodd" clipRule="evenodd" d="M3 123C3 123 14.3298 94.153 35.1282 88.0957C55.9266 82.0384 65.9333 80.5508 65.9333 80.5508C65.9333 80.5508 80.699 80.5508 92.1777 80.5508C103.656 80.5508 100.887 63.5348 109.06 63.5348C117.233 63.5348 117.217 91.9728 124.78 91.9728C132.343 91.9728 142.264 78.03 153.831 80.5508C165.398 83.0716 186.825 91.9728 193.761 91.9728C200.697 91.9728 206.296 63.5348 214.07 63.5348C221.844 63.5348 238.653 93.7771 244.234 91.9728C249.814 90.1684 258.8 60 266.19 60C272.075 60 284.1 88.057 286.678 88.0957C294.762 88.2171 300.192 72.9284 305.423 72.9284C312.323 72.9284 323.377 65.2437 335.553 63.5348C347.729 61.8259 348.218 82.07 363.639 80.5508C367.875 80.1335 372.949 82.2017 376.437 87.1008C379.446 91.3274 381.054 97.4325 382.521 104.647C383.479 109.364 382.521 123 382.521 123" fill="url(#paint0_linear_0_106)"></path>
                                    <path className="text-green-500" d="M3 121.077C3 121.077 15.3041 93.6691 36.0195 87.756C56.7349 81.8429 66.6632 80.9723 66.6632 80.9723C66.6632 80.9723 80.0327 80.9723 91.4656 80.9723C102.898 80.9723 100.415 64.2824 108.556 64.2824C116.696 64.2824 117.693 92.1332 125.226 92.1332C132.759 92.1332 142.07 78.5115 153.591 80.9723C165.113 83.433 186.092 92.1332 193 92.1332C199.908 92.1332 205.274 64.2824 213.017 64.2824C220.76 64.2824 237.832 93.8946 243.39 92.1332C248.948 90.3718 257.923 60.5 265.284 60.5C271.145 60.5 283.204 87.7182 285.772 87.756C293.823 87.8746 299.2 73.0802 304.411 73.0802C311.283 73.0802 321.425 65.9506 333.552 64.2824C345.68 62.6141 346.91 82.4553 362.27 80.9723C377.629 79.4892 383 106.605 383 106.605" stroke="currentColor" strokeWidth="3"></path>
                                    <defs>
                                        <linearGradient id="paint0_linear_0_106" x1="3" y1="60" x2="3" y2="123" gradientUnits="userSpaceOnUse">
                                            <stop className="text-green-600/30" stopColor="currentColor"></stop>
                                            <stop className="text-white dark:text-transparent" offset="1" stopColor="currentColor" stopOpacity="0.103775"></stop>
                                        </linearGradient>
                                        <clipPath id="clip0_0_106">
                                            <rect width="358" height="30" fill="white" transform="translate(14 14)"></rect>
                                        </clipPath>
                                    </defs>
                                </svg>
                            </div>
                            <div className="mt-6 text-center relative z-10 space-y-6">
                                <h2 className="text-3xl font-medium text-base-content">Maintain Healthy Weight</h2>
                                <p className="text-base-content">It’s time to put away the calculator. Whether you want to maintain or even lose weight, NutriTrack is the only weight management meal planner.</p>
                            </div>
                        </div>
                    </Tilt>
                    <Tilt tiltMaxAngleX={5} tiltMaxAngleY={5} perspective={1000} scale={1} 
                    className="col-span-full lg:col-span-3 overflow-hidden relative p-8 rounded-xl bg-secondary bg-opacity-70">
                        <div className="flex flex-wrap justify-center items-center gap-6">
                            <div className="flex flex-col justify-between relative z-10 space-y-12 lg:space-y-6">
                                <div className="space-y-2">
                                    <h2 className="text-3xl font-medium text-center text-base-content">Take Back Your Time</h2>
                                    <p className="text-base-content max-w-64 text-center">Skip the cookbook and Pinterest hunt. With NutriTrack, you can transform your daily meals with quick, exciting, and nutritious dishes in just 20 minutes or less.</p>
                                </div>
                            </div>
                            <div className="relative aspect-square rounded-full size-32 flex items-center justify-center border mx-auto dark:bg-white/5 dark:border-white/10 before:absolute before:-inset-2 before:border dark:before:border-white/5 dark:before:bg-white/5 before:rounded-full">
                              <MdOutlineMoreTime className="text-8xl text-blue-500 ml-2 mb-1"/>
                            </div>
                        </div>
                    </Tilt>
                    <Tilt tiltMaxAngleX={5} tiltMaxAngleY={5} perspective={1000} scale={1}
                     className="col-span-full lg:col-span-3 overflow-hidden relative p-8 rounded-xl bg-secondary bg-opacity-70 text-base-content flex items-center justify-center gap-10">
                        <div className="text-4xl sm:text-5xl md:text-7xl font-bold">Get<br/>Started</div>
                        <FaArrowRight className="text-9xl animate-pulse"/>
                        <div className="absolute inset-0 cursor-pointer" onClick={()=>{navigate("/userinfo")}}></div>
                    </Tilt>
                </div>
            </div>
        </div>
    </div>
</section>
  );
};

export default Home;
