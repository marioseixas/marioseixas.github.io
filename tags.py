import os
import yaml
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List

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
        partial_tags.append(">".join(parts[:i]))
    return partial_tags


def process_tags(posts_dir: str, output_file: str) -> dict:
    """Processes tags from markdown files and generates tag data."""

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

    tag_data = generate_tag_data(all_posts, tag_frequency)

    # Write the processed tags to a YAML file
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            [{"tag": tag, "posts": data["posts"]} for tag, data in sorted(tag_data.items())],
            f,
            allow_unicode=True,
        )

    logging.info(f"Processed tags have been written to {output_file}")

    return tag_data


def generate_tag_data(all_posts: list, tag_frequency: dict) -> dict:
    """Generates the tag data structure with relationships and post information."""
    tag_data = defaultdict(
        lambda: {
            "parents": set(),
            "children": set(),
            "related": defaultdict(int),
            "SUBset": set(),
            "SUPERset": set(),
            "posts": [],
        }
    )

    for post in all_posts:
        for tag in post["tags"]:
            tag_parts = tag.split(">")
            full_tag_path = tag

            # Handle combined tags (parent-child and subset-superset relationships)
            if len(tag_parts) > 1:
                for i in range(len(tag_parts) - 1):
                    parent_tag = ">".join(tag_parts[: i + 1])
                    child_tag = ">".join(tag_parts[: i + 2])
                    if (
                        tag_frequency[parent_tag] >= THRESHOLD
                        and tag_frequency[child_tag] >= THRESHOLD
                    ):
                        tag_data[child_tag]["parents"].add(parent_tag)
                        tag_data[parent_tag]["children"].add(child_tag)

                        # Subset-Superset relationships: Child is subset of Parent
                        tag_data[parent_tag]["SUBset"].add(child_tag)
                        tag_data[child_tag]["SUPERset"].add(parent_tag)

            # Process each partial tag for post association
            for partial_tag in generate_partial_tags(tag):
                if tag_frequency[partial_tag] >= THRESHOLD:
                    post_entry = {
                        "title": post["title"],
                        "url": post["url"],
                        "highlighted": partial_tag == tag,  # Highlight exact tag matches
                        "date": post["date"],
                    }
                    tag_data[partial_tag]["posts"].append(post_entry)

            # Analyze relationships between tags within a single post
            for other_tag in post["tags"]:
                if (
                    other_tag != tag
                    and tag_frequency[other_tag] >= THRESHOLD
                    and tag_frequency[full_tag_path] >= THRESHOLD
                    # Exclude tags already linked in a parent-child or subset-superset relationship
                    and other_tag not in tag_data[full_tag_path]["parents"]
                    and other_tag not in tag_data[full_tag_path]["children"]
                    and other_tag not in tag_data[full_tag_path]["SUBset"]
                    and other_tag not in tag_data[full_tag_path]["SUPERset"]
                ):
                    tag_data[full_tag_path]["related"][other_tag] += 1
                    tag_data[other_tag]["related"][full_tag_path] += 1

    # Clean up data - remove tags without posts and ensure relationships are with existing tags
    tag_data = {tag: data for tag, data in tag_data.items() if data["posts"]}
    for tag, data in tag_data.items():
        data["parents"] = {parent for parent in data["parents"] if parent in tag_data}
        data["children"] = {child for child in data["children"] if child in tag_data}
        data["related"] = {
            related: count
            for related, count in data["related"].items()
            if related in tag_data
        }
        data["SUBset"] = {subset for subset in data["SUBset"] if subset in tag_data}
        data["SUPERset"] = {
            superset for superset in data["SUPERset"] if superset in tag_data
        }

    # Sort posts by date
    for tag, data in tag_data.items():
        data["posts"] = sorted(
            data["posts"], key=lambda x: x.get("date", datetime.min), reverse=True
        )

    return tag_data


def generate_mermaid_er_diagram(tag_data: dict) -> str:
    """Generates a Mermaid ER diagram representing the tag relationships."""
    graph = ["erDiagram"]
    added_entities = set()
    added_relationships = set()  # To prevent duplicate relationships

    def sanitize_entity_name(name: str) -> str:
        """Sanitizes entity names for Mermaid compatibility."""
        return (
            name.replace(">", "_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("ç", "c")
            .replace("ã", "a")
            .replace("á", "a")
            .replace("à", "a")
            .replace("â", "a")
            .replace("é", "e")
            .replace("è", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ì", "i")
            .replace("î", "i")
            .replace("ó", "o")
            .replace("ò", "o")
            .replace("ô", "o")
            .replace("õ", "o")
            .replace("ú", "u")
            .replace("ù", "u")
            .replace("û", "u")
            .replace("ü", "u")
        )

    def add_entity(entity_name: str, data: dict) -> str:
        """Adds an entity to the Mermaid ER diagram with attributes."""
        safe_name = sanitize_entity_name(entity_name)
        if safe_name not in added_entities:
            graph.append(f"    {safe_name} {{")

            # Attributes Definition (revised to prevent redundant attributes)
            for parent in data["parents"]:
                if parent != entity_name:  # Prevent self-reference
                    graph.append(f"        type parent")
                    graph.append(f"        name {sanitize_entity_name(parent)}")
            for child in data["children"]:
                if child != entity_name:  # Prevent self-reference
                    graph.append(f"        type child")
                    graph.append(f"        name {sanitize_entity_name(child)}")
            # Exclude SUBset if it's already implied by a child relationship
            subsets_to_add = data["SUBset"].difference(data["children"])
            for subset in subsets_to_add:
                graph.append(f"        type SUBset")
                graph.append(f"        name {sanitize_entity_name(subset)}")
            # Exclude SUPERset if it's already implied by a parent relationship
            supersets_to_add = data["SUPERset"].difference(data["parents"])
            for superset in supersets_to_add:
                graph.append(f"        type SUPERset")
                graph.append(f"        name {sanitize_entity_name(superset)}")
            for related, count in data["related"].items():
                if related != entity_name:  # Prevent self-reference
                    graph.append(f"        type related")
                    graph.append(f"        name {sanitize_entity_name(related)}")

            graph.append("    }")
            added_entities.add(safe_name)
        return safe_name

    def add_relationship(from_entity: str, to_entity: str, label: str) -> None:
        """Adds a relationship link between entities, preventing duplicates."""
        relationship = (from_entity, to_entity, label)
        if relationship not in added_relationships:
            graph.append(f"    {from_entity} ||--|| {to_entity} : \"{label}\"")
            added_relationships.add(relationship)

    # Generate Entities
    for tag_name, data in tag_data.items():
        add_entity(tag_name, data)

    # Generate Relationships - Now with explicit relationship definitions
    for tag_name, data in tag_data.items():
        safe_tag_name = sanitize_entity_name(tag_name)
        # Explicit SUPERset relationship definitions
        for superset in data["SUPERset"]:
            safe_superset = sanitize_entity_name(superset)
            if superset not in data["parents"]:  # Prevent redundant links
                add_relationship(safe_tag_name, safe_superset, "SUPERset of")

    graph.append("%% Styling")
    graph.append("classDef mainNode fill:#f9f,stroke:#333,stroke-width:4px;")
    graph.append("classDef combinedNode fill:#bbf,stroke:#66f,stroke-width:2px;")
    # Mark main (atomic) tags as mainNode
    for tag_name in tag_data:
        if ">" not in tag_name:
            graph.append(f"class {sanitize_entity_name(tag_name)} mainNode;")
    # Mark combined tags as combinedNode
    for tag_name in tag_data:
        if ">" in tag_name:
            graph.append(f"class {sanitize_entity_name(tag_name)} combinedNode;")

    return "\n".join(graph)


if __name__ == "__main__":
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(
        os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml"
    )

    tag_data = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_er_diagram(tag_data)

    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
