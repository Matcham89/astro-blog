import { defineConfig } from 'astro/config';
import expressiveCode from 'astro-expressive-code';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://astro-blog-1r2.pages.dev',
  integrations: [
    expressiveCode({
      themes: ['github-dark', 'github-light'],
      styleOverrides: {
        borderRadius: '0.5rem',
        borderWidth: '1px',
      },
      defaultProps: {
        wrap: true,
        preserveIndent: true,
      },
    }),
    tailwind()
  ]
});