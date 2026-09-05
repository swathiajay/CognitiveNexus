import os
import streamlit as st

from huggingface_hub import InferenceClient

from modules.rag import (
    extract_pdf_chunks,
    retrieve_relevant_chunks
)

from modules.evaluator import (
    create_evaluation_prompt,
    parse_evaluation
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CognitiveNexus",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HUGGING FACE CONFIGURATION
# ============================================================

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:

    st.error(
        "Hugging Face token not found. "
        "Please set HF_TOKEN in the terminal."
    )

    st.stop()


client = InferenceClient(
    api_key=HF_TOKEN
)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_chunks" not in st.session_state:
    st.session_state.pdf_chunks = []

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🧠 CognitiveNexus</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    AI-Powered Knowledge & Productivity Assistant
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ CognitiveNexus")

st.sidebar.markdown(
    """
    ### Features

    🧠 Conversation Memory

    📄 RAG Knowledge Assistant

    ⚙️ Smart Prompt Engineering

    📊 Response Evaluation

    📌 Source Support

    🎓 Personalized Study Mode
    """
)


# ============================================================
# MODE SELECTION
# ============================================================

st.subheader("Choose AI Mode")

mode = st.selectbox(
    "Select a mode",
    [
        "Research",
        "Study",
        "Analysis",
        "Content",
        "Creative",
        "General Chat"
    ]
)


mode_descriptions = {

    "Research":
        "Explore topics with structured research-oriented responses.",

    "Study":
        "Learn topics through explanations, summaries, quizzes, flashcards, and learning plans.",

    "Analysis":
        "Break down information and identify important insights.",

    "Content":
        "Create professional written content.",

    "Creative":
        "Generate creative ideas, stories, and brainstorming outputs.",

    "General Chat":
        "Ask general questions and have a natural conversation."
}


st.info(mode_descriptions[mode])


# ============================================================
# PERSONALIZED STUDY MODE
# ============================================================

study_task = None

if mode == "Study":

    st.subheader("🎓 Personalized Study Mode")

    study_task = st.selectbox(
        "Choose your study task",
        [
            "Auto Detect",
            "Explanation",
            "Summary",
            "Quiz",
            "Flashcards",
            "Learning Plan"
        ]
    )


# ============================================================
# RAG KNOWLEDGE ASSISTANT
# ============================================================

st.subheader("📄 Knowledge Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF to ask questions about it",
    type=["pdf"]
)


if uploaded_file:

    if st.session_state.pdf_name != uploaded_file.name:

        with st.spinner("Reading PDF..."):

            chunks = extract_pdf_chunks(
                uploaded_file
            )

            st.session_state.pdf_chunks = chunks
            st.session_state.pdf_name = uploaded_file.name

        if chunks:

            st.success(
                f"PDF uploaded successfully! "
                f"{len(chunks)} text chunks created."
            )

        else:

            st.warning(
                "No readable text was found in this PDF."
            )


if st.session_state.pdf_name:

    st.caption(
        f"📎 Current document: "
        f"{st.session_state.pdf_name}"
    )

    if st.button("Clear PDF"):

        st.session_state.pdf_chunks = []
        st.session_state.pdf_name = ""

        st.rerun()


# ============================================================
# TASK DETECTION
# ============================================================

def detect_task_type(
    mode,
    user_prompt,
    study_task=None
):

    prompt = user_prompt.lower()


    # --------------------------------------------------------
    # STUDY
    # --------------------------------------------------------

    if mode == "Study":

        if study_task and study_task != "Auto Detect":

            return study_task.lower().replace(
                " ",
                "_"
            )

        if any(
            word in prompt
            for word in [
                "quiz",
                "questions",
                "mcq",
                "test"
            ]
        ):

            return "quiz"


        if any(
            word in prompt
            for word in [
                "flashcard",
                "flash cards",
                "cards"
            ]
        ):

            return "flashcards"


        if any(
            word in prompt
            for word in [
                "summary",
                "summarize",
                "short notes",
                "notes"
            ]
        ):

            return "summary"


        if any(
            word in prompt
            for word in [
                "study plan",
                "learning plan",
                "timetable"
            ]
        ):

            return "learning_plan"


        return "explanation"


    # --------------------------------------------------------
    # RESEARCH
    # --------------------------------------------------------

    if mode == "Research":

        if any(
            word in prompt
            for word in [
                "compare",
                "comparison",
                "difference"
            ]
        ):

            return "comparison"


        if any(
            word in prompt
            for word in [
                "summary",
                "summarize",
                "overview"
            ]
        ):

            return "summary"


        return "research_explanation"


    # --------------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------------

    if mode == "Analysis":

        if any(
            word in prompt
            for word in [
                "compare",
                "comparison",
                "difference"
            ]
        ):

            return "comparison"


        if any(
            word in prompt
            for word in [
                "pros and cons",
                "advantages",
                "disadvantages"
            ]
        ):

            return "pros_cons"


        return "analysis"


    # --------------------------------------------------------
    # CONTENT
    # --------------------------------------------------------

    if mode == "Content":

        if any(
            word in prompt
            for word in [
                "email",
                "mail"
            ]
        ):

            return "email"


        if any(
            word in prompt
            for word in [
                "social media",
                "instagram",
                "linkedin",
                "post"
            ]
        ):

            return "social_post"


        if any(
            word in prompt
            for word in [
                "article",
                "blog"
            ]
        ):

            return "article"


        return "content_creation"


    # --------------------------------------------------------
    # CREATIVE
    # --------------------------------------------------------

    if mode == "Creative":

        if any(
            word in prompt
            for word in [
                "story",
                "short story"
            ]
        ):

            return "story"


        if any(
            word in prompt
            for word in [
                "idea",
                "ideas",
                "brainstorm"
            ]
        ):

            return "brainstorm"


        return "creative"


    # --------------------------------------------------------
    # GENERAL CHAT
    # --------------------------------------------------------

    return "general"


# ============================================================
# TASK-SPECIFIC PROMPT OPTIMIZATION
# ============================================================

def create_structured_prompt(
    mode,
    user_prompt,
    task_type,
    retrieved_context=""
):

    instructions = {

        "explanation": """
Explain the topic clearly for a student.

Use simple language.

Give:
1. Definition
2. Key points
3. Simple example

Avoid unnecessary complexity.
""",

        "summary": """
Summarize the information concisely.

Keep only the most important points.

Use clear bullet points.

Do not add unsupported information.
""",

        "quiz": """
Create a short educational quiz.

Include clear questions and answers.

Use multiple-choice questions when appropriate.

Keep the difficulty suitable for a student.
""",

        "flashcards": """
Create useful study flashcards.

Format each card as:

Question:
Answer:

Focus on important concepts and definitions.

Keep answers short and easy to revise.
""",

        "learning_plan": """
Create a practical learning plan.

Break the topic into manageable steps.

Include:

1. What to learn first
2. What to learn next
3. What to practice
4. Final revision

Keep the plan realistic for a student.
""",

        "research_explanation": """
Provide a structured research-oriented explanation.

Explain important concepts clearly.

Distinguish facts from assumptions.

Use examples when helpful.
""",

        "comparison": """
Compare the requested subjects clearly.

Use a table when appropriate.

Highlight:

- Similarities
- Differences
- Advantages
- Limitations

End with a short conclusion.
""",

        "pros_cons": """
Analyze the topic using advantages and disadvantages.

Present both sides fairly.

End with a balanced conclusion.
""",

        "analysis": """
Analyze the request carefully.

Break the problem into logical parts.

Explain important observations and conclusions clearly.

Avoid unsupported assumptions.
""",

        "email": """
Write a professional and clear email.

Include an appropriate subject line.

Maintain a polite and professional tone.

Keep the message concise.
""",

        "social_post": """
Create an engaging social media post.

Use clear and concise language.

Keep the content professional.
""",

        "article": """
Write a well-structured article.

Include:

- Introduction
- Main sections
- Conclusion

Keep the writing informative and readable.
""",

        "content_creation": """
Create polished content based on the user's request.

Use an appropriate structure, tone, and level of detail.
""",

        "story": """
Write a creative and engaging story.

Include a clear beginning, development, and ending.
""",

        "brainstorm": """
Generate multiple creative ideas.

Make each idea distinct and practical.

Briefly explain each idea.
""",

        "creative": """
Respond creatively while following the user's requirements.

Use original ideas and engaging presentation.
""",

        "general": """
Answer the user's request clearly and directly.

Use a helpful and natural tone.
"""
    }


    selected_instruction = instructions.get(
        task_type,
        instructions["general"]
    )


    context_section = ""


    if retrieved_context:

        context_section = f"""
UPLOADED DOCUMENT CONTEXT:

{retrieved_context}

IMPORTANT:

Use the uploaded document as the primary source.

If the answer is not available in the document,
clearly say that the information was not found
in the uploaded document.

Do not invent information.
"""


    return f"""
You are CognitiveNexus,
an AI-powered knowledge and productivity assistant.

MODE:
{mode}

DETECTED TASK:
{task_type}

USER REQUEST:
{user_prompt}

TASK-SPECIFIC INSTRUCTIONS:

{selected_instruction}

{context_section}

GENERAL RULES:

- Follow the user's request precisely.
- Keep the answer relevant.
- Do not invent facts.
- Use clear formatting.
- If document context is provided, prioritize it.
"""


# ============================================================
# RESPONSE GENERATION
# ============================================================

def generate_response(
    mode,
    user_prompt,
    study_task=None
):

    task_type = detect_task_type(
        mode,
        user_prompt,
        study_task
    )


    retrieved_chunks = []


    # --------------------------------------------------------
    # RAG RETRIEVAL
    # --------------------------------------------------------

    if st.session_state.pdf_chunks:

        retrieved_chunks = retrieve_relevant_chunks(
            user_prompt,
            st.session_state.pdf_chunks,
            top_k=3
        )


    retrieved_context = ""


    if retrieved_chunks:

        context_parts = []


        for chunk in retrieved_chunks:

            context_parts.append(
                f"""
[Page {chunk['page']}]

{chunk['text']}
"""
            )


        retrieved_context = "\n".join(
            context_parts
        )


    # --------------------------------------------------------
    # STRUCTURED PROMPT
    # --------------------------------------------------------

    structured_prompt = create_structured_prompt(
        mode,
        user_prompt,
        task_type,
        retrieved_context
    )


    # --------------------------------------------------------
    # SYSTEM MESSAGE
    # --------------------------------------------------------

    messages = [

        {
            "role": "system",
            "content":
                """
You are CognitiveNexus.

You are a helpful, accurate,
and context-aware AI assistant.
"""
        }

    ]


    # --------------------------------------------------------
    # CONVERSATION MEMORY
    # --------------------------------------------------------

    for item in st.session_state.chat_history:

        messages.append(
            {
                "role": item["role"],
                "content": item["content"]
            }
        )


    messages.append(
        {
            "role": "user",
            "content": structured_prompt
        }
    )


    # --------------------------------------------------------
    # HUGGING FACE MODEL
    # --------------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )


    answer = response.choices[0].message.content


    # --------------------------------------------------------
    # SAVE CONVERSATION
    # --------------------------------------------------------

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )


    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    return (
        answer,
        task_type,
        retrieved_chunks
    )


# ============================================================
# RESPONSE EVALUATION
# ============================================================

def evaluate_response(
    question,
    answer
):

    evaluation_prompt = create_evaluation_prompt(
        question,
        answer
    )


    messages = [

        {
            "role": "system",
            "content":
                """
You are a careful AI response evaluator.

Return only valid JSON.
"""
        },

        {
            "role": "user",
            "content": evaluation_prompt
        }

    ]


    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )


    evaluation_text = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )


    if evaluation_text.startswith("```"):

        evaluation_text = (
            evaluation_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    return parse_evaluation(
        evaluation_text
    )


# ============================================================
# USER INPUT
# ============================================================

st.subheader("💬 Ask CognitiveNexus")

user_prompt = st.text_area(
    "Enter your request",
    placeholder="Example: Explain Machine Learning",
    height=120
)


generate_button = st.button(
    "🚀 Generate Response"
)


# ============================================================
# GENERATE RESPONSE
# ============================================================

if generate_button:

    if not user_prompt.strip():

        st.warning(
            "Please enter a request first."
        )

    else:

        with st.spinner(
            "CognitiveNexus is thinking..."
        ):

            try:

                (
                    answer,
                    task_type,
                    retrieved_chunks
                ) = generate_response(
                    mode,
                    user_prompt,
                    study_task
                )


                # ====================================================
                # RESPONSE
                # ====================================================

                st.subheader("🤖 Response")

                st.write(answer)


                # ====================================================
                # TASK DETECTION
                # ====================================================

                st.success(
                    f"Task detected: "
                    f"**{task_type.replace('_', ' ').title()}**"
                )


                # ====================================================
                # SOURCE SUPPORT
                # ====================================================

                if retrieved_chunks:

                    st.subheader(
                        "📌 Sources from Uploaded PDF"
                    )

                    seen_pages = set()


                    for chunk in retrieved_chunks:

                        page = chunk["page"]


                        if page not in seen_pages:

                            st.write(
                                f"📄 **Page {page}**"
                            )

                            seen_pages.add(page)


                    st.info(
                        "This response used information "
                        "retrieved from the uploaded PDF."
                    )


                # ====================================================
                # RESPONSE EVALUATION
                # ====================================================

                st.subheader(
                    "📊 Response Evaluation"
                )


                with st.spinner(
                    "Evaluating response..."
                ):

                    evaluation = evaluate_response(
                        user_prompt,
                        answer
                    )


                # ------------------------------------------------
                # FIVE EVENLY ALIGNED METRICS
                # ------------------------------------------------

                col1, col2, col3, col4, col5 = st.columns(5)


                with col1:

                    st.metric(
                        "Relevance",
                        evaluation.get(
                            "relevance",
                            "N/A"
                        )
                    )


                with col2:

                    st.metric(
                        "Completeness",
                        evaluation.get(
                            "completeness",
                            "N/A"
                        )
                    )


                with col3:

                    st.metric(
                        "Accuracy",
                        evaluation.get(
                            "accuracy",
                            "N/A"
                        )
                    )


                with col4:

                    st.metric(
                        "Hallucination Safety",
                        evaluation.get(
                            "hallucination_risk",
                            "N/A"
                        )
                    )


                with col5:

                    st.metric(
                        "Overall Score",
                        evaluation.get(
                            "overall_score",
                            "N/A"
                        )
                    )


                # ------------------------------------------------
                # EVALUATION SUMMARY
                # ------------------------------------------------

                st.write(
                    "**Evaluation Summary:**"
                )


                st.info(
                    evaluation.get(
                        "summary",
                        "No evaluation summary available."
                    )
                )


            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )


# ============================================================
# SMART PROMPT ENGINEERING
# ============================================================

with st.expander(
    "⚙️ Smart Prompt Engineering"
):

    if user_prompt.strip():

        preview_task = detect_task_type(
            mode,
            user_prompt,
            study_task
        )


        st.write(
            "**Selected Mode:**",
            mode
        )


        st.write(
            "**Detected Task:**",
            preview_task.replace(
                "_",
                " "
            ).title()
        )


        st.write(
            """
            CognitiveNexus automatically adapts
            its prompt structure according to
            the selected mode and detected task.
            """
        )


    else:

        st.write(
            "Enter a request to see the detected task."
        )


# ============================================================
# CONVERSATION HISTORY
# ============================================================

if st.session_state.chat_history:

    st.subheader(
        "🧠 Conversation Memory"
    )


    for item in st.session_state.chat_history:

        if item["role"] == "user":

            st.markdown(
                f"**You:** {item['content']}"
            )

        else:

            st.markdown(
                f"**CognitiveNexus:** {item['content']}"
            )


    if st.button(
        "🗑️ Clear Conversation"
    ):

        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "CognitiveNexus • AI-Powered Knowledge & Productivity Assistant"
)