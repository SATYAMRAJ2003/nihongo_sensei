const ImprovementCard = ({ improvements }) => {
  return (
    <div className="bg-purple-50 border border-purple-300 p-4 rounded-xl">
      <h2 className="text-lg font-semibold">✨ Improved Sentences</h2>

      {improvements.map((item, i) => (
        <div key={i} className="mt-3">
          <p className="font-medium">{item.sentence}</p>
          <p className="text-sm text-gray-600">
            {item.reason} ({item.level})
          </p>
        </div>
      ))}
    </div>
  );
};

export default ImprovementCard;
