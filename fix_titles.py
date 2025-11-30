#!/usr/bin/env python3
"""
Fix missing titles in repository frontmatter
"""

import subprocess
import base64
import yaml
import re

REPOS_TO_FIX = [
    {
        'name': '2024-12-1-ArgoCD-Multi-Source-Deployments-for-Google-Config-Connector',
        'title': 'ArgoCD Multi-Source Deployments for Google Config Connector'
    },
    {
        'name': '2024-12-7-Lokalise-Translations-With-Github-Actions',
        'title': 'Lokalise Translations With Github Actions'
    }
]

def get_readme_content(repo_name):
    """Fetch README content from GitHub"""
    result = subprocess.run(
        ['gh', 'api', f'repos/Matcham89/{repo_name}/readme', '--jq', '.content'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    content = base64.b64decode(result.stdout.strip()).decode('utf-8')
    return content

def parse_frontmatter(content):
    """Extract YAML frontmatter and body"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].strip()
    return frontmatter, body

def update_readme(repo_name, new_content):
    """Update README.md in repository"""
    # Clone repo to temp location
    temp_dir = f'/tmp/fix-title-{repo_name}'
    subprocess.run(['rm', '-rf', temp_dir], capture_output=True)

    # Clone
    result = subprocess.run(
        ['gh', 'repo', 'clone', f'Matcham89/{repo_name}', temp_dir],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Failed to clone {repo_name}")
        return False

    # Write new README
    readme_path = f'{temp_dir}/README.md'
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Commit and push
    subprocess.run(['git', 'add', 'README.md'], cwd=temp_dir)
    subprocess.run(
        ['git', 'commit', '-m', 'Add missing title to frontmatter'],
        cwd=temp_dir
    )
    result = subprocess.run(['git', 'push'], cwd=temp_dir, capture_output=True)

    # Cleanup
    subprocess.run(['rm', '-rf', temp_dir], capture_output=True)

    return result.returncode == 0

def main():
    print("Fixing missing titles in frontmatter...\n")

    for repo_info in REPOS_TO_FIX:
        repo_name = repo_info['name']
        title = repo_info['title']

        print(f"{'='*80}")
        print(f"Processing: {repo_name}")
        print(f"Adding title: {title}")

        # Get current content
        content = get_readme_content(repo_name)
        if not content:
            print("❌ Could not fetch README")
            continue

        # Parse frontmatter
        frontmatter, body = parse_frontmatter(content)

        # Add title
        frontmatter['title'] = title

        # Rebuild content
        new_content = "---\n"
        new_content += yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        new_content += "---\n\n"
        new_content += body

        # Update repository
        if update_readme(repo_name, new_content):
            print(f"✅ Successfully updated {repo_name}")
        else:
            print(f"❌ Failed to update {repo_name}")

    print("\n" + "="*80)
    print("Done!")

if __name__ == '__main__':
    main()
