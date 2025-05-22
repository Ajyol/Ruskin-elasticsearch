# 📚 Ruskin Elasticsearch

This project allows you to parse, index, and search through XML documents using **Elasticsearch**, with optional visualization using **Kibana**. It's designed to help you process literary or archival collections like the works of John Ruskin.

---

## ✨ Features

- Parses structured XML files.
- Indexes documents into Elasticsearch for full-text search.
- Easy Docker setup for Elasticsearch and Kibana.
- Ready for Flask integration to build a search UI.

---

## 📁 Project Structure
```
ruskin-elasticsearch/
│
├── indexer/
│   └── parse_and_index.py       # XML parsing and indexing script
── app/
│   └── search_api.py            # Searching API
├── data/                        # Put your XML files here
├── docker-compose.yml           # Docker config (ES + Kibana)
├── requirements.txt             # Python dependencies
└── README.md                    # Project guide
```
---

## 📌 Step 1: Install all the Dependencies
Everything you need is listed in `requirements.txt`, so run the following command in your terminal to have everything installed.
```bash
  pip install -r requirements.txt
```

## 🐳 Step 2: Start Elasticsearch & Kibana with Docker

1. Make sure Docker is installed and running.
2. In your project folder, there is a file called `docker-compose.yml` that has all the requirements for installing and runnning elasticsearch in your container.
3. Then run:

```bash
  docker-compose up -d
```

## 🐍 Step 3: Set Up Python Environment
### 1. Create and activate a virtual environment

```bash
  python3 -m venv venv
  source venv/bin/activate    # On Windows: venv\Scripts\activate
```

## 📄 Step 3: Index Your XML Files
1. Put your XML files in a data/ folder at the project root.
2. Run the indexer script:

```bash
  python indexer/parse_and_index.py
```

## 🔍 Step 4: Search with Kibana
1. Open your browser and go to [http://localhost:5601](http://localhost:5601).
2. Click on **Discover** in the left sidebar.
3. Create a new **Data View** with the following settings:
   - **Name**: `ruskin_works`
   - **Index pattern**: `ruskin_works`
   - **Timestamp field**: *(leave this blank)*
4. Click **Create data view**.
5. Once created, you can use the **Discover** tab to search and explore your indexed XML documents.

## 🔍 Step 5: Use the search API to lookup
Run the following prompt on your terminal or simply run `search_api.py`.
```bash
  python app/search_api.py
```
