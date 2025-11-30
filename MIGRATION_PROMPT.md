# Jekyll to Hub & Spoke Blog Migration Instructions

## Objective
Migrate all blog posts from the Jekyll-based `matcham89.github.io` repository to individual GitHub repositories, each tagged with `blog-post` for automatic fetching by the new Astro blog.

## Prerequisites & Permissions Required

### GitHub CLI Authentication
You will need the following GitHub CLI permissions:
- `repo` - Full control of private repositories (to create public repos and manage content)
- `workflow` - Update GitHub Actions workflows (if posts contain workflow files)

### Required Tools
- GitHub CLI (`gh`) must be installed and authenticated
- `git` command-line tool
- Access to clone the source repository: `https://github.com/Matcham89/matcham89.github.io`

## Source Repository Details

- **Source Repo**: `Matcham89/matcham89.github.io`
- **Blog Engine**: Jekyll with Minimal Mistakes theme
- **Posts Location**: `_posts/` directory
- **Post Format**: Markdown files with YAML frontmatter
- **Naming Convention**: Jekyll standard `YYYY-MM-DD-post-slug.md`

## Migration Requirements

### 1. Repository Creation
- **Visibility**: Create PUBLIC repositories (required for blog fetching)
- **Naming Strategy**: Use the post slug from the filename
  - Example: `2024-01-15-deploying-kubernetes.md` → repo name: `deploying-kubernetes`
- **Owner**: `Matcham89`
- **Topic**: Each repo MUST be tagged with `blog-post` topic

### 2. Frontmatter Transformation

**Extract from Jekyll frontmatter:**
```yaml
---
title: "Post Title Here"
date: 2024-01-15
categories: [category1, category2]
tags: [tag1, tag2]
excerpt: "Post excerpt here"
header:
  image: /assets/images/image.jpg
# ... other Jekyll fields
---
```

**Transform to new format (keep ONLY essential fields):**
```yaml
---
title: "Post Title Here"
date: "2024-01-15"
description: "Post excerpt here"
---
```

**Rules:**
- `title`: Required - use original title
- `date`: Required - use original date, format as YYYY-MM-DD string
- `description`: Optional - use `excerpt` field if available, otherwise first paragraph of content
- **DISCARD**: All other Jekyll-specific fields (categories, tags, header, layout, etc.)

### 3. Content Processing

**Image Handling:**
- Scan post content for image references
- If images are referenced in `_posts/` content:
  - Check if image exists in source repo's `assets/` or `images/` directories
  - If found: Copy image to new repo and update markdown reference
  - If not found: Keep original URL reference to `matcham89.github.io`
- Images should be placed in an `images/` or `assets/` folder in the new repo
- Update markdown image paths to be relative: `![alt](./images/image.jpg)`

**Content Cleanup:**
- Remove Jekyll-specific liquid tags: `{% ... %}`
- Remove Jekyll includes: `{% include ... %}`
- Keep all standard markdown formatting
- Preserve code blocks with syntax highlighting
- Keep all links (both internal and external)

### 4. Repository Structure

Each new repository should have:
```
repo-name/
├── README.md          # The migrated blog post content
├── images/           # (if post has images) Referenced images
│   └── image.jpg
└── .gitignore        # Basic gitignore for images/editor files
```

**README.md Structure:**
```markdown
---
title: "Post Title"
date: "YYYY-MM-DD"
description: "Post description"
---

[Original post content here, cleaned of Jekyll-specific syntax]
```

### 5. Repository Metadata

For each repository:
- **Description**: Use the post description/excerpt (max 350 characters)
- **Topics**: MUST include `blog-post` (required for fetching)
- **Homepage URL**: Leave empty or set to `https://chrismatcham.dev`
- **README**: Enabled (auto-created with content)

## Step-by-Step Process

### Step 1: Clone Source Repository
```bash
git clone https://github.com/Matcham89/matcham89.github.io
cd matcham89.github.io
```

### Step 2: Process Each Post

For each markdown file in `_posts/`:

1. **Parse filename** to extract:
   - Date: `YYYY-MM-DD`
   - Slug: Everything after the date (repo name)

2. **Parse frontmatter** to extract:
   - title
   - date (use from frontmatter, fallback to filename)
   - description/excerpt

3. **Extract content** (everything after frontmatter)

4. **Process images**:
   - Find all image references: `![...](...)`
   - If path is relative and exists in source repo, copy image
   - Update image paths in content

5. **Create new repository**:
   ```bash
   gh repo create Matcham89/[repo-slug] \
     --public \
     --description "[post-description]" \
     --clone
   ```

6. **Set repository topic**:
   ```bash
   gh repo edit Matcham89/[repo-slug] \
     --add-topic blog-post
   ```

7. **Create README.md** with new frontmatter + cleaned content

8. **Copy images** (if any) to `images/` directory

9. **Commit and push**:
   ```bash
   cd [repo-slug]
   git add .
   git commit -m "Migrate blog post from Jekyll site"
   git push origin main
   cd ..
   ```

### Step 3: Verify Migration

After processing all posts:
1. List all repositories with `blog-post` topic:
   ```bash
   gh repo list Matcham89 --topic blog-post --json name,description
   ```
2. Verify count matches number of posts in `_posts/`
3. Spot-check a few repositories to ensure:
   - README.md has correct frontmatter
   - Content is properly formatted
   - Images are accessible
   - `blog-post` topic is set

## Error Handling

**If repository creation fails:**
- Log the error
- Continue with next post
- Report failed posts at the end

**If image is referenced but not found:**
- Log a warning with post name and image path
- Leave original image reference in markdown
- Continue processing

**If frontmatter is malformed:**
- Log error with filename
- Attempt to extract title from first heading
- Use filename date
- Continue with partial frontmatter

## Expected Output

At completion, you should have:
- ✅ One public GitHub repository per blog post
- ✅ Each repo tagged with `blog-post` topic
- ✅ Clean README.md with proper frontmatter
- ✅ Images copied where applicable
- ✅ Summary report showing:
  - Total posts processed
  - Successfully created repositories
  - Failed migrations (if any)
  - Warnings (missing images, etc.)

## Verification Command

After migration, test the blog loader:
```bash
# This should fetch all migrated posts
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=user:Matcham89+topic:blog-post"
```

## Important Notes

1. **DO NOT delete** the original `matcham89.github.io` repository until migration is verified
2. **Repository names must be unique** - if a repo name already exists, append a number: `post-slug-2`
3. **Rate Limiting**: GitHub API has rate limits. Add delays between repo creations if processing many posts
4. **Commit messages**: Use consistent format for easy tracking
5. **Dry run option**: Consider implementing a `--dry-run` flag to preview changes before executing

## Questions to Ask Before Starting

- [ ] Do you have `gh` CLI installed and authenticated?
- [ ] Do you have write access to create repos under `Matcham89`?
- [ ] Should I create a backup/log file of the migration process?
- [ ] Do you want to migrate ALL posts or start with a specific subset?
- [ ] Should I archive/mark the old Jekyll repo after successful migration?

## Example Migration

**Source**: `_posts/2024-01-15-kubernetes-deployment.md`
```yaml
---
title: "Deploying Kubernetes on AWS"
date: 2024-01-15
categories: [DevOps, Kubernetes]
tags: [aws, k8s, cloud]
excerpt: "A guide to deploying Kubernetes clusters on AWS EKS"
header:
  image: /assets/images/k8s-header.jpg
---

![Architecture](../images/k8s-arch.png)

Content here...
```

**Result**: Repository `Matcham89/kubernetes-deployment`
- README.md:
```yaml
---
title: "Deploying Kubernetes on AWS"
date: "2024-01-15"
description: "A guide to deploying Kubernetes clusters on AWS EKS"
---

![Architecture](./images/k8s-arch.png)

Content here...
```
- images/k8s-arch.png (copied from source)
- Topic: `blog-post`
- Description: "A guide to deploying Kubernetes clusters on AWS EKS"

---

## Ready to Proceed?

Once you confirm the prerequisites and answer the questions above, the migration can begin. The process will be logged and you'll receive a summary report upon completion.
