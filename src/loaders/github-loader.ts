// src/loaders/github-loader.ts
import matter from 'gray-matter';

// This topic tags the repos you want to appear on the blog
const BLOG_TOPIC = 'blog-post'; 

export async function githubLoader() {
  const username = import.meta.env.GITHUB_USERNAME;
  const token = import.meta.env.GITHUB_TOKEN;
  
  if (!token) throw new Error("Missing GITHUB_TOKEN");

  // 1. Fetch all repos for the user with the specific topic
  const repoResponse = await fetch(
    `https://api.github.com/search/repositories?q=user:${username}+topic:${BLOG_TOPIC}`,
    { headers: { Authorization: `token ${token}`, 'User-Agent': 'astro-blog-loader' } }
  );
  
  const { items: repos } = await repoResponse.json();
  
  // 2. Map over repos and fetch the raw README content for each
  const posts = await Promise.all(repos.map(async (repo: any) => {
    const rawUrl = `https://raw.githubusercontent.com/${username}/${repo.name}/${repo.default_branch}/README.md`;
    
    const contentRes = await fetch(rawUrl);
    if (!contentRes.ok) {
        console.warn(`Skipping ${repo.name}: No README found`);
        return null;
    }
    
    const rawMarkdown = await contentRes.text();
    
    // 3. Parse Frontmatter (metadata) from the Markdown
    const { data, content } = matter(rawMarkdown);

    return {
      id: repo.name, // The repo name becomes the URL slug
      ...data,       // Spread frontmatter (title, date, etc.)
      body: content, // The actual markdown text
      githubUrl: repo.html_url, // Link back to the repo
      stars: repo.stargazers_count // Bonus: Show star count!
    };
  }));

  return posts.filter(p => p !== null);
}