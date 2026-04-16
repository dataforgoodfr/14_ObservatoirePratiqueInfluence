import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  async headers() {
    return [
      {
        source: "/key-metrics",
        headers: [
          {
            key: "Content-Security-Policy",
            value: `frame-src ${process.env.METABASE_URL ?? "https://opi-metabase.services.d4g.fr"}`,
          },
        ],
      },
    ];
  },
};

export default nextConfig;
