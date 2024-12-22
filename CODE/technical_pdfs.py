import os
import fitz  # PyMuPDF

def search_abstract_in_pdfs(folder_path, output_file, keywords):
    """
    Searches through all PDFs in a folder and its subfolders for specified keywords in the abstract.
    If a keyword is found in the abstract, the file path and name are stored in an output file.

    Parameters:
    - folder_path: Path to the folder to search through.
    - output_file: Name of the output file to store the results.
    - keywords: List of keywords to search for in the PDF abstracts.
    """

    relevant_docs_count = 0  # Initialize counter for relevant documents

    for root, _, files in os.walk(folder_path):
        for file in files:
            if not file.startswith("Introduction") and file.endswith(".pdf"):
                try:
                    # Construct full file path
                    full_path = os.path.join(root, file)
                    # Open the PDF
                    doc = fitz.open(full_path)

                    # Assume abstract is on the first page and marked by the word "Abstract"
                    first_page = doc.load_page(0)
                    text = first_page.get_text("text")

                    # Find the abstract section
                    abstract_start = text.lower().find("abstract")
                    if abstract_start != -1:
                        # Let's assume the abstract ends at the next section heading (e.g., "Introduction")
                        next_section_start = text.lower().find("introduction", abstract_start)
                        if next_section_start != -1:
                            abstract_text = text[abstract_start:next_section_start]
                        else:
                            # In case there is no clear next section, take a reasonable chunk of text
                            abstract_text = text[abstract_start:abstract_start + 1000]  # Adjust as necessary

                        # Check if any of the keywords exist in the abstract
                        if any(keyword.lower() in abstract_text.lower() for keyword in keywords):
                            # Increment the counter for relevant documents
                            relevant_docs_count += 1

                            # Write the file path and name to the output file
                            with open(os.path.join(folder_path, output_file), "a") as f:
                                f.write(f"{full_path}\n")
                    
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

    # Write the total count of relevant documents to the output file
    with open(os.path.join(folder_path, output_file), "a") as f:
        f.write(f"\nTotal number of relevant documents: {relevant_docs_count}\n")

if __name__ == "__main__":
    # Define the folder path, output file name, and keywords to search for
    folder_path = '.'  # Current directory
    output_file = 'technical_pdfs.txt'
    keywords = ["empirical", "experiment", "experiments", "evaluation", "source code", "source-code", "artifact", "implementation", "tool"]

    # Start the search
    search_abstract_in_pdfs(folder_path, output_file, keywords)

    print("Search complete. Check the output file for results.")
