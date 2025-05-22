import os
from lxml import etree
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")
INDEX_NAME = "ruskin_works"

def init_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)

def parse_and_index_file(filepath):
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

    es.index(index=INDEX_NAME, body=doc)

def index_all(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".xml"):
                filepath = os.path.join(root, file)
                print(f"Indexing {filepath}")
                parse_and_index_file(filepath)

if __name__ == "__main__":
    init_index()
    index_all("data")
    print("✅ All documents indexed.")
