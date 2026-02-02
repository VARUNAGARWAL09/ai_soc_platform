/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    swcMinify: true,
    transpilePackages: ['@react-pdf/renderer'],
    webpack: (config) => {
        config.resolve.alias.canvas = false;
        config.resolve.alias.encoding = false;
        return config;
    },
}

module.exports = nextConfig
