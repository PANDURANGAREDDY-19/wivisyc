"use client";

import { auth, provider } from "@/lib/firebase";
import { signInWithPopup } from "firebase/auth";
import { useRouter } from "next/navigation";
import { useStore } from "@/store/useStore";

export default function Login() {
  const router = useRouter();
  const setUser = useStore((s) => s.setUser);

  const handleLogin = async () => {
    const result = await signInWithPopup(auth, provider);
    setUser(result.user);
    router.push("/profile");
  };

  return (
    <div className="w-full max-w-md text-center">

      <div className="glass-card glow p-10">

        {/* Logo */}
        <div className="text-5xl mb-4">🌐🎙️</div>

        <h1 className="text-2xl font-semibold text-gray-700 mb-2">
          Welcome to Wivisyc
        </h1>

        <p className="text-gray-500 mb-6">
          Sign in to start real-time voice translation.
        </p>

        {/* Google Button */}
        <button
          onClick={handleLogin}
          className="w-full flex items-center justify-center gap-3 px-5 py-3 rounded-xl bg-white border shadow hover:shadow-md transition"
        >
          <span className="text-lg">🔐</span>
          <span className="text-gray-700 font-medium">
            Sign in with Google
          </span>
        </button>

      </div>

      {/* Bottom icons */}
      <div className="mt-6 text-2xl opacity-70">
        🎧 🌍 💬
      </div>
    </div>
  );
}