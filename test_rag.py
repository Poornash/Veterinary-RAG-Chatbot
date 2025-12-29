from backend.rag import get_rag_response

while True:
    q = input("Ask VetBot: ")
    answer, src = get_rag_response(q)
    print("\nAnswer:", answer)
    print("-" * 80)
