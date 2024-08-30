import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Union, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Threshold for generating permutations
THRESHOLD = 0  # Adjust this value as needed

def extract_frontmatter(file_content: str) -> str:
    """Extracts the YAML frontmatter from a markdown file."""
    frontmatter = ""
    content_lines = file_content.split("\n")
    if content_lines[0].strip() == "---":
        for i, line in enumerate(content_lines[1:], 1):
            if line.strip() == "---":
                frontmatter = "\n".join(content_lines[1:i])
                break
    return frontmatter

def generate_partial_tags(tag: str) -> List[str]:
    """Generates all partial tags for a given tag."""
    parts = tag.split(">")
    partial_tags = []
    for i in range(1, len(parts) + 1):
        for j in range(len(parts) - i + 1):
            partial_tags.append(">".join(parts[j: j + i]))
    return partial_tags

def process_tags(posts_dir: str, output_file: str) -> tuple:
    """
    Processes tags from markdown files, handling nested tags, highlighting exact matches,
    preventing duplicates using file paths, and generating a Mermaid graph.
    """

    tag_frequency = defaultdict(int)
    all_posts = []
    seen_posts = set()
    tag_co_occurrences = defaultdict(lambda: defaultdict(int))

    logging.info(f"Processing markdown files in directory: {posts_dir}")

    for filename in os.listdir(posts_dir):
        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(posts_dir, filename)
        if file_path in seen_posts:
            logging.warning(f"Skipping duplicate post: {filename}")
            continue
        seen_posts.add(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
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

        tags = post_data.get("tags", [])
        if isinstance(tags, str):
            tags = [tag.strip() for tag in tags.split(",")]
        elif not isinstance(tags, list):
            tags = [str(tags)]

        # Count tag frequencies including partial tags
        for tag in tags:
            for partial_tag in generate_partial_tags(tag):
                tag_frequency[partial_tag] += 1

        # Count tag co-occurrences
        for i, tag1 in enumerate(tags):
            for tag2 in tags[i+1:]:
                if tag1 != tag2:
                    tag_co_occurrences[tag1][tag2] += 1
                    tag_co_occurrences[tag2][tag1] += 1

        title = post_data.get("title", os.path.splitext(filename)[0])
        url = "/" + "-".join(filename.split("-")[3:]).replace(".md", "")

        try:
            post_date = datetime.strptime("-".join(filename.split("-")[:3]), "%Y-%m-%d")
        except ValueError:
            logging.warning(f"Unable to parse date from filename {filename}")
            post_date = datetime.min

        all_posts.append(
            {"title": title, "url": url, "date": post_date, "tags": tags}
        )

    # Second pass: Generate tag data based on frequency threshold
    tag_data = defaultdict(
        lambda: {"parents": set(), "children": set(), "related": set(), "posts": []}
    )
    combined_tags = set()  # Keep track of combined tags

    for post in all_posts:
        for tag in post["tags"]:
            tag_parts = tag.split(">")
            full_tag_path = tag

            # Detect combined tags and store relationships
            if len(tag_parts) > 1:
                combined_tags.add(tag)
                for i in range(len(tag_parts) - 1):
                    tag_data[tag]["parents"].add(tag_parts[i])
                    tag_data[tag_parts[i]]["children"].add(tag)

            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        "title": post["title"],
                        "url": post["url"],
                        "highlighted": partial_tag == tag,
                        "date": post["date"],
                    }
                    tag_data[partial_tag]["posts"].append(post_entry)

            # Establish parent-child relationships
            for i in range(1, len(tag_parts)):
                parent_tag = ">".join(tag_parts[:i])
                child_tag = ">".join(tag_parts[:i + 1])
                if (
                    tag_frequency[parent_tag] >= THRESHOLD
                    and tag_frequency[child_tag] >= THRESHOLD
                ):
                    tag_data[child_tag]["parents"].add(parent_tag)
                    tag_data[parent_tag]["children"].add(child_tag)

            # Track non-hierarchical (related) relationships between tags
            for other_tag in post["tags"]:
                if (
                    other_tag != tag
                    and tag_frequency[other_tag] >= THRESHOLD
                    and tag_frequency[full_tag_path] >= THRESHOLD
                    and other_tag not in tag_data[full_tag_path]["parents"]  # Ensure no hierarchical relation
                    and other_tag not in tag_data[full_tag_path]["children"]  # Ensure no hierarchical relation
                ):
                    tag_data[full_tag_path]["related"].add(other_tag)
                    tag_data[other_tag]["related"].add(full_tag_path)

    # Remove tags with no posts
    tag_data = {tag: data for tag, data in tag_data.items() if data["posts"]}

    # Clean up relationships
    for tag, data in tag_data.items():
        data["parents"] = {parent for parent in data["parents"] if parent in tag_data}
        data["children"] = {child for child in data["children"] if child in tag_data}
        data["related"] = {related for related in data["related"] if related in tag_data}

    # Sort posts within each tag by date (most recent first)
    for tag, data in tag_data.items():
        data["posts"] = sorted(
            data["posts"], key=lambda x: x.get("date", datetime.min), reverse=True
        )

    # Sort tags alphabetically before writing to YAML
    sorted_tag_data = sorted(tag_data.items())

    # Write the processed tags to a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            [{"tag": tag, "posts": data["posts"]} for tag, data in sorted_tag_data],
            f,
            allow_unicode=True,
        )

    logging.info(f"Processed tags have been written to {output_file}")

    return tag_data, combined_tags, tag_co_occurrences

def generate_mermaid_graph(
    tag_data: Union[List[Dict[str, Any]], Dict[str, Any]], 
    tag_co_occurrences: Dict[str, Dict[str, int]], 
    direction: str = "TD"
) -> str:
    """
    Generates Mermaid graph code for the tag structure.
    """
    graph = [f"erDiagram"]
    added_nodes = set()
    added_edges = set()

    def add_node(tag: str) -> str:
        """Adds a node to the graph if it hasn't been added yet."""
        safe_tag = tag.replace('>', '_').replace(' ', '_')
        if safe_tag not in added_nodes:
            node_def = f'    {safe_tag} {{'
            graph.append(node_def)

            # Add attributes
            attributes = []
            if '>' in tag:  # Combined tag
                parts = tag.split('>')
                for part in parts:
                    attributes.append(f'        parent {part}')
            for child in tag_data[tag].get('children', []):
                attributes.append(f'        child {child}')
            for related_tag, count in tag_co_occurrences[tag].items():
                attributes.append(f'        related_{count} {related_tag}')
            for parent in tag_data[tag].get('parents', []):
                if not any(attr.endswith(f' child {parent}') for attr in attributes):
                    attributes.append(f'        SUPERset {parent}')
            for child in tag_data[tag].get('children', []):
                if not any(attr.endswith(f' parent {child}') for attr in attributes):
                    attributes.append(f'        SUBset {child}')

            # Add attributes to the graph
            if attributes:
                graph.extend(attributes)

            graph.append('    }')
            added_nodes.add(safe_tag)
        return safe_tag

    def add_edge(from_tag: str, to_tag: str, label: str) -> None:
        """Adds an edge between two nodes in the graph."""
        safe_from = add_node(from_tag)
        safe_to = add_node(to_tag)
        edge = (safe_from, safe_to)
        if edge not in added_edges:
            graph.append(f'    {safe_from} ||--|| {safe_to} : "{label}"')
            added_edges.add(edge)

    try:
        for tag_name, data in tag_data.items():
            # Add hierarchical relationships (parent-child)
            for child in data.get('children', []):
                add_edge(tag_name, child, "parent of")

            # Add non-hierarchical relationships (related) with co-occurrence count
            for related_tag in data.get('related', []):
                count = tag_co_occurrences[tag_name][related_tag]
                add_edge(tag_name, related_tag, f"related to, {count} co-occurrences")

    except Exception as e:
        logging.error(f"Error processing tag_data: {e}")
        return ""

    return '\n'.join(graph)

if __name__ == "__main__":
    # Use environment variables to determine paths (adapt if necessary)
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml")

    tag_data, combined_tags, tag_co_occurrences = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_graph(tag_data, tag_co_occurrences)

    # Write the Mermaid graph to a file
    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
