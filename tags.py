import os
import yaml
from collections import defaultdict
from datetime import datetime
import re

def extract_frontmatter(file_content):
    """
    Extracts the YAML frontmatter from the given file content.
    If the frontmatter is missing, returns an empty string.
    """
    frontmatter = ""
    content_lines = file_content.split('\n')
    if content_lines[0].strip() == '---':
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n'.join(content_lines[1:i])
                break
    return frontmatter

def process_tags(posts_dir, output_file):
    """
    Processes markdown files in the specified posts directory to extract tags and generate a YAML file
    mapping tags to posts. The posts are sorted by date within each tag.
    """
    tag_data = defaultdict(list)
    
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            frontmatter = extract_frontmatter(file_content)
            if not frontmatter:
                print(f"Warning: No frontmatter found in {filename}. Skipping file.")
                continue
            
            try:
                post_data = yaml.safe_load(frontmatter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in {filename}: {e}. Skipping file.")
                continue
            
            tags = post_data.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]
            elif not isinstance(tags, list):
                tags = [str(tags)]
            
            title = post_data.get('title', os.path.splitext(filename)[0])
            
            # Prioritize slug from front matter
            slug = post_data.get('permalink') or post_data.get('slug')
            
            # Fallback to extracting slug from filename if not in front matter
            if not slug:
                slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename.replace('.md', ''))

            # Construct the URL based on the slug
            url = f'/{slug}'
            
            # Extract post date for sorting
            try:
                post_date = datetime.strptime('-'.join(filename.split('-')[:3]), '%Y-%m-%d')
            except ValueError:
                print(f"Warning: Unable to parse date from filename {filename}. Using default date.")
                post_date = datetime.min
            
            for tag in tags:
                tag_parts = tag.split('>') if isinstance(tag, str) else [str(tag)]
                
                for i in range(len(tag_parts)):
                    partial_tag = '>'.join(tag_parts[:i+1])
                    tag_data[partial_tag].append({
                        'title': title,
                        'url': url,
                        'date': post_date
                    })

    # Sort posts within each tag by date, most recent first
    for tag, posts in tag_data.items():
        tag_data[tag] = sorted(posts, key=lambda x: x['date'], reverse=True)
        # Remove date from final output
        for post in tag_data[tag]:
            del post['date']

    # Write the processed tags to a YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': posts} for tag, posts in tag_data.items()], f, allow_unicode=True)

if __name__ == '__main__':
    process_tags('_posts', '_data/processed_tags.yml')
