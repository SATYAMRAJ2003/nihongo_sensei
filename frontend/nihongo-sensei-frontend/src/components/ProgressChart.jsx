function ProgressChart({ history }) {
  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold">📈 Progress Over Time</h3>

      <ul className="mt-2 space-y-1">
        {history.map((item, index) => (
          <li key={index} className="text-sm">
            Attempt {index + 1}: {item.score} ({item.jlpt})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProgressChart; // ✅ THIS LINE IS REQUIRED
