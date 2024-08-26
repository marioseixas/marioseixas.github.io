import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Threshold for generating permutations
THRESHOLD = 0  # Adjust this value as needed

# Dictionary to store tag frequencies
tag_frequency = defaultdict(int)

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

def process_tags(posts_dir):
    """Processes tags from markdown files, handling nested tags, highlighting exact matches,
    preventing duplicates using file paths, and generating a Mermaid graph."""
    
    tag_data = defaultdict(lambda: {'parents': set(), 'children': set(), 'posts': []})
    post_tags = defaultdict(set)

    logging.info(f"Processing markdown files in directory: {posts_dir}")

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(posts_dir, filename)

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

            # Count tag frequencies
            for tag in tags:
                tag_frequency[tag] += 1

            title = post_data.get('title', os.path.splitext(filename)[0])
            url = '/' + '-'.join(filename.split('-')[3:]).replace('.md', '')

            try:
                post_date = datetime.strptime('-'.join(filename.split('-')[:3]), '%Y-%m-%d')
            except ValueError:
                logging.warning(f"Unable to parse date from filename {filename}")
                post_date = datetime.min

            for tag in tags:
                parts = tag.split('>')
                full_tag = tag

                # Add the full tag to post_tags
                post_tags[url].add(full_tag)
                
                # Process hierarchical relationships with threshold check
                for i in range(1, len(parts) + 1):
                    current = '>'.join(parts[:i])
                    if all(tag_frequency[part] >= THRESHOLD for part in parts[:i]):
                        tag_data[current]['posts'].append({'url': url, 'title': title})

                        if i > 1:
                            parent = '>'.join(parts[:i-1])
                            tag_data[current]['parents'].add(parent)
                            tag_data[parent]['children'].add(current)

    return tag_data, post_tags

def generate_mermaid_graph(tag_data, post_tags):
    """Generates Mermaid graph code for the tag structure."""
    graph = "graph TD\n"
    
    # Add nodes and hierarchical relationships
    for tag, data in tag_data.items():
        safe_tag = tag.replace('>', '_')
        graph += f"{safe_tag}({tag})\n"
        for parent in data['parents']:
            safe_parent = parent.replace('>', '_')
            graph += f"{safe_parent} --> {safe_tag}\n"
    
    # Add non-hierarchical relationships (posts sharing tags)
    processed_pairs = set()
    for post, tags in post_tags.items():
        for tag1 in tags:
            for tag2 in tags:
                if tag1 != tag2 and (tag1, tag2) not in processed_pairs and (tag2, tag1) not in processed_pairs:
                    safe_tag1 = tag1.replace('>', '_')
                    safe_tag2 = tag2.replace('>', '_')
                    graph += f"{safe_tag1} -.-> {safe_tag2}\n"
                    processed_pairs.add((tag1, tag2))

    return graph

if __name__ == '__main__':
    # Use environment variables to determine paths
    posts_dir = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_posts')
    output_file = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_data/processed_tags.yml')
    
    tag_data, post_tags = process_tags(posts_dir)
    mermaid_graph = generate_mermaid_graph(tag_data, post_tags)

    # Write the Mermaid graph to a file
    with open(os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_includes/tag_graph.html'), 'w', encoding='utf-8') as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
