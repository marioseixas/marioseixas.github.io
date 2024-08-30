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

        all_posts.append({"title": title, "url": url, "date": post_date, "tags": tags})

    # Second pass: Generate tag data based on frequency threshold
    tag_data = defaultdict(
        lambda: {
            "parents": set(),
            "children": set(),
            "related": defaultdict(int),
            "posts": [],
        }
    )  # Updated 'related' to be a defaultdict(int)
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

            # Track non-hierarchical (related) relationships between tags and count co-occurrences
            for other_tag in post["tags"]:
                if (
                    other_tag != tag
                    and tag_frequency[other_tag] >= THRESHOLD
                    and tag_frequency[full_tag_path] >= THRESHOLD
                    and other_tag not in tag_data[full_tag_path]["parents"]
                    # Ensure no hierarchical relation
                    and other_tag not in tag_data[full_tag_path]["children"]
                    # Ensure no hierarchical relation
                ):
                    tag_data[full_tag_path]["related"][other_tag] += 1
                    tag_data[other_tag]["related"][full_tag_path] += 1

    # Remove tags with no posts
    tag_data = {tag: data for tag, data in tag_data.items() if data["posts"]}

    # Clean up relationships
    for tag, data in tag_data.items():
        data["parents"] = {parent for parent in data["parents"] if parent in tag_data}
        data["children"] = {child for child in data["children"] if child in tag_data}
        data["related"] = {
            related: count
            for related, count in data["related"].items()
            if related in tag_data
        }  # Keep only related tags that exist

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


def generate_mermaid_graph(
    tag_data: Union[List[Dict[str, Any]], Dict[str, Any]], direction: str = "TD"
) -> str:
    """
    Generates Mermaid ER diagram code for the tag structure,
    including parent, child, SUPERset, and SUBset relationships.

    Args:
        tag_data (Union[List[Dict[str, Any]], Dict[str, Any]]):
            List of dictionaries or dictionary containing tag relationships.
        direction (str): Graph direction (TD, LR, RL, BT). Defaults to "TD".

    Returns:
        str: Mermaid ER diagram code.
    """

    graph = [f"erDiagram"]
    added_nodes = set()
    added_edges = set()

    def sanitize_tag(tag: str) -> str:
        """Sanitizes a tag name to be a valid Mermaid identifier."""
        return (
            tag.replace(">", "_")
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

    def add_node(tag: str) -> str:
        """
        Adds a node (entity) to the graph if it hasn't been added yet,
        including handling of attributes for parent, child, related,
        SUPERset, and SUBset relationships.
        """
        safe_tag = sanitize_tag(tag)
        if safe_tag not in added_nodes:
            graph.append(f"    {safe_tag} {{")  # Start entity definition
            added_nodes.add(safe_tag)

            # Define SUPERset/SUBset for combined tags
            if ">" in tag:
                parts = tag.split(">")
                for i in range(len(parts) - 1):
                    for j in range(i + 1, len(parts)):
                        superset = ">".join(parts[: i + 1])
                        subset = ">".join(parts[: j + 1])
                        if (
                            f'parent "{sanitize_tag(superset)}"'
                            not in graph[graph.index(f"    {safe_tag} {{") :]
                            and f'child "{sanitize_tag(subset)}"'
                            not in graph[graph.index(f"    {safe_tag} {{") :]
                        ):
                            graph.append(f'        SUBset "{subset}"')
                            graph.append(f'        SUPERset "{superset}"')
        return safe_tag

    def add_edge(
        from_tag: str, to_tag: str, edge_type: str = "solid", label: str = ""
    ) -> None:
        """
        Adds an edge (relationship) between two nodes in the graph,
        including handling of parent/child and related attributes
        and ensuring proper formatting for relationship definitions.
        """

        safe_from = add_node(from_tag)
        safe_to = add_node(to_tag)
        edge = (safe_from, safe_to, edge_type)

        if edge not in added_edges:
            if edge_type == "solid":
                # Hierarchical relationship (parent-child)
                if f'parent "{to_tag}"' not in graph[
                    graph.index(f"    {safe_from} {{") :
                ]:
                    graph.append(f'        parent "{to_tag}"')  # parent attribute
                if (
                    f'child "{from_tag}"'
                    not in graph[graph.index(f"    {safe_to} {{") :]
                ):
                    graph.append(
                        f'        child "{from_tag}"'
                    )  # child attribute (if not already added)

            elif edge_type == "dashed":
                # Non-hierarchical relationship (related)
                related_count = sum(
                    1
                    for line in graph
                    if line.startswith("        related_") and f'"{to_tag}"' in line
                )
                if (
                    f'related_{related_count} "{to_tag}"'
                    not in graph[graph.index(f"    {safe_from} {{") :]
                ):
                    graph.append(
                        f'        related_{related_count} "{to_tag}"'
                    )  # related attribute
                related_count = sum(
                    1
                    for line in graph
                    if line.startswith("        related_") and f'"{from_tag}"' in line
                )
                if (
                    f'related_{related_count} "{from_tag}"'
                    not in graph[graph.index(f"    {safe_to} {{") :]
                ):
                    graph.append(
                        f'        related_{related_count} "{from_tag}"'
                    )  # related attribute
            added_edges.add(edge)

    try:
        if isinstance(tag_data, list):
            for item in tag_data:
                if isinstance(item, dict) and "tag" in item:
                    add_node(item["tag"])  # Add the node (entity)
                else:
                    logging.warning(f"Skipping invalid item in tag_data: {item}")
        elif isinstance(tag_data, dict):
            for tag_name, data in tag_data.items():
                add_node(tag_name)
        else:
            logging.error(f"Unexpected tag_data type: {type(tag_data)}")
            return ""

        if isinstance(tag_data, list):
            for item in tag_data:
                if isinstance(item, dict) and "tag" in item:
                    for child in item.get("children", []):
                        add_edge(item["tag"], child, "solid")  # Add parent-child edges
                    for related, count in item.get("related", {}).items():
                        add_edge(
                            item["tag"], related, "dashed", f"related ({count})"
                        )  # Add related edges with counts
                else:
                    logging.warning(f"Skipping invalid item in tag_data: {item}")
        elif isinstance(tag_data, dict):
            for tag_name, data in tag_data.items():
                for child in data.get("children", []):
                    add_edge(tag_name, child, "solid")  # Add parent-child edges
                for related, count in data.get("related", {}).items():
                    add_edge(
                        tag_name, related, "dashed", f"related ({count})"
                    )  # Add related edges with counts
        else:
            logging.error(f"Unexpected tag_data type: {type(tag_data)}")
            return ""
    except Exception as e:
        logging.error(f"Error processing tag_data: {e}")
        return ""

    # Ensure all entities have closing braces
    for node in added_nodes:
        if f"    {node} {{" in graph and not f"    {node} {{" in graph[
            graph.index(f"    {node} {{") + 1 :
        ]:
            graph.append("    }")
    return "\n".join(graph)


if __name__ == "__main__":
    posts_dir = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_posts")
    output_file = os.path.join(
        os.getenv("GITHUB_WORKSPACE", ""), "_data/processed_tags.yml"
    )

    tag_data, combined_tags = process_tags(posts_dir, output_file)
    mermaid_graph = generate_mermaid_graph(tag_data)

    with open(
        os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "_includes/tag_graph.html"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(f"<div class='mermaid'>\n{mermaid_graph}\n</div>")

    logging.info("Mermaid graph has been written to _includes/tag_graph.html")
