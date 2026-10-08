import { useState } from "react";
import { sendMessage } from "./api/chat";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!message.trim()) {
      return;
    }

    setLoading(true);

    try {
      const data = await sendMessage("web-user", message);

      const text = data.responses
        .map((item) => item.text)
        .join("\n");

      setResponse(text);
      setMessage("");
    } catch (error) {
      console.error(error);
      setResponse("Sorry, something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>BuBot</h1>

      <form onSubmit={handleSubmit}>
        <input
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Ask BuBot something..."
        />

        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {response && (
        <p>
          <strong>BuBot:</strong> {response}
        </p>
      )}
    </main>
  );
}

export default App;