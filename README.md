# Chris Matcham - Platform Engineer Blog

[![Deploy to Cloudflare Pages](https://img.shields.io/badge/Deploy-Cloudflare%20Pages-F38020?logo=cloudflare&logoColor=white)](https://astro-blog-1r2.pages.dev)
[![Built with Astro](https://img.shields.io/badge/Built%20with-Astro-FF5D01?logo=astro&logoColor=white)](https://astro.build)
[![Hub & Spoke Architecture](https://img.shields.io/badge/Architecture-Hub%20%26%20Spoke-blue)](https://github.com/Matcham89)

> A modern blog platform with content sourced directly from GitHub repositories using the Hub & Spoke architecture.

**Live Site**: [https://astro-blog-1r2.pages.dev](https://astro-blog-1r2.pages.dev)

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
  - **[YYYY-MM-DD]** [Post Title](https://github.com/Matcham89/repo-name) - Brief description
-->

### 2025

- **[2025-11-30]** [Blog Test](https://github.com/Matcham89/blog-test) - Testing the Hub & Spoke blog architecture

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

Migrating from the old [matcham89.github.io](https://github.com/Matcham89/matcham89.github.io) Jekyll blog? See [`MIGRATION_PROMPT.md`](./MIGRATION_PROMPT.md) for detailed instructions on automating the migration process.

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

- **Blog**: [astro-blog-1r2.pages.dev](https://astro-blog-1r2.pages.dev)
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

*Platform Engineer | Cloud Infrastructure | DevOps*

</div>