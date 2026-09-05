import re
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_pdf_chunks(uploaded_file, chunk_size=1000):
    """
    Extract text from PDF and divide it into chunks
    while keeping the page number.
    """

    reader = PdfReader(uploaded_file)

    chunks = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if not page_text:
            continue

        page_text = re.sub(r"\s+", " ", page_text).strip()

        for i in range(0, len(page_text), chunk_size):

            chunk_text = page_text[i:i + chunk_size]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

    return chunks


def retrieve_relevant_chunks(query, chunks, top_k=3):
    """
    Retrieve the most relevant PDF chunks
    using TF-IDF and cosine similarity.
    """

    if not chunks:
        return []

    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    documents = chunk_texts + [query]

    matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []

    for index in top_indices:

        if similarities[index] > 0:

            results.append({
                "text": chunk_texts[index],
                "page": chunks[index]["page"],
                "score": float(similarities[index])
            })

    return results