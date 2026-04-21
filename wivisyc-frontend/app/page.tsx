import Link from "next/link";

export default function Home() {
  return (
    <div className="w-full max-w-4xl text-center">

      {/* Hero Section */}
      <div className="glass-card glow p-10">

        <h1 className="text-4xl font-bold text-gray-700 mb-4">
          🌍 Wivisyc
        </h1>

        <p className="text-gray-500 mb-6 text-lg">
          Real-time voice communication with intelligent translation.
          Speak naturally. Connect globally.
        </p>

        {/* Buttons */}
        <div className="flex justify-center gap-4">
          <Link href="/login">
            <button className="px-6 py-3 rounded-xl bg-blue-500 text-white hover:bg-blue-600 transition">
              Get Started
            </button>
          </Link>

          <Link href="/room">
            <button className="px-6 py-3 rounded-xl bg-white border border-gray-300 hover:bg-gray-100 transition">
              Join Room
            </button>
          </Link>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid md:grid-cols-3 gap-6 mt-10">

        <div className="glass-card p-6 text-left">
          <h3 className="font-semibold text-gray-700 mb-2">🎙️ Voice First</h3>
          <p className="text-sm text-gray-500">
            Natural voice interaction with high-quality audio capture.
          </p>
        </div>

        <div className="glass-card p-6 text-left">
          <h3 className="font-semibold text-gray-700 mb-2">🌐 Live Translate</h3>
          <p className="text-sm text-gray-500">
            Break language barriers with real-time translation.
          </p>
        </div>

        <div className="glass-card p-6 text-left">
          <h3 className="font-semibold text-gray-700 mb-2">🤝 Collaborative</h3>
          <p className="text-sm text-gray-500">
            Join rooms and communicate seamlessly with others.
          </p>
        </div>

      </div>
    </div>
  );
}