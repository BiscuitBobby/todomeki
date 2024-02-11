from langchain_community.embeddings import HuggingFaceEmbeddings

print("loading all-MiniLM-L6-v2")
all_MiniLM_L6_v2 = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("loaded all-MiniLM-L6-v2")
