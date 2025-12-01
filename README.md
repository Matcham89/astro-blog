# Chris Matcham - Platform Engineer Blog

[![Deploy to Cloudflare Pages](https://img.shields.io/badge/Deploy-Cloudflare%20Pages-F38020?logo=cloudflare&logoColor=white)](https://astro-blog-1r2.pages.dev)
[![Built with Astro](https://img.shields.io/badge/Built%20with-Astro-FF5D01?logo=astro&logoColor=white)](https://astro.build)
[![Hub & Spoke Architecture](https://img.shields.io/badge/Architecture-Hub%20%26%20Spoke-blue)](https://github.com/Matcham89)

> A modern blog platform with content sourced directly from GitHub repositories using the Hub & Spoke architecture.

**Live Site**: [https://astro-blog-1r2.pages.dev](https://chrismatcham.dev)

---

## 🏗️ Architecture Overview

This blog uses a unique **Hub & Spoke** architecture:

- **Hub** (this repo): Astro-powered static site that fetches and displays blog post metadata
- **Spokes**: Individual GitHub repositories tagged with `blog-post`, each containing a single blog post in its README

### How It Works

1. **Content Creation**: Write a blog post in a new GitHub repository's `README.md`
2. **Tagging**: Add the `blog-post` topic to the repository
3. **Update Trigger**: Add entry to this README's "Latest Posts" section (triggers rebuild)
4. **Auto-Fetch**: Astro build fetches all repos tagged with `blog-post` via GitHub API
5. **Display**: Blog homepage displays posts with descriptions and links to GitHub
6. **Read**: Users click to read posts natively on GitHub

---

## 📝 Latest Posts

<!--
  🔔 IMPORTANT: Each time you add a new blog post repository, add it to the list below.
  This will trigger a Cloudflare Pages rebuild and fetch your new content.

  Template:
  - **[YYYY-MM-DD]** [Post Title](https://github.com/Matcham89/repo-name)
-->

### 2025

- **[2025-09-30]** [How to Create a Google Cloud Project (GCP) Step-by-Step](https://github.com/Matcham89/how-to-create-a-google-cloud-project-gcp-step-by-step)
- **[2025-09-17]** [Cloud Engineer Reveals Top Job Hunting Strategies](https://github.com/Matcham89/cloud-engineer-reveals-top-job-hunting-strategies)
- **[2025-08-22]** [The Secret to Getting Hired in Tech Quickly](https://github.com/Matcham89/the-secret-to-getting-hired-in-tech-quickly)
- **[2025-08-16]** [I Tried Building My Own MCP Tool From Scratch](https://github.com/Matcham89/i-tried-building-my-own-mcp-tool-from-scratch)
- **[2025-05-08]** [Exploring ArgoCD's New MCP Server with Kagent](https://github.com/Matcham89/Exploring-ArgoCD-s-New-MCP-Server-with-Kagent)
- **[2025-05-05]** [Deploying a K8S Ninja using Kagent MCP with ArgoCD & Helm](https://github.com/Matcham89/Deploying-a-K8S-ninja-using-kagent-MCP-with-ArgoCD-Helm)
- **[2025-05-01]** [Simple Portable Kubernetes Lab](https://github.com/Matcham89/Simple-Portable-Kubernetes-Lab)
- **[2025-03-31]** [Certified Kubernetes Application Developer Exam: What You Really Need To Know!](https://github.com/Matcham89/Certified-Kubernetes-Application-Developer-Exam.-What-You-Really-Need-To-Know)
- **[2025-01-14]** [Why I Switched From Hostinger To Github Pages](https://github.com/Matcham89/Why-I-Switched-From-Hostinger-To-Github-Pages)
- **[2025-01-10]** [Cloud Computing Trends and Essential Skills for 2025](https://github.com/Matcham89/Cloud-Computing-Trends-and-Essential-Skills-for-2025)
- **[2025-01-01]** [Hands-On Kubernetes: Part 2 - Deploying Vault](https://github.com/Matcham89/Hands-On-Kubernetes-Part-2-Deploying-Vault)

### 2024

- **[2024-12-21]** [Hands-On Kubernetes: Part 1 - Deploying Kind](https://github.com/Matcham89/Hands-On-Kubernetes-Part-1-Deploying-Kind)
- **[2024-12-14]** [Local Kubernetes Development: A Journey to KIND](https://github.com/Matcham89/Local-Kubernetes-Development-A-Journey-to-KIND)
- **[2024-12-07]** [Lokalise Translations With Github Actions](https://github.com/Matcham89/2024-12-7-Lokalise-Translations-With-Github-Actions)
- **[2024-12-01]** [ArgoCD Multi-Source Deployments for Google Config Connector](https://github.com/Matcham89/2024-12-1-ArgoCD-Multi-Source-Deployments-for-Google-Config-Connector)
- **[2024-11-15]** [Cloud Computing Trends and Essential Skills for 2024](https://github.com/Matcham89/Cloud-Computing-Trends-and-Essential-Skills-for-2024)
- **[2024-11-01]** [Transforming Your GitHub Profile: From Basic to Brilliant](https://github.com/Matcham89/Transforming-Your-GitHub-Profile-From-Basic-to-Brilliant)
- **[2024-06-17]** [I Tried Building My Own MCP Tool From Scratch (2024)](https://github.com/Matcham89/i-tried-building-my-own-mcp-tool-from-scratch-2024)

### 2023

- **[2023-11-01]** [Google Cloud Professional Cloud Architect Exam](https://github.com/Matcham89/Google-Cloud-Professional-Cloud-Architect-Exam)
- **[2023-08-13]** [I Tried Building My Own MCP Tool From Scratch (2023)](https://github.com/Matcham89/i-tried-building-my-own-mcp-tool-from-scratch-2023)

<!-- Total posts: 20 -->
<!-- Add new posts above this line, in reverse chronological order (newest first) -->

---

## 🚀 Tech Stack

- **[Astro 5.0](https://astro.build)** - Static site generator with Content Layer API
- **[Tailwind CSS](https://tailwindcss.com)** - Utility-first CSS framework
- **[Expressive Code](https://github.com/expressive-code/expressive-code)** - Syntax highlighting
- **[Cloudflare Pages](https://pages.cloudflare.com)** - Deployment and hosting
- **GitHub API** - Content fetching and aggregation

---

## 📂 Project Structure

```
astro-blog/
├── src/
│   ├── content/
│   │   └── config.ts          # Content collection schema
│   ├── layouts/
│   │   └── Layout.astro       # Base layout with glassmorphism
│   ├── loaders/
│   │   └── github-loader.ts   # Custom Content Layer loader
│   ├── pages/
│   │   └── index.astro        # Homepage listing all posts
│   └── env.d.ts               # TypeScript environment definitions
├── public/                     # Static assets
├── astro.config.mjs           # Astro configuration
├── tailwind.config.mjs        # Tailwind configuration
└── .env                       # Environment variables (not committed)
```

---

## 🔧 Local Development

### Prerequisites

- Node.js 22.x or later
- GitHub Personal Access Token with `public_repo` scope

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Matcham89/astro-blog.git
   cd astro-blog
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add:
   ```env
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_USERNAME=Matcham89
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

   Open [http://localhost:4321](http://localhost:4321)

5. **Build for production**
   ```bash
   npm run build
   ```

---

## ✍️ Creating a New Blog Post

### Step 1: Create a New Repository

```bash
# Create a new public repository
gh repo create Matcham89/my-post-slug --public --description "Post description here"
cd my-post-slug
```

### Step 2: Write Your Post

Create a `README.md` with frontmatter:

```markdown
---
title: "Your Post Title"
date: "2025-11-30"
description: "A brief description of your post (shows on homepage)"
---

# Your Post Title

Your blog post content here in Markdown...

## Sections

- Use standard markdown
- Add code blocks
- Include images

![Image description](./images/example.png)
```

### Step 3: Tag the Repository

```bash
# Add the blog-post topic
gh repo edit Matcham89/my-post-slug --add-topic blog-post
```

### Step 4: Trigger a Rebuild

Edit this README and add your post to the "Latest Posts" section:

```markdown
- **[2025-11-30]** [Your Post Title](https://github.com/Matcham89/my-post-slug) - Brief description
```

Commit and push:

```bash
git add README.md
git commit -m "Add new blog post: Your Post Title"
git push
```

This will trigger a Cloudflare Pages rebuild that fetches your new post!

---

## 🎨 Design Features

### Glassmorphism UI
- Frosted glass panels with backdrop blur
- Semi-transparent cards with subtle gradients
- Responsive design for all devices
- Dark mode optimized

### Color Scheme
- **Primary**: Blue → Purple → Pink gradient
- **Background**: Subtle slate tones with dot pattern
- **Accent**: Color-coded stats (blue, purple, pink)

### Typography
- Professional hierarchy with responsive sizing
- Readable prose styling
- Code syntax highlighting with GitHub themes

---

## 🔐 Environment Variables

Required for both local development and Cloudflare Pages deployment:

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token with `public_repo` scope | ✅ Yes |
| `GITHUB_USERNAME` | Your GitHub username (`Matcham89`) | ✅ Yes |

### Setting up in Cloudflare Pages

1. Go to your Pages project → **Settings** → **Environment Variables**
2. Add both variables for **Production** and **Preview** environments
3. Redeploy to apply changes

---

## 📦 Deployment

### Cloudflare Pages Configuration

- **Build command**: `npm run build`
- **Build output directory**: `dist`
- **Framework preset**: Astro
- **Node version**: 22.x

### Automatic Deployments

Every push to `main` triggers a rebuild that:
1. Fetches all repositories tagged with `blog-post`
2. Parses frontmatter from each README
3. Generates static pages with post listings
4. Deploys to Cloudflare Pages edge network

---

## 🧪 Testing the GitHub API

Verify your setup fetches posts correctly:

```bash
# Test API call
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=user:Matcham89+topic:blog-post"
```

---

## 📊 Blog Statistics

The homepage automatically displays:
- **Total Posts**: Count of all `blog-post` tagged repos
- **Total Stars**: Combined stars across all blog repositories
- **Total Reading Time**: Estimated reading time (200 words/min)

---

## 🔄 Migration from Jekyll

Migrating from the old [matcham89.github.io](https://github.com/Matcham89/matcham89.github.io) Jekyll blog!

---

## 🤝 Contributing

This is a personal blog, but if you find bugs or have suggestions:

1. Open an issue describing the problem/enhancement
2. Feel free to fork and submit a PR
3. Ensure code follows the existing style

---

## 📄 License

MIT License - Feel free to use this architecture for your own blog!

---

## 🔗 Links

- **Blog**: [astro-blog-1r2.pages.dev](https://chrismatcham.dev)
- **GitHub**: [@Matcham89](https://github.com/Matcham89)
- **LinkedIn**: [Christopher Matcham](https://www.linkedin.com/in/christophermatcham/)
- **YouTube**: [@ChrisMatcham](https://www.youtube.com/@ChrisMatcham)

---

## 💡 Why Hub & Spoke?

This architecture offers several advantages:

✅ **Version Control**: Each post is a Git repository with full history
✅ **Collaboration**: Others can open issues/PRs on your posts
✅ **Portability**: Posts aren't locked to one platform
✅ **Native GitHub**: Users benefit from GitHub's markdown rendering
✅ **Discoverability**: Posts are individual repos, easier to find
✅ **Interactive**: Stars, forks, and engagement per post

---

<div align="center">

**Built with ❤️ by Chris Matcham**

*Senior Platform Engineer | Cloud Infrastructure | DevOps*

</div>
