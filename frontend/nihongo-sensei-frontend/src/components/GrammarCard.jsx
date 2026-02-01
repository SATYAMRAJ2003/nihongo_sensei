const GrammarCard = ({
  patterns,
  level,
  feedback,
  mistakes,
  corrections
}) => {
  return (
    <div className="bg-blue-50 border border-blue-300 p-4 rounded-xl">
      <h2 className="text-lg font-semibold">📘 Grammar</h2>

      <p>JLPT Level: <b>{level}</b></p>
      <p className="mt-2">{feedback}</p>

      <div className="mt-3">
        <p className="font-medium">Patterns Used:</p>
        <ul className="list-disc ml-6">
          {patterns.map((p, i) => (
            <li key={i}>{p}</li>
          ))}
        </ul>
      </div>

      {mistakes.length > 0 && (
        <div className="mt-3 text-red-600">
          <p className="font-medium">Mistakes Found</p>
          <ul className="list-disc ml-6">
            {mistakes.map((m, i) => (
              <li key={i}>{m}</li>
            ))}
          </ul>
        </div>
      )}

      {corrections.length > 0 && (
        <div className="mt-3 text-green-700">
          <p className="font-medium">Corrections</p>
          <ul className="list-disc ml-6">
            {corrections.map((c, i) => (
              <li key={i}>{c}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default GrammarCard;
