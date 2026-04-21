"use client";

import { useState } from "react";

export default function AudioUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [audioList, setAudioList] = useState<string[]>([]);

  const handleUpload = () => {
    if (!file) {
      alert("Please select an audio file");
      return;
    }

    // convert file to URL
    const url = URL.createObjectURL(file);

    // store in list
    setAudioList((prev) => [...prev, url]);

    // reset input
    setFile(null);
  };

  return (
    <div className="glass-card p-6">

      <h2 className="text-lg font-semibold mb-4">📤 Upload Audio</h2>

      <input
        type="file"
        accept="audio/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4 w-full"
      />

      <button
        onClick={handleUpload}
        className="btn bg-blue-500 text-white"
      >
        Upload
      </button>

      {/* Display uploaded audios */}
      <div className="mt-4 space-y-2">
        {audioList.map((audio, index) => (
          <div key={index} className="p-2 bg-white rounded-lg shadow">
            <p className="text-sm text-gray-500">
              Uploaded {index + 1}
            </p>
            <audio controls src={audio} className="w-full" />
          </div>
        ))}
      </div>

    </div>
  );
}