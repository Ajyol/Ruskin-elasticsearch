from elasticsearch import Elasticsearch

es = Elasticsearch(
    ["http://localhost:9200"],
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=8"}
)

INDEX_NAME = "ruskin_works"

def search_documents(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "title_type", "content"]
            }
        }
    }

    res = es.search(index=INDEX_NAME, body=body)

    print(f"\n🔍 Results for: '{query}'")
    for hit in res['hits']['hits']:
        print(f"\n📄 Filename: {hit['_source']['filename']}")
        print(f"📌 Title: {hit['_source']['title']}")
        print(f"📝 Snippet: {hit['_source']['content'][:200]}...")

if __name__ == "__main__":
    keyword = input("Enter your search keyword: ")
    search_documents(keyword)
