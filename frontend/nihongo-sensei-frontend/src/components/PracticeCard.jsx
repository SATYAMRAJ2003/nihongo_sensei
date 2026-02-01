const PracticeCard = ({ weakArea, recommendations }) => {
  return (
    <div className="bg-yellow-50 border border-yellow-300 p-4 rounded-xl">
      <h2 className="text-lg font-semibold">🎯 Focus Area</h2>

      <p className="mt-1">{weakArea.message}</p>

      <ul className="list-disc ml-6 mt-3">
        {recommendations.map((r, i) => (
          <li key={i}>{r}</li>
        ))}
      </ul>
    </div>
  );
};

export default PracticeCard;
