from fastapi import FastAPI
from app.llm_openai import chat_with_llm
from app.search import web_search
from app.db import init_db, save_result

app = FastAPI(title="Web Research Assistant")

# Initialize the database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Root route (health check)
@app.get("/")
def home():
    return {"message": "Welcome to the Web Research Assistant API", "status": "running"}

# Search and summarize endpoint
@app.get("/search")
def search_and_analyze(query: str):
    search_results = web_search(query)
    context = "\n".join(
        [f"{r['title']}: {r.get('snippet', '')} ({r['link']})" for r in search_results]
    )
    ai_summary = chat_with_llm(
        "You are a research assistant that summarizes search results.",
        f"Summarize the following search results:\n{context}"
    )
    save_result(query, ai_summary)
    return {
        "query": query,
        "summary": ai_summary,
        "sources": search_results
    }















# from fastapi import FastAPI
# from app.llm_openai import chat_with_llm
# from app.search import web_search
# from app.db import init_db, save_result
#
# app = FastAPI(title="Web Research Assistant")
#
# init_db()
#
# @app.get("/search")
# def search_and_analyze(query: str):
#     search_results = web_search(query)
#     context = "\n".join([f"{r['title']}: {r['snippet']} ({r['link']})" for r in search_results])
#     ai_summary = chat_with_llm(
#         "You are a research assistant that summarizes search results.",
#         f"Summarize the following search results:\n{context}"
#     )
#     save_result(query, ai_summary)
#     return {"query": query, "summary": ai_summary, "sources": search_results}

