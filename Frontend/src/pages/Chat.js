import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";

const Chat = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState({});
  const [message, setMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const scrollRef = useRef();

  useEffect(() => {
    // Scroll to the bottom when new messages are added
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleUserQuery = async (userQuery) => {
    if (!message.trim()) {
      return;
    }

    const email = user.email;
    try {
      let newChatHistory = [...chatHistory];
      newChatHistory.push({
        user: userQuery,
        bot: "AI is thinking ...",
      });
      setChatHistory(newChatHistory);

      const requestBody = new URLSearchParams();
      requestBody.append("message", userQuery);
      requestBody.append("history", JSON.stringify(history));

      const config = {
        headers: {
          accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        params: {
          email_id: email,
        },
      };

      // Make a POST request to your chatbot service
      const response = await axios.post(
      "https://nutrition-ai-backend.onrender.com/health/chat",

        requestBody,
        config
      );


      // Assuming response.data has 'response' and 'history' fields
      newChatHistory[newChatHistory.length - 1].bot = response.data.response || "No response from AI";
      setHistory(response.data.history || {});
      setChatHistory(newChatHistory);
      setMessage("");

    } catch (error) {
      console.error("Error in handling user query -->", error.response?.data || error.message);
      // Optionally update UI with error
    }
  };


  return (
    <div className="pt-2 pb-5 px-2 w-full flex flex-col justify-end items-center gap-2 max-h-[93%] sm:max-h-[100%]">
      <div className="w-full overflow-auto invisible-scrollbar relative" ref={scrollRef}>
        {chatHistory.map((chat, index) => (
          <div key={index}>
            <div className="chat chat-end">
              <div className="chat-bubble chat-bubble-info">
                {chat.user}
              </div>
            </div>
            <div className="chat chat-start">
              <div className="chat-bubble chat-bubble-accent">
                {chat.bot}
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="flex gap-2 sm:gap-4">
        <input 
          className="input input-bordered text-center sm:w-[20rem] md:w-[30rem] lg:w-[35rem]"
          type="text"
          placeholder="Ask your question"
          onChange={(e) => setMessage(e.target.value)}
          value={message}
        />
        <button className="btn btn-info text-lg font-semibold text-white w-fit"
         onClick={() => handleUserQuery(message)}>Send</button>
        {/* You can add a "Stop" button if needed */}
      </div>
    </div>
  );
};

export default Chat;