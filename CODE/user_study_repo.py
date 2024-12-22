import os
import fitz  # PyMuPDF
import re

def search_abstract_in_pdfs(folder_path, output_file, keywords):
    """
    Searches through all PDFs in a folder and its subfolders for specified keywords in the abstract.
    If a keyword is found in the abstract, the file path and name are stored in an output file.

    Additionally, checks for GitHub, GitLab, Zenodo, anonymous GitHub links, Google Drive, OneDrive, and any other git links in the entire PDF.
    
    Parameters:
    - folder_path: Path to the folder to search through.
    - output_file: Name of the output file to store the results.
    - keywords: List of keywords to search for in the PDF abstracts.
    """

    # Regex patterns for different repositories and storage services
    patterns = [
        r'github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',
        r'gitlab\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',
        r'zenodo\.org/record/\d+',
        r'figshare\.com/articles/[\w/-]+',
        r'figshare\.com/collections/[\w/-]+',
        r'anonymous\.4open\.science/[\w/-]+',
        r'gitlab\.[A-Za-z0-9_.-]+\.(edu|ac|university)/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',
        r'drive\.google\.com/file/d/[A-Za-z0-9_-]+',  # Google Drive files
        r'drive\.google\.com/drive/folders/[A-Za-z0-9_-]+',  # Google Drive folders
        r'onedrive\.live\.com/[\w/-]+',  # OneDrive files
        r'1drv\.ms/[\w/-]+'  # OneDrive short links
    ]

    count = 0

    with open(os.path.join(folder_path, output_file), "w") as f_output:
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
                                # Check for links in the entire PDF
                                full_text = ""
                                for page_num in range(doc.page_count):
                                    page = doc.load_page(page_num)
                                    full_text += page.get_text("text")

                                # Match against the patterns
                                if any(re.search(pattern, full_text) for pattern in patterns):
                                    # Write the file path and name to the output file
                                    f_output.write(f"{full_path}\n")
                                    count += 1
                    
                    except Exception as e:
                        print(f"Error processing file {file}: {e}")

        # Write the count of relevant documents at the end of the file
        f_output.write(f"\nTotal relevant documents: {count}\n")

if __name__ == "__main__":
    # Define the folder path, output file name, and keywords to search for
    folder_path = '.'  # Current directory
    output_file = 'user_study_repo.txt'
    keywords = ["user study", "user-study", "questionnaire", "online survey", "user survey", "interview", "interviews"]

    # Start the search
    search_abstract_in_pdfs(folder_path, output_file, keywords)

    print("Search complete. Check the output file for results.")