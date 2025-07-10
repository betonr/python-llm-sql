# 🧠 Conversational BI with SQL + LLMs (Local Setup)

This project showcases how to combine a smart chatbot with SQL queries to explore business data conversationally. It merges a React front-end with a FastAPI back-end and LLMs running locally via [Ollama](https://ollama.com/), with no external cloud needed.

## 🧩 Project Structure

```
.
├── front-end          # React interface
├── back-llm           # Python API (FastAPI + LlamaIndex)
├── docker-compose.yml # Infrastructure services (Ollama, Postgres, PgAdmin)
└── README.md
```

## 🚀 Features

* Chat interface for natural language questions like:

  * "Who sold the most today?"
  * "How many clients did João assist last week?"
* Backend turns questions into SQL using **SQLCoder 7B** (running locally with Ollama)
* Results are queried directly from Postgres

---

## ✅ Requirements

* Docker installed and running
* At least 16GB of free RAM to run models locally
* Python 3.10+ with `pip` (if running backend outside Docker)
* Node.js 18+ with `npm` or `yarn` (for front-end)

---

## 🔧 Getting Started (Local Setup)

### 1. Launch infrastructure

```bash
docker-compose up -d
```

This spins up:

* 🐘 `postgres`: database
* 📊 `pgadmin`: web interface ([http://localhost:5050](http://localhost:5050))
* 🤖 `ollama`: LLM server ([http://localhost:11434](http://localhost:11434))

### 2. Access Ollama container to download models

Open a terminal into the Ollama container:

```bash
docker exec -it ollama bash
```

Inside the container, run:

```bash
ollama pull sqlcoder:7b
ollama pull nomic-embed-text
```

> You can also use the host system if Ollama is installed natively.

### 3. Access the database using pgAdmin

* Email: `admin@admin.com`
* Password: `admin`
* Host: `postgres`
* Username: `postgres`, Password: `password`

Create a database named `sales_db` and add tables:

```sql
CREATE TABLE attendants (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE sales (
  id SERIAL PRIMARY KEY,
  attendant_id INTEGER,
  amount REAL,
  sale_date DATE,
  FOREIGN KEY (attendant_id) REFERENCES attendants(id)
);
```

Add sample data if needed.

### 4. Run the backend

```bash
cd back-llm
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Update the database URI in `main.py`:

```python
"postgresql://postgres:postgres@localhost:5432/sales_db"
```

Start the API:

```bash
uvicorn main:app --reload
```

### 5. Run the front-end

```bash
cd front-end
npm install
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) and chat away 🎯

---

## 🛠 Tech Stack

* **FastAPI** – lightweight Python API
* **LlamaIndex** – connects structured data to LLMs
* **SQLCoder 7B** – open-source SQL generation model
* **nomic-embed-text** – lightweight embedding model
* **Ollama** – local LLM orchestrator
* **PostgreSQL** – relational database
* **React + Tailwind** – modern and responsive front-end

---

## 💡 Future Ideas

* JWT-based user authentication
* Chat history and smart prompt tags
* On-demand mini-charts via chat
* Multi-schema or multi-tenant support


---

For questions, suggestions, or collaboration, reach out on [LinkedIn](https://www.linkedin.com/in/betonoronha/) 🙌
