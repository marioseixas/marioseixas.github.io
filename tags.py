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
    """Processes tags from markdown files to establish hierarchical and non-hierarchical relationships."""
    tag_data = defaultdict(lambda: {'parents': set(), 'children': set(), 'posts': []})
    post_tags = defaultdict(set)

    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            with open(os.path.join(posts_dir, filename), 'r', encoding='utf-8') as f:
                frontmatter = extract_frontmatter(f.read())

            if not frontmatter:
                continue

            post_data = yaml.safe_load(frontmatter)
            tags = post_data.get('tags', [])
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]

            url = '/' + '-'.join(filename.split('-')[3:]).replace('.md', '')

            for tag in tags:
                parts = tag.split('>')
                full_tag = tag

                # Add the full tag to post_tags
                post_tags[url].add(full_tag)

                # Process hierarchical relationships
                for i in range(1, len(parts) + 1):
                    current = '>'.join(parts[:i])
                    tag_data[current]['posts'].append({'url': url, 'title': post_data.get('title', '')})

                    if i > 1:
                        parent = '>'.join(parts[:i - 1])
                        tag_data[current]['parents'].add(parent)
                        tag_data[parent]['children'].add(current)

    # Count tag frequencies (For THRESHOLD functionality)
    for post_url, tags in post_tags.items():
        for tag in tags:
            tag_frequency[tag] += 1

    return tag_data, post_tags


def generate_mermaid_graph(tag_data, post_tags):
    """Generates Mermaid graph code for visualizing tag relationships."""
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
    mermaid_output_file = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_includes/tag_graph.html')

    tag_data, post_tags = process_tags(posts_dir)
    mermaid_graph = generate_mermaid_graph(tag_data, post_tags)

    # Write the Mermaid graph to a file
    with open(mermaid_output_file, 'w', encoding='utf-8') as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info(f"Mermaid graph has been written to {mermaid_output_file}")

    # Write the processed tags to a YAML file
    sorted_tag_data = sorted(tag_data.items())
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': posts['posts']} for tag, posts in sorted_tag_data], f, allow_unicode=True)

    logging.info(f"Processed tags have been written to {output_file}")
