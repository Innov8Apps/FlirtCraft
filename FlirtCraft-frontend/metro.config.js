const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// Performance optimizations
config.transformer.minifierPath = 'metro-minify-terser';
config.transformer.minifierConfig = {
  // Terser options for better performance
  ecma: 8,
  keep_fnames: true,
  mangle: {
    keep_fnames: true,
  },
};

// Enable lazy bundling for better performance
config.resolver.enableGlobalPackages = true;

module.exports = config;