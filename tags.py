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

    return tag_data, combined_tags

def generate_mermaid_er_diagram(tag_data: Dict[str, Any]) -> str:
    """
    Generates Mermaid Entity Relationship (ER) diagram code for the tag structure.

    Args:
        tag_data (Dict[str, Any]): Dictionary containing tag relationships.

    Returns:
        str: Mermaid ER diagram code.
    """
    diagram = ["erDiagram"]
    added_entities = set()
    added_relationships = set()
    entity_attributes = defaultdict(lambda: {"parents": set(), "related": set()})

    def add_entity(tag: str) -> str:
        """
        Adds an entity to the diagram if it hasn't been added yet.

        Args:
            tag (str): The tag name to be added.

        Returns:
            str: The sanitized tag name used in the diagram.
        """
        safe_tag = tag.replace('>', '_').replace(' ', '_')
        if safe_tag not in added_entities:
            added_entities.add(safe_tag)
        return safe_tag

    def add_relationship(from_tag: str, to_tag: str, relationship_type: str) -> None:
        """
        Adds a relationship between two entities in the diagram and updates their attributes.

        Args:
            from_tag (str): The starting entity of the relationship.
            to_tag (str): The ending entity of the relationship.
            relationship_type (str): The type of relationship ('hierarchical' or 'related').
        """
        safe_from = add_entity(from_tag)
        safe_to = add_entity(to_tag)
        relationship = (safe_from, safe_to, relationship_type)
        if relationship not in added_relationships:
            if relationship_type == 'hierarchical':
                diagram.append(f'    {safe_from} ||--o{{ {safe_to} : "parent of"')
                entity_attributes[safe_to]["parents"].add(from_tag)
            else:  # related
                diagram.append(f'    {safe_from} ||--|| {safe_to} : "related to"')
                entity_attributes[safe_from]["related"].add(to_tag)
                entity_attributes[safe_to]["related"].add(from_tag)
            added_relationships.add(relationship)

    def process_tag(tag_name: str, data: Dict[str, Any]) -> None:
        """
        Processes a single tag and its relationships.

        Args:
            tag_name (str): The name of the tag.
            data (Dict[str, Any]): The data associated with the tag, including children and related tags.
        """
        # Add main entity
        add_entity(tag_name)

        # Handle combined tags
        if '>' in tag_name:
            parts = tag_name.split('>')
            for i in range(len(parts) - 1):
                add_relationship(parts[i], parts[i+1], 'hierarchical')

        # Add hierarchical relationships
        for child in data.get('children', []):
            add_relationship(tag_name, child, 'hierarchical')

        # Add non-hierarchical relationships
        for related in data.get('related', []):
            add_relationship(tag_name, related, 'related')

    def render_entities() -> None:
        """
        Renders all entities with their attributes in the ER diagram.
        """
        for tag, safe_tag in [(tag, tag.replace('>', '_').replace(' ', '_')) for tag in added_entities]:
            attributes = []
            for parent in sorted(entity_attributes[safe_tag]["parents"]):
                attributes.append(f'        string "parent:{parent}"')
            for related in sorted(entity_attributes[safe_tag]["related"]):
                attributes.append(f'        string "related:{related}"')
            
            if attributes:
                diagram.append(f'    {safe_tag} {{')
                diagram.extend(attributes)
                diagram.append('    }')
            else:
                diagram.append(f'    {safe_tag}')

    try:
        for tag_name, data in tag_data.items():
            process_tag(tag_name, data)
        
        render_entities()
    except Exception as e:
        logging.error(f"Error processing tag_data: {e}")
        return ""

    return '\n'.join(diagram)

if __name__ == "__main__":
    # Use environment variables to determine paths (adapt if necessary)
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml")

    tag_data, combined_tags = process_tags(posts_dir, output_file)
    mermaid_er_diagram = generate_mermaid_er_diagram(tag_data)

    # Write the Mermaid ER diagram to a file
    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_er_diagram}\n</div>")

    logging.info("Mermaid ER diagram has been written to _includes/tag_graph.html")
