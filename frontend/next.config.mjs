/** @type {import('next').NextConfig} */
const isProd = process.env.TAURI_BUILD === "1";

const nextConfig = isProd
  ? { output: "export", images: { unoptimized: true } }
  : {
      async rewrites() {
        const apiOrigin =
          process.env.MEETFLOW_API_ORIGIN || "http://127.0.0.1:8000";
        return [
          {
            source: "/__meetflow/api/:path*",
            destination: `${apiOrigin.replace(/\/$/, "")}/api/:path*`,
          },
        ];
      },
    };

export default nextConfig;
