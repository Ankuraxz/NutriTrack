import React, { useState, useEffect } from "react";
import axios from "axios";
import MealPlan from "../components/core/MealPlan";
import { useAuth } from "../context/AuthContext";

const MealGenerator = () => {
    const { user } = useAuth();
    const [generatedMeal, setGeneratedMeal] = useState(null);
    const [loading, setLoading] = useState(false);

    // Load stored meal data on component mount
    useEffect(() => {
        const storedMeal = localStorage.getItem("generatedMeal");
        if (storedMeal) {
            setGeneratedMeal(JSON.parse(storedMeal));
        }
    }, []);

    const generateMeal = async () => {
        const email = user.email;
        setLoading(true);

        // Clear previously stored meal
        localStorage.removeItem("generatedMeal");

        try {
            // Generate the meal plan
            await axios.get(
                `https://nutrition-ai-backend.onrender.com/meal/generate_meal/${email}`,
                {
                    headers: {
                        accept: "application/json",
                    },
                    params: {
                        email_id: email,
                    },
                }
            );

            // Fetch the generated meal plan
            await showMeal();
        } catch (error) {
            console.error("Error generating meal:", error);
        }
        setLoading(false);
    };

    const showMeal = async () => {
        try {
            const response = await axios.get(
                `https://nutrition-ai-backend.onrender.com/meal/show_meal/${user.email}`,
                {
                    headers: {
                        accept: "application/json",
                    },
                    params: {
                        email_id: user.email,
                    },
                }
            );

            const mealData = response.data;

            // Log the meal data to verify the structure
            console.log("Fetched meal data:", mealData);

            // Convert the meal array to an object keyed by day (if it is an array)
            if (Array.isArray(mealData)) {
                const mealDataObject = mealData.reduce((acc, curr) => {
                    const dayKey = Object.keys(curr)[0]; // Extract day key (e.g., 'day1')
                    acc[dayKey] = curr[dayKey]; // Assign meals to the respective day
                    return acc;
                }, {});
                setGeneratedMeal(mealDataObject);
                localStorage.setItem("generatedMeal", JSON.stringify(mealDataObject));
            } else {
                console.error("Unexpected meal data structure:", mealData);
            }
        } catch (error) {
            console.error("Error showing meal:", error);
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
                className="btn btn-info text-white text-lg font-semibold mb-10 w-fit"
                onClick={generateMeal}
            >
                Generate Meal
            </button>

            {generatedMeal && (
                <div className="w-full">
                    <MealPlan mealDetails={generatedMeal} />
                </div>
            )}
        </div>
    );
};

export default MealGenerator;
