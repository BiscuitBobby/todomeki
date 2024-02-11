from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import HTMLHeaderTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from todomeki.models.embeddings import all_MiniLM_L6_v2 as embeddings

def similar_search_scrape(url = "https://python.langchain.com/docs/integrations/vectorstores/qdrant", k=2):
    headers_to_split_on = [
        ("h1", None),
        ("h2", None),
        ("h3", None),
        ("h4", None),
        ("h5", None),
        ("h6", None),
    ]

    html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    html_header_splits = html_splitter.split_text_from_url(url)

    chunk_size = 500
    chunk_overlap = 30
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split
    splits = text_splitter.split_documents(html_header_splits)
    #print(splits)
    # Load the HTML content from the URLs
    data = splits

    print(data)

    try:
        qdrant = Qdrant.from_documents(
            data,
            embeddings,
            location=":memory:",  # Local mode with in-memory storage only
            collection_name="my_documents",
        )

        query = "date and time dd/mm/YYYY"
        found_docs = qdrant.max_marginal_relevance_search(query, k=k, fetch_k=10)

        result_string = ""
        for i, doc in enumerate(found_docs):
            print(f"{i + 1}.", doc.page_content, "\n")
            result_string += f"{i +  1}. {doc.page_content}\n"
            return result_string
    except:
        return None
