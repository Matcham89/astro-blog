// src/loaders/github-loader.ts
import matter from 'gray-matter';
import type { Loader } from 'astro/loaders';

// This topic tags the repos you want to appear on the blog
const BLOG_TOPIC = 'blog-post';

export function githubLoader(): Loader {
  return {
    name: 'github-loader',
    load: async ({ store, logger }) => {
      const username = process.env.GITHUB_USERNAME || import.meta.env.GITHUB_USERNAME;
      const token = process.env.GITHUB_TOKEN || import.meta.env.GITHUB_TOKEN;

      if (!token) throw new Error("Missing GITHUB_TOKEN");
      if (!username) throw new Error("Missing GITHUB_USERNAME");

      logger.info(`Fetching blog posts from GitHub for user: ${username}`);

      // 1. Fetch all repos for the user with the specific topic
      const repoResponse = await fetch(
        `https://api.github.com/search/repositories?q=user:${username}+topic:${BLOG_TOPIC}`,
        { headers: { Authorization: `token ${token}`, 'User-Agent': 'astro-blog-loader' } }
      );

      if (!repoResponse.ok) {
        throw new Error(`GitHub API error: ${repoResponse.statusText}`);
      }

      const { items: repos } = await repoResponse.json();

      logger.info(`Found ${repos.length} repositories with topic "${BLOG_TOPIC}"`);

      // Clear existing entries
      store.clear();

      // 2. Map over repos and fetch the raw README content for each
      await Promise.all(repos.map(async (repo: any) => {
        const rawUrl = `https://raw.githubusercontent.com/${username}/${repo.name}/${repo.default_branch}/README.md`;

        try {
          const contentRes = await fetch(rawUrl);
          if (!contentRes.ok) {
            logger.warn(`Skipping ${repo.name}: No README found`);
            return;
          }

          const rawMarkdown = await contentRes.text();

          // 3. Parse Frontmatter (metadata) from the Markdown
          const { data, content } = matter(rawMarkdown);

          // 4. Store the entry using the Content Layer API
          store.set({
            id: repo.name, // The repo name becomes the URL slug
            data: {
              title: data.title || repo.name,
              date: data.date || repo.created_at,
              description: data.description || repo.description,
              githubUrl: repo.html_url,
              stars: repo.stargazers_count,
            },
            body: content,
          });

          logger.info(`Loaded post: ${repo.name}`);
        } catch (error) {
          logger.warn(`Error loading ${repo.name}: ${error}`);
        }
      }));
    }
  };
}