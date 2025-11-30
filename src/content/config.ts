// src/content/config.ts
import { defineCollection, z } from 'astro:content';
import { githubLoader } from '../loaders/github-loader';

const blog = defineCollection({
  loader: githubLoader, 
  schema: z.object({
    title: z.string(),
    date: z.string().or(z.date()), // Handle flexible date formats
    description: z.string().optional(),
    githubUrl: z.string().url(),
    stars: z.number().optional(),
  })
});

export const collections = { blog };