import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Threshold for generating permutations
THRESHOLD = 2  # Adjust this value as needed

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

def generate_partial_tags(tag):
    """Generates all partial tags for a given tag."""
    parts = tag.split('>')
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append('>'.join(parts[j:j+i]))
    return partial_tags

def process_tags(posts_dir, output_file):
    """Processes tags from markdown files, handling nested tags, highlighting exact matches, and preventing duplicates."""

    tag_frequency = defaultdict(int)
    all_posts = []
    seen_posts = set()

    logging.info(f"Processing markdown files in directory: {posts_dir}")

    # First pass: Count tag frequencies and collect all posts
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue

        file_path = os.path.join(posts_dir, filename)
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

        # Count tag frequencies including partial tags
        for tag in tags:
            for partial_tag in generate_partial_tags(tag):
                tag_frequency[partial_tag] += 1

        title = post_data.get('title', os.path.splitext(filename)[0])
        url = '/' + '-'.join(filename.split('-')[3:]).replace('.md', '')

        try:
            post_date = datetime.strptime('-'.join(filename.split('-')[:3]), '%Y-%m-%d')
        except ValueError:
            logging.warning(f"Unable to parse date from filename {filename}")
            post_date = datetime.min

        all_posts.append({
            'title': title,
            'url': url,
            'date': post_date,
            'tags': tags
        })

    # Second pass: Generate tag data based on frequency threshold
    tag_data = defaultdict(list)
    for post in all_posts:
        for tag in post['tags']:
            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        'title': post['title'],
                        'url': post['url'],
                        'highlighted': partial_tag == tag,
                        'date': post['date']
                    }
                    tag_data[partial_tag].append(post_entry)

    # Sort posts within each tag by date (most recent first)
    for tag, posts in tag_data.items():
        tag_data[tag] = sorted(posts, key=lambda x: x['date'], reverse=True)

    # Sort tags alphabetically
    sorted_tag_data = sorted(tag_data.items())

    # Write the processed tags to a YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': posts} for tag, posts in sorted_tag_data], f, allow_unicode=True)

    logging.info(f"Processed tags have been written to {output_file}")

if __name__ == '__main__':
    process_tags('_posts', '_data/processed_tags.yml')
