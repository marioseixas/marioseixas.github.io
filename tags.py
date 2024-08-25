import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_frontmatter(file_content):
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split('\n')
    if content_lines[0].strip() == '---':
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n'.join(content_lines[1:i])
                break
    return frontmatter

def process_tags(posts_dir, output_file):
    """Processes tags from markdown files, handling nested tags, highlighting exact matches, and preventing duplicates using file paths.

    Args:
        posts_dir (str): Directory containing markdown files.
        output_file (str): Path to the output YAML file.
    """
    tag_data = defaultdict(list)
    seen_posts = set() # Set to store unique post file paths

    logging.info(f"Processing markdown files in directory: {posts_dir}")

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)

            # Duplicate prevention: Skip if this file has already been processed
            if file_path in seen_posts: 
                logging.warning(f"Skipping duplicate post: {filename}")
                continue
            seen_posts.add(file_path)

            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            frontmatter = extract_frontmatter(file_content)
            if not frontmatter:
                logging.warning(f"No frontmatter found in {filename}")
                continue

            try:
                post_data = yaml.safe_load(frontmatter)
            except yaml.YAMLError as e:
                logging.error(f"Error parsing frontmatter in {filename}: {e}")
                continue

            tags = post_data.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]
            elif not isinstance(tags, list):
                tags = [str(tags)]

            title = post_data.get('title', os.path.splitext(filename)[0])
            url = '/' + '-'.join(filename.split('-')[3:]).replace('.md', '')

            try:
                post_date = datetime.strptime('-'.join(filename.split('-')[:3]), '%Y-%m-%d')
            except ValueError:
                logging.warning(f"Unable to parse date from filename {filename}")
                post_date = datetime.min

            for tag in tags:
                tag_parts = [part.strip() for part in tag.split('>')]

                for i in range(len(tag_parts)):
                    partial_tag = '>'.join(tag_parts[:i+1])
                    post_entry = {
                        'title': title,
                        'url': url,
                        'highlighted': partial_tag == tag  # Highlight if exact match
                    }
                    tag_data[partial_tag].append(post_entry) # No duplicate check needed here now

    # Sort posts within each tag by date (most recent first)
    for tag, posts in tag_data.items():
        tag_data[tag] = sorted(posts, key=lambda x: x.get('date', datetime.min), reverse=True)

    # Sort tags alphabetically
    sorted_tag_data = sorted(tag_data.items())

    # Write the processed tags to a YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': posts} for tag, posts in sorted_tag_data], f, allow_unicode=True)

    logging.info(f"Processed tags have been written to {output_file}")

if __name__ == '__main__':
    process_tags('_posts', '_data/processed_tags.yml')
