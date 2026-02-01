const PronunciationCard = ({ score, jlpt, feedback, progress }) => {
  return (
    <div className="bg-green-50 border border-green-300 p-4 rounded-xl">
      <h2 className="text-lg font-semibold">🗣 Pronunciation</h2>

      <p className="text-3xl font-bold text-green-700">{score}%</p>
      <p>JLPT Level: <b>{jlpt}</b></p>

      <p className="mt-2">{feedback}</p>

      {progress && (
        <p className="mt-2 text-sm text-gray-600">📈 {progress}</p>
      )}
    </div>
  );
};

export default PronunciationCard;
