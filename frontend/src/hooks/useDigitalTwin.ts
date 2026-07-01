import { useState } from "react";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

// Ensure API URL is configurable via window object if embedded
const getApiUrl = () => {
  if (typeof window !== "undefined" && (window as any).__DIGITAL_TWIN_API_URL__) {
    return (window as any).__DIGITAL_TWIN_API_URL__;
  }
  return import.meta.env.VITE_API_URL || "http://localhost:8000";
};

export function useDigitalTwin() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: "Hi! I'm Ramveer's Digital Twin. Feel free to ask me about his experience, projects, or skills!"
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = async (content: string) => {
    if (!content.trim()) return;

    const userMessage: Message = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = getApiUrl();
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [...messages, userMessage].map(m => ({ role: m.role, content: m.content })),
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message.");
      }

      if (!response.body) throw new Error("No response body.");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;

      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      let assistantContent = "";

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split("\n");
          
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              const dataStr = line.slice(6);
              if (dataStr === "[DONE]") {
                done = true;
                break;
              }
              
              try {
                const data = JSON.parse(dataStr);
                if (data.text) {
                  assistantContent += data.text;
                  setMessages((prev) => {
                    const newMsgs = [...prev];
                    newMsgs[newMsgs.length - 1].content = assistantContent;
                    return newMsgs;
                  });
                }
              } catch (e) {
                // Ignore parse errors on partial chunks
              }
            }
          }
        }
      }
    } catch (err: any) {
      console.error(err);
      setError(err.message || "An error occurred.");
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I'm currently unavailable. Please try again later." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    messages,
    sendMessage,
    isLoading,
    error,
  };
}
