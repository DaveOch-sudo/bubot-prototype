import apiClient from "./client";

export async function sendMessage(sender, message) {
  const response = await apiClient.post("/chat/", {
    sender,
    message,
  });

  return response.data;
}