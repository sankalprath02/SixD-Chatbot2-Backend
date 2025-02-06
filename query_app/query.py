import pdfplumber  # type: ignore
from langchain_groq import ChatGroq  # type: ignore

# Initialize the LLM with API key and model
llm = ChatGroq(
    temperature=0,
    groq_api_key="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",  # Replace with your API key
    model_name="llama-3.3-70b-versatile",
)

# Function to extract text from a PDF file
def extract_pdf_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

# Function to format response properly
def format_response(response):
    formatted_lines = []
    response_lines = response.split("\n")

    for line in response_lines:
        stripped_line = line.strip()

        # Ensure numbered lists (1., 2., etc.) and bullet points (-, •) start on a new line
        if stripped_line.startswith(tuple(f"{i}." for i in range(1, 21))) or stripped_line.startswith(("-", "•")):
            formatted_lines.append("\n" + stripped_line)  # New line before lists
        else:
            # Append to last item if it's part of a paragraph
            if formatted_lines and not formatted_lines[-1].endswith("\n"):
                formatted_lines[-1] += " " + stripped_line  # Keep paragraph flow
            else:
                formatted_lines.append(stripped_line)

    return "\n".join(formatted_lines).strip()

# Function to get answers based on organizational information
def ask_question_from_pdf(pdf_path, question):
    organization_info = extract_pdf_text(pdf_path)

    # Improved Prompt for Better List Structuring
    prompt = f"""
You are an expert assistant providing structured responses based on company documentation.<br><br>

<b>Response Formatting Instructions:</b><br>
- Use `<br>` tags for line breaks instead of newlines (`\n`).<br>
- Use `<b>` tags for bold text instead of bold character(`** **`).<br>
- Use paragraphs for general explanations.<br>
- <b>Use numbered lists (1., 2., 3.)</b> for ordered information with an explicit `<br>` before each point for proper format.<br>
- <b>Use bullet points (-)</b> for unordered key points.<br>
- Ensure proper `<br>` tags between sections and list items for line breaks.<br><br>

<b>Example Response Format:</b><br>
Our company provides the following services:<br><br>

1. <b>As-Built Engineering</b><br>
   - Converts brownfield facilities into accurate 3D digital models.<br>
   - Helps with modifications and compliance.<br><br>

2. <b>Dimension Control</b><br>
   - Ensures precision alignment and optimal equipment performance.<br>
   - Reduces downtime during maintenance.<br><br>

These services aim to optimize efficiency, reduce costs, and improve asset reliability.<br><br>

---<br><br>

<b>Organizational Information:</b><br>
{organization_info}<br><br>

<b>Question:</b><br>
{question}
"""
    # Get response from LLM
    response = llm.invoke(prompt)
    

    # Process and format response
    formatted_response = format_response(response.content)
    

    return formatted_response
