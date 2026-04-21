import "./globals.css";
import Navbar from "@/components/Navbar";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-gray-50 to-gray-100 text-gray-800">
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1 flex justify-center items-center p-6">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}