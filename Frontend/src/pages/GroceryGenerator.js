import React, { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const GroceryGenerator = () => {
    const { user } = useAuth();
    const [groceryList, setGroceryList] = useState([]);
    const [loading, setLoading] = useState(false);

    // Load stored grocery list on component mount
    useEffect(() => {
        const storedGroceryList = localStorage.getItem("groceryList");
        if (storedGroceryList) {
            setGroceryList(JSON.parse(storedGroceryList));
        }
    }, []);

    const generateGroceryList = async () => {
        const email = user.email;
        setLoading(true);

        // Clear previously stored grocery list
        localStorage.removeItem("groceryList");

        try {
            // First API call to generate grocery
            await axios.get(
                `https://nutrition-ai-backend.onrender.com/grocery/generate_grocery_list/${email}`,
                {
                    headers: {
                        Accept: "application/json",
                    },
                    params: {
                        email_id: email,
                    },
                }
            );

            // Second API call to show grocery list
            const showResponse = await axios.get(
                `https://nutrition-ai-backend.onrender.com/grocery/show_grocery_list/${email}`,
                {
                    headers: {
                        Accept: "application/json",
                    },
                    params: {
                        email_id: email,
                    },
                }
            );

            // Assuming the response contains the displayed grocery list as a string
            const showData = showResponse.data;

            // Split the string into an array using commas as the delimiter
            const parsedGroceryList = showData.grocery_list
                .split(",")
                .map((item) => item.trim())
                .filter((item) => item.length > 0); // Filter out any empty strings

            // Check if parsedGroceryList is iterable (an array)
            if (Array.isArray(parsedGroceryList)) {
                // Update the state with the parsed grocery list
                setGroceryList(parsedGroceryList);
                // Store the grocery list in localStorage
                localStorage.setItem("groceryList", JSON.stringify(parsedGroceryList));
            } else {
                console.error(
                    "Invalid data format for parsedGroceryList:",
                    parsedGroceryList
                );
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false);
        }
    };

    if (loading)
        return (
            <div className="w-full flex justify-center">
                <div className="loading loading-dots loading-lg bg-[#41b2de]"></div>
            </div>
        );

    return (
        <div className="w-full flex flex-col items-center p-5 overflow-auto">
            <button
                className="btn btn-info text-lg font-semibold text-white mb-10 w-fit"
                onClick={generateGroceryList}
            >
                Generate Grocery
            </button>

            {/* Display the generated grocery list in multiple columns */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
                {groceryList.map((item, index) => (
                    <div key={index} className="flex items-center gap-2">
                        <input
                            type="checkbox"
                            id={`item-${index}`}
                            className="checkbox checkbox-info"
                        />
                        <label htmlFor={`item-${index}`} className="ml-2 capitalize">
                            {item}
                        </label>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default GroceryGenerator;
