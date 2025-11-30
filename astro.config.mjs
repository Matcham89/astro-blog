import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  integrations: [
    expressiveCode(),
    tailwind()
  ]
});