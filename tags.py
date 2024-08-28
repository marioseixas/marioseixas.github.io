import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Union, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Threshold for generating permutations
THRESHOLD = 0  # Set this value according to your needs

def extract_frontmatter(file_content: str) -> str:
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split('\n')
    if content_lines[0].strip() == '---':
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == '---':
                frontmatter = '\n.join(content_lines[1:i])
                break
    return frontmatter

def generate_partial_tags(tag: str) -> List[str]:
    """Generates all possible partial tags for a given hierarchical tag."""
    parts = tag.split('>')
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append('>'.join(parts[j:j+i]))
    return partial_tags

def process_tags(posts_dir: str, output_file: str) -> Dict[str, Dict[str, Any]]:
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
                parent_tag = '>.join(tag_parts[:i])
                child_tag = '>.join(tag_parts[:i + 1])
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

def generate_mermaid_graph(tag_data: Union[List[Dict[str, Any]], Dict[str, Any]], direction: str = "TD") -> str:
    """
    Generates Mermaid graph code for the tag structure.

    Args:
        tag_data (Union[List[Dict[str, Any]], Dict[str, Any]]): List of dictionaries or dictionary containing tag relationships.
        direction (str): Graph direction (TD, LR, RL, BT). Defaults to "TD".

    Returns:
        str: Mermaid graph code.
    """
    graph = [f"graph {direction}"]
    added_nodes = set()
    added_edges = set()

    def add_node(tag: str, style: str) -> str:
        """
        Adds a node to the graph if it hasn't been added yet.

        Args:
            tag (str): The tag name to be added.
            style (str): The style class for the node.

        Returns:
            str: The sanitized tag name used in the graph.
        """
        safe_tag = tag.replace('>', '_').replace(' ', '_')  # Sanitize tag name (basic)
        if safe_tag not in added_nodes:
            node_def = f'    {safe_tag}["{tag}"]'
            if style:
                node_def += f':::{style}'
            graph.append(node_def)
            added_nodes.add(safe_tag)
        return safe_tag

    def add_edge(from_tag: str, to_tag: str, edge_type: str = 'solid') -> None:
        """
        Adds an edge between two nodes in the graph.

        Args:
            from_tag (str): The starting node of the edge.
            to_tag (str): The ending node of the edge.
            edge_type (str): The type of edge ('solid' or 'dashed'). Defaults to 'solid'.
        """
        safe_from = add_node(from_tag, 'mainNode' if '>' not in from_tag else 'combinedNode')
        safe_to = add_node(to_tag, 'mainNode' if '>' not in to_tag else 'combinedNode')
        edge = (safe_from, safe_to, edge_type)
        if edge not in added_edges:
            edge_style = '-->' if edge_type == 'solid' else '-.->|related|'
            graph.append(f'    {safe_from} {edge_style} {safe_to}')
            added_edges.add(edge)

    def process_tag(tag_name: str, data: Dict[str, Any]) -> None:
        """
        Processes a single tag and its relationships.

        Args:
            tag_name (str): The name of the tag.
            data (Dict[str, Any]): The data associated with the tag, including children and related tags.
        """
        # Add hierarchical relationships
        for child in data.get('children', []):
            add_edge(tag_name, child, 'solid')

        # Add non-hierarchical relationships
        for related in data.get('related', []):
            add_edge(tag_name, related, 'dashed')

        # Handle compound tags (optimized)
        if '>' in tag_name:
            parts = tag_name.split('>')
            for i in range(len(parts) - 1):
                parent = '>'.join(parts[:i + 1])
                child = '>'.join(parts[:i + 2])
                add_edge(parent, child, 'solid')

    try:
        if isinstance(tag_data, dict):
            for tag_name, data in tag_data.items():
                process_tag(tag_name, data)
        elif isinstance(tag_data, list):
            for tag_dict in tag_data:
                for tag_name, data in tag_dict.items():
                    process_tag(tag_name, data)
        else:
            logging.error("Invalid tag data structure.")
            return ""

    except Exception as e:
        logging.error(f"Error generating Mermaid graph: {e}")
        return ""

    graph.append("    classDef mainNode fill:#f9f,stroke:#333,stroke-width:2px;")
    graph.append("    classDef combinedNode fill:#ff9,stroke:#333,stroke-width:2px;")

    return '\n'.join(graph)

# Example usage:
if __name__ == "__main__":
    posts_dir = "posts"  # Replace with the path to your posts directory
    output_file = "tag_data.yaml"

    # Process the tags
    tag_data = process_tags(posts_dir, output_file)

    # Generate the Mermaid graph
    mermaid_graph = generate_mermaid_graph(tag_data, direction="TD")

    # Save the Mermaid graph to a file
    with open("tag_graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_graph)

    logging.info("Mermaid graph has been written to tag_graph.mmd")
