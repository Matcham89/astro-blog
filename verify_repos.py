#!/usr/bin/env python3
"""
Verify and update migrated blog repositories
- Check titles in frontmatter
- Generate descriptions from content
- Update GitHub repo descriptions
"""

import subprocess
import json
import re
import yaml

def get_blog_repos():
    """Get all repositories with blog-post topic"""
    result = subprocess.run(
        ['gh', 'repo', 'list', 'Matcham89', '--topic', 'blog-post', '--json', 'name,url,description', '--limit', '50'],
        capture_output=True,
        text=True
    )
    repos = json.loads(result.stdout)
    # Filter out test repo
    return [r for r in repos if r['name'] != 'blog-test']

def get_readme_content(repo_name):
    """Fetch README content from GitHub"""
    result = subprocess.run(
        ['gh', 'api', f'repos/Matcham89/{repo_name}/readme', '--jq', '.content'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    # Content is base64 encoded
    import base64
    content = base64.b64decode(result.stdout.strip()).decode('utf-8')
    return content

def parse_frontmatter(content):
    """Extract YAML frontmatter and body from markdown"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return frontmatter, body

def generate_description(body, max_length=300):
    """Generate a description from the blog content"""
    # Remove HTML tags
    body = re.sub(r'<[^>]+>', '', body)

    # Remove markdown images
    body = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', body)

    # Remove markdown links but keep text
    body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body)

    # Remove markdown headers
    body = re.sub(r'#+\s+', '', body)

    # Remove extra whitespace
    body = re.sub(r'\s+', ' ', body).strip()

    # Get first few sentences
    sentences = re.split(r'[.!?]\s+', body)
    description = ''
    for sentence in sentences:
        if len(description) + len(sentence) + 1 < max_length:
            description += sentence + '. '
        else:
            break

    return description.strip()

def update_repo_description(repo_name, description):
    """Update GitHub repository description"""
    result = subprocess.run(
        ['gh', 'repo', 'edit', f'Matcham89/{repo_name}', '--description', description],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def main():
    print("Fetching all blog-post repositories...")
    repos = get_blog_repos()
    print(f"Found {len(repos)} repositories to verify\n")

    results = []

    for repo in sorted(repos, key=lambda x: x['name']):
        print(f"\n{'='*80}")
        print(f"Processing: {repo['name']}")
        print(f"URL: {repo['url']}")
        print(f"Current Description: {repo['description']}")

        # Get README content
        content = get_readme_content(repo['name'])
        if not content:
            print("❌ Could not fetch README")
            results.append({
                'name': repo['name'],
                'status': 'failed',
                'reason': 'Could not fetch README'
            })
            continue

        # Parse frontmatter
        frontmatter, body = parse_frontmatter(content)

        # Check title
        title = frontmatter.get('title', 'NO TITLE')
        print(f"Title in frontmatter: {title}")

        # Generate description
        new_description = generate_description(body)
        print(f"\nGenerated description:")
        print(f"  {new_description}")

        # Update if needed
        if new_description and new_description != repo['description']:
            print(f"\n📝 Updating repository description...")
            if update_repo_description(repo['name'], new_description):
                print("✅ Description updated successfully")
                results.append({
                    'name': repo['name'],
                    'status': 'updated',
                    'title': title,
                    'old_description': repo['description'],
                    'new_description': new_description
                })
            else:
                print("❌ Failed to update description")
                results.append({
                    'name': repo['name'],
                    'status': 'failed',
                    'reason': 'Failed to update description'
                })
        else:
            print("✅ Description already good")
            results.append({
                'name': repo['name'],
                'status': 'unchanged',
                'title': title,
                'description': repo['description']
            })

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total repositories: {len(repos)}")
    print(f"Updated: {len([r for r in results if r['status'] == 'updated'])}")
    print(f"Unchanged: {len([r for r in results if r['status'] == 'unchanged'])}")
    print(f"Failed: {len([r for r in results if r['status'] == 'failed'])}")

    # Save results
    with open('repo_verification_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: repo_verification_results.json")

if __name__ == '__main__':
    main()
