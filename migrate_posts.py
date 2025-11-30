#!/usr/bin/env python3
"""
Jekyll to Hub & Spoke Blog Migration Script
Migrates Jekyll blog posts to individual GitHub repositories
"""

import os
import re
import yaml
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class MigrationLogger:
    def __init__(self, log_file="migration-log.md"):
        self.log_file = log_file
        self.entries = []
        self.start_time = datetime.now()

    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        self.entries.append(entry)
        print(entry)

    def save(self):
        with open(self.log_file, 'w') as f:
            f.write(f"# Jekyll to Hub & Spoke Migration Log\n\n")
            f.write(f"**Started:** {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Migration Log\n\n")
            for entry in self.entries:
                f.write(f"{entry}\n")

class PostMigrator:
    def __init__(self, source_repo_path, logger, dry_run=False):
        self.source_repo = Path(source_repo_path)
        self.posts_dir = self.source_repo / "_posts"
        self.images_dir = self.source_repo / "assets" / "images"
        self.logger = logger
        self.dry_run = dry_run
        self.temp_dir = Path("/tmp/blog-migration")

    def parse_frontmatter(self, content):
        """Extract YAML frontmatter from markdown content"""
        if not content.startswith('---'):
            return {}, content

        try:
            # Find the end of frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content

            frontmatter_raw = parts[1].strip()
            body = parts[2].strip()

            # Parse YAML
            frontmatter = yaml.safe_load(frontmatter_raw) or {}
            return frontmatter, body
        except Exception as e:
            self.logger.log(f"Error parsing frontmatter: {e}", "ERROR")
            return {}, content

    def sanitize_repo_name(self, name):
        """Sanitize repository name to match GitHub's requirements"""
        # GitHub converts colons to dashes, let's do it proactively
        name = name.replace(':', '-')
        # Remove any other invalid characters
        name = re.sub(r'[^a-zA-Z0-9\-_.]', '-', name)
        # Remove consecutive dashes
        name = re.sub(r'-+', '-', name)
        # Remove leading/trailing dashes
        name = name.strip('-')
        return name

    def extract_repo_name(self, filename):
        """Extract repository name from Jekyll post filename"""
        # Format: YYYY-MM-DD-post-slug.md
        match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
        if match:
            slug = match.group(1)
            return self.sanitize_repo_name(slug)
        return self.sanitize_repo_name(filename.replace('.md', ''))

    def extract_date(self, filename, frontmatter):
        """Extract date from filename or frontmatter"""
        # Try frontmatter first
        if 'date' in frontmatter:
            date = frontmatter['date']
            if isinstance(date, str):
                return date.split()[0]  # Take just the date part
            return date.strftime('%Y-%m-%d')

        # Fall back to filename
        match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            return match.group(1)

        return datetime.now().strftime('%Y-%m-%d')

    def extract_title_from_slug(self, slug):
        """Convert slug to title format"""
        # Replace dashes with spaces and capitalize each word
        title = slug.replace('-', ' ').title()
        return title

    def transform_frontmatter(self, frontmatter, filename):
        """Transform Jekyll frontmatter to new format (only title, no date)"""
        new_frontmatter = {}

        # Title (required) - use frontmatter title or extract from filename
        if 'title' in frontmatter:
            new_frontmatter['title'] = frontmatter['title']
        else:
            # Extract from filename: YYYY-MM-DD-post-slug.md -> Post Slug
            match = re.match(r'\d{4}-\d{2}-\d{2}-(.+)\.md', filename)
            if match:
                slug = match.group(1)
                new_frontmatter['title'] = self.extract_title_from_slug(slug)

        return new_frontmatter

    def find_images_in_content(self, content):
        """Find all image references in markdown content"""
        # Match markdown images: ![alt](path)
        pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        return [(alt, path) for alt, path in matches]

    def process_images(self, content, repo_path):
        """Copy referenced images and update paths"""
        images = self.find_images_in_content(content)
        updated_content = content

        if not images:
            return updated_content

        # Create images directory in new repo
        images_dest = repo_path / "images"
        if not self.dry_run:
            images_dest.mkdir(exist_ok=True)

        for alt, img_path in images:
            # Check if image exists in source repo
            # Handle both absolute and relative paths
            possible_paths = [
                self.images_dir / Path(img_path).name,
                self.source_repo / img_path.lstrip('/'),
                self.source_repo / "assets" / img_path.lstrip('/'),
            ]

            source_image = None
            for possible_path in possible_paths:
                if possible_path.exists():
                    source_image = possible_path
                    break

            if source_image:
                # Copy image
                dest_image = images_dest / source_image.name
                if not self.dry_run:
                    shutil.copy2(source_image, dest_image)
                self.logger.log(f"Copied image: {source_image.name}")

                # Update path in content
                new_path = f"./images/{source_image.name}"
                updated_content = updated_content.replace(f"]({img_path})", f"]({new_path})")
            else:
                self.logger.log(f"Image not found: {img_path}", "WARNING")

        return updated_content

    def clean_content(self, content):
        """Remove Jekyll-specific syntax"""
        # Remove liquid tags
        content = re.sub(r'\{%.*?%\}', '', content)

        # Remove liquid includes
        content = re.sub(r'\{%\s*include.*?%\}', '', content)

        # Clean up extra blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip()

    def repo_exists(self, repo_name):
        """Check if repository already exists"""
        try:
            result = subprocess.run(
                ['gh', 'repo', 'view', f'Matcham89/{repo_name}'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def create_repository(self, repo_name, description):
        """Create a new GitHub repository"""
        if self.dry_run:
            self.logger.log(f"[DRY RUN] Would create repo: {repo_name}")
            return True

        try:
            # Create repository
            cmd = [
                'gh', 'repo', 'create', f'Matcham89/{repo_name}',
                '--public',
                '--description', description[:350] if description else f'Blog post: {repo_name}',
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                self.logger.log(f"Failed to create repo {repo_name}: {result.stderr}", "ERROR")
                return False

            self.logger.log(f"Created repository: {repo_name}")

            # Add blog-post topic
            topic_cmd = [
                'gh', 'repo', 'edit', f'Matcham89/{repo_name}',
                '--add-topic', 'blog-post'
            ]
            subprocess.run(topic_cmd, capture_output=True)

            return True

        except Exception as e:
            self.logger.log(f"Exception creating repo {repo_name}: {e}", "ERROR")
            return False

    def migrate_post(self, post_file):
        """Migrate a single blog post"""
        self.logger.log(f"\n{'='*60}")
        self.logger.log(f"Processing: {post_file.name}")

        # Read post content
        with open(post_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse frontmatter
        frontmatter, body = self.parse_frontmatter(content)

        # Extract metadata
        repo_name = self.extract_repo_name(post_file.name)
        date = self.extract_date(post_file.name, frontmatter)

        # Check if repo exists
        if self.repo_exists(repo_name):
            self.logger.log(f"Repository already exists: {repo_name}", "WARNING")
            return {
                'status': 'conflict',
                'filename': post_file.name,
                'repo_name': repo_name,
                'reason': 'Repository already exists'
            }

        # Transform frontmatter (only title, no date)
        new_frontmatter = self.transform_frontmatter(frontmatter, post_file.name)

        # Clean content
        cleaned_body = self.clean_content(body)

        # Create temp directory for this repo
        repo_path = self.temp_dir / repo_name
        if not self.dry_run:
            repo_path.mkdir(parents=True, exist_ok=True)

        # Process images
        processed_body = self.process_images(cleaned_body, repo_path)

        # Build README content (only title in frontmatter, then content)
        readme_content = "---\n"
        readme_content += yaml.dump(new_frontmatter, default_flow_style=False, allow_unicode=True)
        readme_content += "---\n\n"
        readme_content += processed_body

        # Create repository - use title as description
        description = new_frontmatter.get('title', f'Blog post: {repo_name}')
        if not self.create_repository(repo_name, description):
            return {
                'status': 'failed',
                'filename': post_file.name,
                'repo_name': repo_name,
                'reason': 'Failed to create repository'
            }

        # Clone and populate repository
        if not self.dry_run:
            try:
                # Clone the repository
                clone_cmd = ['gh', 'repo', 'clone', f'Matcham89/{repo_name}', str(repo_path)]
                subprocess.run(clone_cmd, capture_output=True, cwd=self.temp_dir)

                # Write README
                with open(repo_path / 'README.md', 'w', encoding='utf-8') as f:
                    f.write(readme_content)

                # Create .gitignore
                with open(repo_path / '.gitignore', 'w') as f:
                    f.write("# Editor files\n.DS_Store\n*.swp\n*.swo\n*~\n\n# IDE\n.vscode/\n.idea/\n")

                # Git operations
                subprocess.run(['git', 'add', '.'], cwd=repo_path)
                subprocess.run(
                    ['git', 'commit', '-m', 'Migrate blog post from Jekyll site'],
                    cwd=repo_path
                )
                subprocess.run(['git', 'push', 'origin', 'main'], cwd=repo_path)

                self.logger.log(f"Successfully migrated: {repo_name}")

            except Exception as e:
                self.logger.log(f"Error during git operations for {repo_name}: {e}", "ERROR")
                return {
                    'status': 'failed',
                    'filename': post_file.name,
                    'repo_name': repo_name,
                    'reason': str(e)
                }

        return {
            'status': 'success',
            'filename': post_file.name,
            'repo_name': repo_name,
            'title': new_frontmatter.get('title', ''),
            'date': date
        }

    def get_all_posts(self):
        """Get all markdown files from _posts directory"""
        return sorted(self.posts_dir.glob('*.md'))

    def migrate_all(self, limit=None):
        """Migrate all posts or a limited number"""
        posts = self.get_all_posts()

        if limit:
            posts = posts[:limit]

        self.logger.log(f"Found {len(posts)} posts to migrate")

        # Create temp directory
        if not self.dry_run:
            self.temp_dir.mkdir(exist_ok=True)

        results = {
            'success': [],
            'failed': [],
            'conflicts': []
        }

        for post in posts:
            result = self.migrate_post(post)

            if result['status'] == 'success':
                results['success'].append(result)
            elif result['status'] == 'conflict':
                results['conflicts'].append(result)
            else:
                results['failed'].append(result)

        return results

def main():
    import sys

    # Configuration
    SOURCE_REPO = "/tmp/matcham89.github.io"
    LIMIT = 2 if '--test' in sys.argv else None
    DRY_RUN = '--dry-run' in sys.argv

    # Initialize logger
    logger = MigrationLogger()
    logger.log("Starting Jekyll to Hub & Spoke migration")

    if DRY_RUN:
        logger.log("DRY RUN MODE - No changes will be made", "INFO")

    if LIMIT:
        logger.log(f"TEST MODE - Migrating first {LIMIT} posts only", "INFO")

    # Initialize migrator
    migrator = PostMigrator(SOURCE_REPO, logger, dry_run=DRY_RUN)

    # Run migration
    results = migrator.migrate_all(limit=LIMIT)

    # Print summary
    logger.log("\n" + "="*60)
    logger.log("MIGRATION SUMMARY")
    logger.log("="*60)
    logger.log(f"✅ Successful: {len(results['success'])}")
    logger.log(f"❌ Failed: {len(results['failed'])}")
    logger.log(f"⚠️  Conflicts: {len(results['conflicts'])}")

    if results['success']:
        logger.log("\nSuccessfully migrated:")
        for r in results['success']:
            logger.log(f"  - {r['repo_name']} ({r['filename']})")

    if results['failed']:
        logger.log("\nFailed migrations:")
        for r in results['failed']:
            logger.log(f"  - {r['repo_name']}: {r['reason']}")

    if results['conflicts']:
        logger.log("\nConflicts (repos already exist):")
        for r in results['conflicts']:
            logger.log(f"  - {r['repo_name']}")

    # Save log
    logger.save()
    logger.log(f"\nLog saved to: migration-log.md")

if __name__ == "__main__":
    main()
