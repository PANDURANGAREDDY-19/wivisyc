"use client";

import { useState, useRef } from "react";

export default function AudioRecorder() {
  const [recording, setRecording] = useState(false);
  const [audioList, setAudioList] = useState<string[]>([]);
  const mediaRecorder = useRef<any>(null);
  const chunks = useRef<any[]>([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder.current = new MediaRecorder(stream);

    mediaRecorder.current.ondataavailable = (e: any) => {
      chunks.current.push(e.data);
    };

    mediaRecorder.current.onstop = () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      const url = URL.createObjectURL(blob);
      setAudioList((prev) => [...prev, url]);
      chunks.current = [];
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorder.current.stop();
    setRecording(false);
  };

  return (
    <div className="glass-card p-6">

      <h2 className="text-lg font-semibold mb-4">🎙️ Recorder</h2>

      {/* Button */}
      <button
        onClick={recording ? stopRecording : startRecording}
        className={`btn text-white ${
          recording
            ? "bg-red-500 hover:bg-red-600"
            : "bg-blue-500 hover:bg-blue-600"
        }`}
      >
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {/* 🌊 Waveform animation */}
      {recording && (
        <div className="flex gap-1 mt-4 justify-center">
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="w-1 h-6 bg-blue-400 animate-pulse rounded"
              style={{
                animationDelay: `${i * 0.1}s`,
              }}
            />
          ))}
        </div>
      )}

      {/* Audio List */}
      <div className="mt-5 space-y-3">
        {audioList.map((audio, index) => (
          <div
            key={index}
            className="p-3 bg-white rounded-lg shadow-sm border"
          >
            <p className="text-sm text-gray-500">
              Recording {index + 1}
            </p>
            <audio controls src={audio} className="w-full mt-1" />
          </div>
        ))}
      </div>
    </div>
  );
}