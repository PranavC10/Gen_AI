import json
import pandas as pd
import os

def LLM_call(text):
    """
    Placeholder for your LLM call function.
    Replace this function with your actual implementation.
    
    The function is expected to return a JSON string representing an array of objects.
    Each object must have:
      - "simple_prompt": The simplified sub-question.
      - "keywords": A list of keywords.
      - "final_prompt": The final audit prompt.
    """
    # For demonstration purposes, we'll return a dummy JSON response.
    dummy_response = json.dumps([
        {
            "simple_prompt": text,  # In a real scenario, this would be a simplified version.
            "keywords": ["example", "keywords"],
            "final_prompt": f"AUDIT: {text} | Keywords: example, keywords. Please verify the query's accuracy."
        }
    ])
    return dummy_response

def split_question_using_llm(question_text):
    """
    Constructs a prompt for the LLM to split a complex question into simple sub-prompts.
    The LLM is expected to return a JSON array of objects with:
      - "simple_prompt"
      - "keywords"
      - "final_prompt"
    """
    prompt = f"""
You are an assistant that takes a complex questionnaire question and splits it into N simple sub-prompts for use in retrieval augmented generation (RAG).
For each sub-prompt, extract the main keywords that are essential for searching the document.
Additionally, generate a final audit prompt that includes:
  - The simplified sub-question.
  - The extracted keywords.
  - An instruction for the model audit team to verify that the simplified query accurately reflects the original question's intent.
Return your answer as a JSON array of objects. Each object must have exactly three keys:
  - "simple_prompt": The simplified sub-question.
  - "keywords": A list of keywords.
  - "final_prompt": The final audit prompt.
  
Question: "{question_text}"

Ensure that the output is valid JSON.
    """
    response_text = LLM_call(prompt)
    try:
        result = json.loads(response_text)
    except Exception as e:
        print("Error parsing JSON response:", e)
        result = []
    return result

def main():
    # Path to the Excel file containing questionnaire forms.
    excel_file_path = "questions.xlsx"  # Update this path as needed.

    if not os.path.exists(excel_file_path):
        print(f"Error: File '{excel_file_path}' not found.")
        return

    # Read the Excel file; it must contain a column named "Question".
    df = pd.read_excel(excel_file_path)
    if "Question" not in df.columns:
        print("Error: Excel file must contain a 'Question' column.")
        return

    processed_questions = []
    for idx, row in df.iterrows():
        question_text = row["Question"]
        print(f"Processing Question {idx+1}: {question_text}")
        sub_prompts = split_question_using_llm(question_text)
        processed_questions.append({
            "Original Question": question_text,
            "Sub Prompts": sub_prompts
        })

    # Print the results for each question.
    for item in processed_questions:
        print("\n========================================")
        print("Original Question:")
        print(item["Original Question"])
        print("========================================\n")
        for sub in item["Sub Prompts"]:
            print("Final Audit Prompt:")
            print(sub.get("final_prompt", ""))
            print("\n")

    # Optionally, save the processed results to a JSON file for later review.
    with open("processed_questions.json", "w") as f:
        json.dump(processed_questions, f, indent=4)

if __name__ == "__main__":
    main()
