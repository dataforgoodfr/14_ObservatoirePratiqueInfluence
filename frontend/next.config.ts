import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  images: { unoptimized: true },
  // Note:
  // GH pages deployment generally require to configure a basePath.
  // However this is not needed here as we have mapped a subdomain in gh config (observatoire.payetoninfluence.org)
};

export default nextConfig;
