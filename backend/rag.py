import os
from datetime import datetime

from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnableSequence
from langchain_core.output_parsers import StrOutputParser

from .preprocessor import load_vectorstore
from .db import get_db_connection


# ---------------------------------------------
# Load local model (Ollama)
# ---------------------------------------------
def load_local_llm():
    return Ollama(model="phi3:mini")



# ---------------------------------------------
# Load Vector Store
# ---------------------------------------------
vectordb = load_vectorstore()
retriever = vectordb.as_retriever(search_kwargs={"k": 2})


# ---------------------------------------------------------
# RAG PROMPT
# ---------------------------------------------------------

template = """
You are VETBOT — an offline veterinary assistant trained to give calm, friendly and helpful guidance for pet owners.

RULES:
1. Only answer questions related to:
   - pets (dogs, cats, birds, rabbits, etc.)
   - pet diseases / symptoms
   - pet care & nutrition
   - veterinary medicine
   - clinics/doctors provided in documents

2. If the user asks anything NOT related to pets or veterinary topics, reply EXACTLY:
   "This question is not related to pets or veterinary topics, so I cannot answer it."

3. Keep answers:
   - short (8-10 lines max)
   - simple
   - clear
   - not too friendly
   - actionable

4. If documents do not contain the answer, reply:
   "I don't have enough information from the documents."

5. If user says things like:
   - “okay”
   - “done”
   - “thank you”
   - “thanks”
   - “ok done”
   You MUST reply:
   "I'm glad I could help. Take good care of your pet, and feel free to ask if you need anything else."

6. Do NOT add jokes, personal stories, or unnecessary friendliness.
7. Do NOT mention page numbers, document names, or sources. Only give the answer.

Context:
{context}

Question:
{question}

VetBot Answer:

"""





prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)




# ---------------------------------------------
# Build RAG Pipeline (New Runnable format)
# ---------------------------------------------
def build_rag_chain():
    llm = load_local_llm()

    def build_inputs(question):
        return {
            "context": retriever.invoke(question),
            "question": question
        }

    chain = (
        build_inputs
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

rag_chain = build_rag_chain()


# ---------------------------------------------
# Get RAG Response
# ---------------------------------------------
# ---------------------------------------------
# Get RAG Response (with HARD FILTER)
# ---------------------------------------------
def get_rag_response(user_question: str):

    greetings = ["hi", "hello", "hey", "hii", "yo"]
    
    if user_question.lower().strip() in greetings:
        return ("Hi! How can I help with your pet today?", [])


    # ---------------------------------------------------
    # 1. TOPIC CLASSIFIER → Reject if NOT a pet question
    # ---------------------------------------------------
    pet_keywords = [
        "dog", "dogs", "cat", "cats", "kitten", "puppy",
        "parrot", "bird", "rabbit", "hamster", "pet",
        "animal", "vet", "veterinary", "clinic", "hi","hello"
    ]

    # If NONE of these words appear → instantly reject
    if not any(word in user_question.lower() for word in pet_keywords):
        return ("This question is not related to pets or veterinary topics, so I cannot answer it.", [])

    # ---------------------------------------------------
    # 2. HARD FILTER (Extra safety for random topics)
    # ---------------------------------------------------
    non_pet_keywords = [
        "capital", "president", "math", "country", "physics", "chemistry",
        "france", "india", "pasta", "recipe", "human", "brain", "history",
        "computer", "technology", "mobile", "actor", "movie"
    ]

    if any(word in user_question.lower() for word in non_pet_keywords):
        return ("This question is not related to pets or veterinary topics, so I cannot answer it.", [])

    # ---------------------------------------------------
    # 3. POLITE ENDING HANDLER
    # ---------------------------------------------------
    polite_words = ["ok", "okay", "thanks", "thank you", "done", "ok done"]

    if any(user_question.lower().strip() == w for w in polite_words):
        return ("I'm glad I could help. Take good care of your pet, and feel free to ask if you need anything else.", [])

    # ---------------------------------------------------
    # 4. NORMAL RAG MODEL CALL
    # ---------------------------------------------------
    try:
        answer = rag_chain.invoke(user_question).strip()
        return answer, []
    except Exception as e:
        return (f"Error: {e}", [])




# ---------------------------------------------
# Save chat history
# ---------------------------------------------
def save_chat_history(user_id: int, question: str, answer: str):
    conn = get_db_connection()
    cur = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO history (user_id, question, answer, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, question, answer, timestamp))

    conn.commit()
    conn.close()


# ---------------------------------------------
# Load chat history
# ---------------------------------------------
def load_chat_history(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT question, answer, timestamp
        FROM history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()

    return rows