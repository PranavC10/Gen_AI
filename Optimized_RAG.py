# retrieval_system.py
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

# ======================
# Document Processing
# ======================

def process_document(pages, chunk_size=700, overlap=150):
    """Convert pages into hierarchical chunks with metadata"""
    sections = detect_sections(pages)  # Implement your section detection
    return [chunk_section(s, chunk_size, overlap) for s in sections]

def chunk_section(section_text, chunk_size, overlap):
    """Create overlapping chunks from a section"""
    return [
        {
            'text': section_text[i:i+chunk_size],
            'context_window': section_text[max(0,i-overlap):i+chunk_size+overlap],
            'section_id': hash(section_text[:50])  # Simple section identifier
        }
        for i in range(0, len(section_text), chunk_size - overlap)
    ]

# ======================
# Index Creation
# ======================

def create_indexes(chunks):
    """Create vector and keyword search indexes"""
    texts = [c['text'] for c in chunks]
    
    # Semantic index
    embedder = SentenceTransformer('all-mpnet-base-v2')
    embeddings = embedder.encode(texts)
    vector_index = faiss.IndexFlatL2(embeddings.shape[1])
    vector_index.add(embeddings)
    
    # Keyword index
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(texts)
    
    return {
        'vector_index': vector_index,
        'tfidf_matrix': tfidf_matrix,
        'embedder': embedder,
        'tfidf': tfidf,
        'chunks': chunks
    }

# ======================
# Retrieval Logic
# ======================

def retrieve_context(query, indexes, top_k=5):
    """Hybrid search with results fusion"""
    # Semantic search
    vec_results = vector_search(query, indexes, top_k*2)
    
    # Keyword search
    keyword_results = keyword_search(query, indexes, top_k*2)
    
    # Combine and rerank
    combined = combine_results(vec_results, keyword_results)
    return rerank_results(query, combined, indexes)[:top_k]

def vector_search(query, indexes, k):
    query_embed = indexes['embedder'].encode([query])
    distances, indices = indexes['vector_index'].search(query_embed, k)
    return [indexes['chunks'][i] for i in indices[0]]

def keyword_search(query, indexes, k):
    query_vec = indexes['tfidf'].transform([query])
    scores = (indexes['tfidf_matrix'] @ query_vec.T).toarray().flatten()
    top_indices = np.argpartition(scores, -k)[-k:]
    return [indexes['chunks'][i] for i in top_indices]

# ======================
# Result Processing
# ======================

def combine_results(vec_results, key_results):
    """Deduplicate and combine results"""
    seen = set()
    combined = []
    for res in vec_results + key_results:
        uid = hash(res['text'][:100])
        if uid not in seen:
            combined.append(res)
            seen.add(uid)
    return combined

def rerank_results(query, results, indexes):
    """Simple hybrid reranking"""
    return sorted(results, 
                key=lambda x: len(x['text']) * len(x['context_window']),
                reverse=True)

# ======================
# LLM Interface
# ======================

def generate_answer(query, context_chunks):
    """Format context and call LLM"""
    context_str = "\n\n".join(
        f"[[Section {c['section_id']}]] {c['context_window']}" 
        for c in context_chunks
    )
    return LLM_Call(context_str, query)

# Dummy LLM function placeholder
def LLM_Call(context, question):
    return f"Response using: {context[:200]}..."

# ======================
# Usage Example
# ======================
if __name__ == "__main__":
    # 1. Process document
    dummy_pages = [f"Page {i} content..." for i in range(300)]
    chunks = process_document(dummy_pages)
    
    # 2. Create search indexes
    indexes = create_indexes(chunks)
    
    # 3. Handle query
    user_query = "List all model validation requirements from section 4?"
    relevant_chunks = retrieve_context(user_query, indexes)
    
    # 4. Generate final answer
    answer = generate_answer(user_query, relevant_chunks)
    print("Final Answer:\n", answer)
