import os
import logging
from lxml import etree
from elasticsearch import Elasticsearch

# Enable detailed logs
logging.basicConfig(level=logging.INFO)

# Fix: Specify compatibility with Elasticsearch 8.x
es = Elasticsearch(
    ["http://localhost:9200"],
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}
)

INDEX_NAME = "ruskin_works"


def init_index():
    try:
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME)
            print(f"✅ Created index: {INDEX_NAME}")
        else:
            print(f"ℹ️ Index already exists: {INDEX_NAME}")
    except Exception as e:  # Simplified exception handling
        print(f"❌ Failed to initialize index: {e}")


def parse_and_index_file(filepath):
    try:
        tree = etree.parse(filepath)
        root = tree.getroot()

        title_el = root.find(".//{*}title")
        title_text = title_el.text.strip() if title_el is not None and title_el.text else "Untitled"
        title_type = title_el.attrib.get("type", "unknown") if title_el is not None else "unknown"

        content_el = root.find(".//{*}body")
        content = etree.tostring(content_el, encoding="unicode", method="text") if content_el is not None else ""

        doc = {
            "title": title_text,
            "title_type": title_type,
            "content": content,
            "filename": os.path.basename(filepath)
        }

        es.index(index=INDEX_NAME, document=doc)
        print(f"📄 Indexed: {filepath}")

    except Exception as e:
        print(f"❌ Failed to index {filepath}: {e}")


def index_all(folder):
    if not os.path.exists(folder):
        print(f"❌ Folder '{folder}' does not exist.")
        return

    xml_files_found = False

    for root_dir, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".xml"):
                xml_files_found = True
                filepath = os.path.join(root_dir, file)
                parse_and_index_file(filepath)

    if not xml_files_found:
        print("⚠️ No XML files found to index.")


if __name__ == "__main__":
    try:
        # Test connection
        info = es.info()
        print("✅ Connected to Elasticsearch")
        print(f"Cluster: {info['cluster_name']}, Version: {info['version']['number']}")

        init_index()

        # Get the script's directory and look for data folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Go up one level from indexer/
        data_path = os.path.join(project_root, "data")

        print(f"Looking for data folder at: {data_path}")

        if os.path.exists(data_path):
            index_all(data_path)
        else:
            # Try current directory
            if os.path.exists("data"):
                index_all("data")
            else:
                print(f"❌ Data folder not found at {data_path} or ./data")
                print("Current directory contents:")
                print(os.listdir("."))

        print("🏁 Done indexing.")
    except Exception as e:
        print(f"❌ Error: {e}")