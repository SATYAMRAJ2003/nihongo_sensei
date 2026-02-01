const SenseiMessage = ({ message }) => {
  return (
    <div className="bg-white border p-4 rounded-xl shadow">
      <h2 className="text-lg font-semibold">👨‍🏫 Sensei</h2>
      <p className="mt-2">{message}</p>
    </div>
  );
};

export default SenseiMessage;
