const MealPlan = ({ mealDetails }) => {
  const dayToWeekDay = {
    day1: "Monday",
    day2: "Tuesday",
    day3: "Wednesday",
    day4: "Thursday",
    day5: "Friday",
    day6: "Saturday",
    day7: "Sunday",
  };

  return (
      <div className="relative shadow-md rounded-lg overflow-hidden">
        <table className="w-full text-sm sm:text-base">
          <thead className="uppercase bg-base-300">
          <tr>
            <th scope="col" className="sm:px-6 sm:py-3 p-2 text-start">
              Day
            </th>
            <th scope="col" className="sm:px-6 sm:py-3 p-2 text-start">
              Breakfast
            </th>
            <th scope="col" className="sm:px-6 sm:py-3 p-2 text-start">
              Lunch
            </th>
            <th scope="col" className="sm:px-6 sm:py-3 p-2 text-start">
              Dinner
            </th>
          </tr>
          </thead>
          <tbody>
          {Object.entries(mealDetails).map(([day, value]) => (
              <tr key={day} className="bg-base-200 border-b border-b-base-300 capitalize">
                <td className="sm:px-6 sm:py-3 p-2">{dayToWeekDay[day]}</td>
                <td className="sm:px-6 sm:py-3 p-2">{value.breakfast || 'N/A'}</td>
                <td className="sm:px-6 sm:py-3 p-2">{value.lunch || 'N/A'}</td>
                <td className="sm:px-6 sm:py-3 p-2">{value.dinner || 'N/A'}</td>
              </tr>
          ))}
          </tbody>
        </table>
      </div>
  );
};

export default MealPlan;
