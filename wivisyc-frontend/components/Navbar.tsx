"use client";

import Link from "next/link";
import { useStore } from "@/store/useStore";

export default function Navbar() {
  const user = useStore((s) => s.user);

  return (
    <header className="w-full bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200 px-8 py-4 flex justify-between items-center">
      
      {/* Logo */}
      <h1 className="text-xl font-semibold tracking-tight text-gray-700">
        🎙️ Wivisyc
      </h1>

      {/* Navigation */}
      <div className="flex items-center gap-6 text-sm">
        <Link href="/" className="hover:text-blue-500 transition">
          Home
        </Link>
        <Link href="/room" className="hover:text-blue-500 transition">
          Rooms
        </Link>

        {user ? (
          <div className="flex items-center gap-2">
            <img
              src={user.photoURL}
              className="w-8 h-8 rounded-full border"
            />
            <span className="text-gray-600">{user.displayName}</span>
          </div>
        ) : (
          <Link
            href="/login"
            className="px-4 py-2 rounded-lg bg-blue-500 text-white hover:bg-blue-600 transition"
          >
            Login
          </Link>
        )}
      </div>
    </header>
  );
}