"use client";

import { useStore } from "@/store/useStore";

export default function Profile() {
  const user = useStore((s) => s.user);

  if (!user) {
    return (
      <div className="glass-card p-8 text-center">
        <p className="text-gray-500">Please login to view profile</p>
      </div>
    );
  }

  return (
    <div className="w-full max-w-xl">

      <div className="glass-card glow p-8 text-center">

        {/* Avatar */}
        <img
          src={user.photoURL}
          className="w-24 h-24 rounded-full mx-auto mb-4 border-4 border-white shadow"
        />

        {/* Name */}
        <h2 className="text-2xl font-semibold text-gray-700">
          {user.displayName}
        </h2>

        {/* Email */}
        <p className="text-gray-500 mt-1">{user.email}</p>

        {/* Divider */}
        <div className="border-t my-6"></div>

        {/* Info Cards */}
        <div className="grid grid-cols-2 gap-4 text-left">

          <div className="p-4 bg-white/60 rounded-xl">
            <p className="text-xs text-gray-400">Status</p>
            <p className="font-medium text-green-500">Active</p>
          </div>

          <div className="p-4 bg-white/60 rounded-xl">
            <p className="text-xs text-gray-400">Rooms Joined</p>
            <p className="font-medium text-blue-500">3</p>
          </div>

        </div>

      </div>
    </div>
  );
}