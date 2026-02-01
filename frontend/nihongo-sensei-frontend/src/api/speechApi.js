export const sendAudioToSensei = async (
  audioBlob,
  expectedText,
  sessionId
) => {
  const formData = new FormData();

  formData.append("file", audioBlob, "speech.webm");
  formData.append("expected_text", expectedText);

  if (sessionId) {
    formData.append("session_id", sessionId);
  }

  const response = await fetch("http://localhost:8000/speech-to-text", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload audio");
  }

  return await response.json();
};
