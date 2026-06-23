from src.llm.model import load_llm
from src.prompts.legal_prompt import build_prompt
from src.reranker.cross_encoder import apply_cross_rerank
from src.vector_store.faiss_store import load_vector_store
from src.retrievers.hybrid_retriever import get_hybrid_retriver
from src.embeddings.embedding_model import load_embeddings

class RAGChain:
    def __init__(self):
        self.embeddings = load_embeddings()
        self.db = load_vector_store(self.embeddings)
        self.prompt = build_prompt()
        self.llm = load_llm()

    def query(self, question: str):
        docs = get_hybrid_retriver(question, self.db)
        reranked_docs = apply_cross_rerank(question, docs)
        context = "\n\n".join(doc.page_content for doc in reranked_docs)
        
        response = self.llm.invoke(self.prompt.format(context=context, question=question))
        return response.content
