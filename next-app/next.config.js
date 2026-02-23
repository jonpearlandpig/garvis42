/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config) => {
    config.resolve.alias['@'] = require('path').resolve(__dirname, 'src');
    return config;
  },
  turbopack: {}, // Added to silence Turbopack/Webpack conflict
};

module.exports = nextConfig;
