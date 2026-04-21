"use client";

import { useRouter } from "next/navigation";
import { v4 as uuid } from "uuid";
import { useState } from "react";

export default function Room() {
  const router = useRouter();
  const [roomId, setRoomId] = useState("");

  const generateRoomId = () => {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let id = "";
    for (let i = 0; i < 6; i++) {
      id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
  };

  const createRoom = () => {
    const id = generateRoomId();
    router.push(`/room/${id}`);
  };


  const joinRoom = () => {
    if (!roomId) return;
    router.push(`/room/${roomId}`);
  };

  return (
    <div className="w-full max-w-2xl text-center">

      {/* Header */}
      <div className="glass-card glow p-8 mb-6">
        <h1 className="text-3xl font-bold text-gray-700 mb-2">
          🎧 Audio Rooms
        </h1>
        <p className="text-gray-500">
          Create or join a room and start speaking across languages.
        </p>
      </div>

      {/* Actions */}
      <div className="glass-card p-8 space-y-6">

        {/* Create */}
        <div>
          <button
            onClick={createRoom}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-blue-500 to-indigo-500 text-white font-medium hover:scale-105 transition"
          >
            ➕ Create New Room
          </button>
        </div>

        {/* Divider */}
        <div className="text-gray-400 text-sm">OR</div>

        {/* Join */}
        <div className="flex gap-3">
          <input
            placeholder="Enter Room ID..."
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
            className="flex-1 px-4 py-2 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
          />

          <button
            onClick={joinRoom}
            className="px-5 py-2 rounded-xl bg-green-500 text-white hover:bg-green-600 transition"
          >
            Join
          </button>
        </div>

      </div>

      {/* Bottom Icons */}
      <div className="mt-8 flex justify-center gap-6 text-3xl opacity-70">
        🎙️ 🌐 🔊 🤝
      </div>
    </div>
  );
}