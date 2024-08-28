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

def generate_mermaid_er_diagram(
    tag_data: Union[List[Dict[str, Any]], Dict[str, Any]], direction: str = "TD"
) -> str:
    """
    Generates Mermaid ER diagram code for the tag structure with modified attribute 
    definitions and fixes for invalid characters, missing colons, and incorrect 
    relationship syntax. Also includes child and collection attributes.
    """
    graph = [f"erDiagram"]
    added_entities = set()
    added_relationships = set()

    def sanitize_entity_name(name: str) -> str:
        """Replaces invalid characters in entity names with underscores."""
        return name.replace(">", "_").replace(" ", "_").replace("ç", "c").replace("ã", "a")  # Add more replacements as needed

    def add_entity(entity_name: str, data: Dict[str, Any]) -> str:
        """Adds an entity to the diagram with parent, related, part-of, child, and collection attributes."""
        safe_name = sanitize_entity_name(entity_name)
        if safe_name not in added_entities:
            graph.append(f"    {safe_name} {{")
            for parent in data.get("parents", []):
                graph.append(f"        parent {sanitize_entity_name(parent)}")
            for related in data.get("related", []):
                graph.append(f"        related {sanitize_entity_name(related)}")
            if ">" in entity_name:
                parts = entity_name.split(">")
                for part in parts:
                    graph.append(f"        part_of {sanitize_entity_name(part)}")
            # Add child attributes 
            for child in data.get("children", []):
                graph.append(f"        child {sanitize_entity_name(child)}")
            
            # Add collection attributes for combined tags
            if '>' in entity_name:  # Assuming combined tags represent collections
                graph.append(f"        collection {sanitize_entity_name(entity_name)}")  
                
            graph.append("    }")
            added_entities.add(safe_name)
        return safe_name

    def add_relationship(
        from_entity: str,
        to_entity: str,
        relationship_type: str = "||--||",
        label: str = "",
    ) -> None:
        """Adds a relationship between two entities with correct syntax."""
        safe_from = add_entity(from_entity, tag_data.get(from_entity, {}))
        safe_to = add_entity(to_entity, tag_data.get(to_entity, {}))
        relationship = (safe_from, safe_to, relationship_type)
        if relationship not in added_relationships:
            label_part = f'"{label}"' if label else ""
            # Correct relationship syntax: EntityName RelationshipType EntityName Label (optional) 
            graph.append(f"    {safe_from} {relationship_type} {safe_to} {label_part}")  
            added_relationships.add(relationship)


    def process_tag(tag_name: str, data: Dict[str, Any]) -> None:
        """Processes a single tag and its relationships."""
        # Add main entity
        add_entity(tag_name, data)  # Pass data to add_entity

        # Handle combined tags as entities and relationships
        if ">" in tag_name:
            parts = tag_name.split(">")
            combined_tag = add_entity(tag_name, data)  # Pass data to add_entity
            for part in parts:
                add_relationship(part, combined_tag, "}|--|{", "part of") 

        # Add hierarchical relationships
        for child in data.get("children", []):
            add_relationship(tag_name, child, "||--|{", "parent of") 

        # Add non-hierarchical relationships
        for related in data.get("related", []):
            add_relationship(tag_name, related, "||..||", "related to") 

    try:
        if isinstance(tag_data, list):
            for item in tag_data:
                if isinstance(item, dict) and "tag" in item:
                    process_tag(item["tag"], item)
                else:
                    logging.warning(f"Skipping invalid item in tag_data: {item}")
        elif isinstance(tag_data, dict):
            for tag_name, data in tag_data.items():
                process_tag(tag_name, data)
        else:
            logging.error(f"Unexpected tag_data type: {type(tag_data)}")
            return ""

    except Exception as e:
        logging.error(f"Error processing tag_data: {e}")
        return ""

    return "\n".join(graph)

if __name__ == "__main__":
    # Use environment variables to determine paths (adapt if necessary)
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(
        os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml"
    )

    tag_data, combined_tags = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_er_diagram(tag_data)

    # Write the Mermaid graph to a file
    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
