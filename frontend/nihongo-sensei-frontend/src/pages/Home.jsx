import { useEffect, useState } from "react";

import PronunciationCard from "../components/PronunciationCard";
import GrammarCard from "../components/GrammarCard";
import PracticeCard from "../components/PracticeCard";
import ImprovementCard from "../components/ImprovementCard";
import SenseiMessage from "../components/SenseiMessage";
import ProgressChart from "../components/ProgressChart";

import {
  loadHistory,
  saveHistory,
  clearHistory,
} from "../utils/storage";

function Home() {
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [audioFile, setAudioFile] = useState(null);
  const [expectedText, setExpectedText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 🔁 Load history on mount
  useEffect(() => {
    setHistory(loadHistory());
  }, []);

  // 💾 Save history on update
  useEffect(() => {
    saveHistory(history);
  }, [history]);

  // 🎧 Audio preview
  const audioUrl = audioFile ? URL.createObjectURL(audioFile) : null;

  // 🧹 Cleanup audio URL
  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  const handleSubmit = async () => {
    if (!audioFile) {
      setError("Please upload an audio file.");
      return;
    }

    const trimmedText = expectedText.trim();
    if (!trimmedText) {
      setError("Expected Japanese sentence cannot be empty.");
      return;
    }

    if (trimmedText.length < 5) {
      setError("Please enter at least 5 Japanese characters.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", audioFile);
      formData.append("expected_text", trimmedText);

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 15000);

      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/speech-to-text`,
        {
          method: "POST",
          body: formData,
          signal: controller.signal,
        }
      );

      clearTimeout(timeoutId);

      if (!res.ok) throw new Error("Server error. Please try again.");

      const data = await res.json();
      setResult(data);

      setHistory((prev) => [
        ...prev,
        {
          japanese: data.japanese,
          score: data.pronunciation_score,
          jlpt: data.pronunciation_jlpt,
        },
      ]);
    } catch (err) {
      if (err.name === "AbortError") {
        setError("Request timed out. Please try again.");
      } else if (err instanceof TypeError) {
        setError("Cannot connect to server. Is backend running?");
      } else {
        setError(err.message || "Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = () => {
    if (!window.confirm("Clear all practice history?")) return;
    clearHistory();
    setHistory([]);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-3xl mx-auto space-y-6">
        <header className="text-center">
          <h1 className="text-2xl font-bold text-gray-800">🎌 Nihongo Sensei</h1>
          <p className="text-sm text-gray-500">
            Improve your Japanese pronunciation & grammar
          </p>
        </header>

        {/* Upload Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmit();
          }}
          className="space-y-4"
        >
          <label className="block text-sm font-medium text-gray-700">
            Upload pronunciation audio
          </label>

          <input
            type="file"
            accept="audio/*"
            disabled={loading}
            onChange={(e) => {
              setAudioFile(e.target.files[0]);
              setResult(null);
              setError(null);
            }}
          />

          {audioFile && (
            <p className="text-sm text-gray-600">
              Selected file: <strong>{audioFile.name}</strong>
            </p>
          )}

          {audioUrl && (
            <audio controls className="w-full">
              <source src={audioUrl} />
            </audio>
          )}

          <label className="block text-sm font-medium text-gray-700">
            Expected Japanese sentence
          </label>

          <input
            type="text"
            placeholder="例: 私は日本語を勉強しています"
            value={expectedText}
            disabled={loading}
            onChange={(e) => setExpectedText(e.target.value)}
            className="border p-2 w-full rounded disabled:bg-gray-100"
          />

          <button
            type="submit"
            disabled={loading}
            className={`w-full px-4 py-2 rounded text-white ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          {loading && (
            <p className="text-sm text-center text-gray-500">
              🎧 Sensei is carefully analyzing your speech...
            </p>
          )}
        </form>

        {error && <p className="text-red-500 text-center">{error}</p>}

        {/* Results */}
        {result && (
          <div className="space-y-4">
            <PronunciationCard
              score={result.pronunciation_score}
              jlpt={result.pronunciation_jlpt}
              feedback={result.pronunciation_feedback}
              progress={result.progress_feedback}
            />

            <GrammarCard
              patterns={result.grammar_patterns}
              level={result.grammar_jlpt}
              feedback={result.grammar_feedback}
              mistakes={result.grammar_mistakes}
              corrections={result.grammar_corrections}
            />

            <PracticeCard
              weakArea={result.weak_area}
              recommendations={result.practice_recommendations}
            />

            <ImprovementCard improvements={result.improved_sentences} />
            <SenseiMessage message={result.sensei_reply} />
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <section className="space-y-3">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">📊 Practice History</h2>
              <button
                onClick={handleClearHistory}
                className="text-sm px-3 py-1 rounded bg-red-500 text-white hover:bg-red-600"
              >
                Clear History
              </button>
            </div>

            <ul className="space-y-2">
              {history.map((item, index) => (
                <li
                  key={index}
                  className="border p-2 rounded flex justify-between"
                >
                  <span>{item.japanese}</span>
                  <span className="font-semibold">
                    {item.score} ({item.jlpt})
                  </span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {history.length > 1 && <ProgressChart history={history} />}
      </div>
    </div>
  );
}

export default Home;
