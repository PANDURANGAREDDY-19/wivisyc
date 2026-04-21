"use client";

import { useParams } from "next/navigation";
import AudioRecorder from "@/components/AudioRecorder";
import AudioUpload from "@/components/AudioUpload";

export default function RoomPage() {
  const params = useParams();

  return (
    <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg border border-gray-200 p-8 transition-all duration-300">

      {/* Header */}
      <div className="mb-6 border-b pb-4">
        <h1 className="text-2xl font-semibold text-gray-700">
          Audio Room
        </h1>
        <p className="text-sm text-gray-400 mt-1">
          Room ID: {params.id}
        </p>
      </div>

      {/* Content */}
      <div className="space-y-6">
        <AudioRecorder />
        <AudioUpload />
      </div>
    </div>
  );
}