import { useState } from "react";
import axios from "axios";

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await axios.post("/api/resume/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error uploading resume");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Resume</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 rounded">
        Upload
      </button>

      {result && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          <h3 className="font-bold">AI Analysis:</h3>
          <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
