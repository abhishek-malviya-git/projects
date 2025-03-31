import faiss
import numpy as np
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_core.documents import Document


class ScriptIntentMatcher:
    """Matches user queries to relevant scripts using FAISS and OpenAI embeddings."""

    def __init__(self, api_key):
        self.embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=api_key)

        # ✅ Define script intents and their corresponding execution scripts
        self.script_intents = {
            "check cpu usage": "get_cpu_usage.py",
            "monitor memory usage": "get_memory_usage.py",
            "fetch server statistics perfromance telemetry": "grafana_server_statistics.py",
            "fix slow down unresponsive server": "ansible_playbook_execution.py",
            "troubleshoot network application issue": "ansible_playbook_execution.py",
            "delete temporary files from temp folder when temp folder size exceed 5MB":"e_delete_temp_files.py"
        }

        # ✅ Initialize FAISS Vector Store
        self.vector_store = self.build_vector_store()

    # def build_vector_store(self):
    #     """Builds a FAISS vector store with script intents and their embeddings."""
    #     texts = list(self.script_intents.keys())  # Intent text (searchable)
    #     embeddings = self.embeddings_model.embed_documents(texts)  # Convert text to embeddings

    #     # ✅ Use LangChain’s FAISS utility to create the vector store
    #     store = FAISS.from_texts(texts, self.embeddings_model)

    #     return store


    def build_vector_store(self):
        """Builds a FAISS vector store with script intent embeddings."""
    
        # ✅ Extract intent texts
        texts = list(self.script_intents.keys())
    
        # ✅ Generate embeddings
        embeddings = self.embeddings_model.embed_documents(texts)
    
        # 🔹 Convert embeddings list to NumPy array (Required by FAISS)
        embeddings_np = np.array(embeddings, dtype=np.float32)  # 🔥 FIX: Convert to NumPy array
    
        # ✅ Create FAISS index with L2 distance metric
        index = faiss.IndexFlatL2(embeddings_np.shape[1])
        index.add(embeddings_np)  # ✅ FIX: Pass NumPy array, not list
    
        # ✅ Create an in-memory docstore
        docstore = InMemoryDocstore({i: Document(page_content=texts[i]) for i in range(len(texts))})
    
        # ✅ Create a simple mapping from FAISS index to docstore
        index_to_docstore_id = {i: i for i in range(len(texts))}
    
        # ✅ Pass **Embeddings Object** (instead of function)
        store = FAISS(
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
            embedding_function=self.embeddings_model  # ✅ FIXED: Pass embeddings object
        )
    
        return store





    def find_best_script(self, query):
        """Finds the most relevant script based on user query using FAISS vector search."""
        query_embedding = self.embeddings_model.embed_query(query)  # Convert query to embedding
        
        # ✅ Perform FAISS search (Finds the closest match)
        results = self.vector_store.similarity_search_by_vector(np.array(query_embedding, dtype="float32"), k=1)

        if not results:
            return "No relevant script found."

        matched_intent = results[0].page_content
        return self.script_intents.get(matched_intent, "No relevant script found.")

# --- 🔹 Main Function to Test Intent Matching ---
def main():
    """Test the ScriptIntentMatcher with example queries."""
    
    #api_key = "your_openai_api_key"  # 🔹 Replace with your actual OpenAI API key
    matcher = ScriptIntentMatcher(api_key)

    # ✅ Sample user queries
    test_queries = [
        "Check CPU load",  # Should match "check cpu usage"
        "Find memory performance",  # Should match "monitor memory usage"
        "Troubleshoot network slow speed",  # Should match "troubleshoot network issue"
        "Fix frozen database server",  # Should match "fix unresponsive server"
        "Application Server Appserver02 is unresponsive, take action.",  # Should match "fetch server telemetry"
        "Get data of server name 'grafana-server-05' from Grafana",
        "What is the Memory usage of system ?",
        "Server R56S2323SQS is not responding as expected check it",
        "Please troubleshoot slow response on dbserver03?",
        "Please get me statistics of server WRRSS03W531 ?"# Unrecognized intent
    ]

    print("\n🔍 **Testing Script Intent Matcher**")
    for query in test_queries:
        matched_script = matcher.find_best_script(query)
        print(f"📌 Query: {query}\n🔗 Matched Script: {matched_script}\n")

if __name__ == "__main__":
    main()
