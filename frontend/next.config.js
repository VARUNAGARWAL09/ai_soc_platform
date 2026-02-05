/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    optimizeFonts: true,
    transpilePackages: ['@react-pdf/renderer'],
    experimental: {
        optimizePackageImports: ['framer-motion'],
    },
    webpack: (config) => {
        config.resolve.alias.canvas = false;
        config.resolve.alias.encoding = false;
        return config;
    },
}

module.exports = nextConfig
