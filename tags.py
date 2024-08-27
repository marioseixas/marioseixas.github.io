import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Threshold for generating permutations
THRESHOLD = 0  # Set this value according to your needs

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
    """Generates all possible partial tags for a given hierarchical tag."""
    parts = tag.split('>')
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append('>'.join(parts[j:j+i]))
    return partial_tags

def process_tags(posts_dir, output_file):
    """Processes tags from markdown files, managing nested tags, and generating a Mermaid graph."""
    
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
    tag_data = defaultdict(lambda: {'parents': set(), 'children': set(), 'related': set(), 'posts': []})

    for post in all_posts:
        for tag in post['tags']:
            tag_parts = tag.split('>')
            full_tag_path = tag

            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        'title': post['title'],
                        'url': post['url'],
                        'highlighted': partial_tag == tag,
                        'date': post['date']
                    }
                    tag_data[partial_tag]['posts'].append(post_entry)

            # Establish parent-child relationships
            for i in range(1, len(tag_parts)):
                parent_tag = '>'.join(tag_parts[:i])
                child_tag = '>'.join(tag_parts[:i + 1])
                if tag_frequency[parent_tag] >= THRESHOLD and tag_frequency[child_tag] >= THRESHOLD:
                    tag_data[child_tag]['parents'].add(parent_tag)
                    tag_data[parent_tag]['children'].add(child_tag)

            # Track non-hierarchical (related) relationships
            for other_tag in post['tags']:
                if other_tag != tag and tag_frequency[other_tag] >= THRESHOLD and tag_frequency[full_tag_path] >= THRESHOLD:
                    tag_data[full_tag_path]['related'].add(other_tag)
                    tag_data[other_tag]['related'].add(full_tag_path)

    # Remove tags with no posts
    tag_data = {tag: data for tag, data in tag_data.items() if data['posts']}

    # Clean up relationships
    for tag, data in tag_data.items():
        data['parents'] = {parent for parent in data['parents'] if parent in tag_data}
        data['children'] = {child for child in data['children'] if child in tag_data}
        data['related'] = {related for related in data['related'] if related in tag_data}

    # Sort posts within each tag by date (most recent first)
    for tag, data in tag_data.items():
        data['posts'] = sorted(data['posts'], key=lambda x: x.get('date', datetime.min), reverse=True)

    # Sort tags alphabetically before writing to YAML
    sorted_tag_data = sorted(tag_data.items())

    # Write the processed tags to a YAML file
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump([{'tag': tag, 'posts': data['posts']} for tag, data in sorted_tag_data], f, allow_unicode=True)

    logging.info(f"Processed tags have been written to {output_file}")

    return tag_data

def generate_mermaid_graph(tag_data: Dict[str, Any], direction: str = "TD") -> str:
    """
    Generates Mermaid graph code for the tag structure.

    Args:
        tag_data (Dict[str, Any]): Dictionary containing tag relationships.
        direction (str): Graph direction (TD, LR, RL, BT). Defaults to "TD".

    Returns:
        str: Mermaid graph code.
    """
    graph = [f"graph {direction}"]
    added_nodes = set()
    added_edges = set()

    def add_node(tag: str) -> str:
        safe_tag = tag.replace('>', '_').replace(' ', '_')
        if safe_tag not in added_nodes:
            node_def = f'    "{safe_tag}"["{tag}"]'
            graph.append(node_def)
            added_nodes.add(safe_tag)
        return safe_tag

    def add_edge(from_tag: str, to_tag: str, edge_type: str = 'solid') -> None:
        safe_from = add_node(from_tag)
        safe_to = add_node(to_tag)
        edge = (safe_from, safe_to, edge_type)
        if edge not in added_edges:
            edge_style = '-->' if edge_type == 'solid' else '-..->'
            graph.append(f'    "{safe_from}"" {edge_style}"" {safe_to}"')
            added_edges.add(edge)

    try:
        for tag_name, data in tag_data.items():
            # Add hierarchical relationships
            for child in data.get('children', []):
                add_edge(tag_name, child, 'solid')

            # Add non-hierarchical relationships
            for related in data.get('related', []):
                add_edge(tag_name, related, 'dashed')

            # Handle compound tags
            if '>' in tag_name:
                parts = tag_name.split('>')
                for i in range(len(parts) - 1):
                    parent = '>'.join(parts[:i+1])
                    child = '>'.join(parts[:i+2])
                    add_edge(parent, child, 'solid')
                    add_edge(tag_name, parts[i], 'dashed')

    except AttributeError as e:
        logging.error(f"Invalid tag_data structure: {e}")
        return ""

    return '\n'.join(graph)

if __name__ == '__main__':
    # Use environment variables to determine paths
    posts_dir = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_posts')
    output_file = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_data/processed_tags.yml')
    
    try:
        with open(output_file, 'r') as f:
            tag_data = yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        logging.error(f"Error reading tag data: {e}")
        tag_data = {}

    mermaid_graph = generate_mermaid_graph(tag_data)

    # Write the Mermaid graph to a file
    output_path = os.path.join(os.getenv('GITHUB_WORKSPACE', ''), '_includes/tag_graph.html')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")
        logging.info(f"Mermaid graph has been written to {output_path}")
    except IOError as e:
        logging.error(f"Error writing Mermaid graph: {e}")
