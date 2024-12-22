import requests
from bs4 import BeautifulSoup
import os 

def sanitize_folder_name(name):
    """
    Sanitizes the folder name for use in Windows by replacing or removing invalid characters.
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')  # Replace invalid characters with underscore
    if len(name) > 65:
        name = name[:65]
    return name

def create_folder(folder_name):
    # Check if the directory does not exist before creating it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder created: {folder_name}")
    else:
        print(f"Folder already exists: {folder_name}")

# Base URL of the page you're interested in
base_url = 'https://scholarspace.manoa.hawaii.edu/communities/aaeec9ed-5368-44e3-88e5-33ea62366840'

# Make a request to the base URL
response = requests.get(base_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all elements with the 'ng-star-inserted' class
    ng_star_elements = soup.find_all(class_='lead')
    for element in ng_star_elements:
        print(element)
    
    # Assuming the actual links are within these elements, further filter them
    community_links = [elem for elem in ng_star_elements if 'href' in str(elem)]
    
    # Extract URLs and titles (or any identifiable information)
    for community in community_links:
        # Extract the title (text) from the <a> tag
        title = community.get_text(strip=True)
        title = title[51:]
        folder = sanitize_folder_name(title.replace(" ", "_").replace("/", "_"))
        create_folder(folder)
        os.chdir(folder)
        # Extract the href attribute if available
        link = community.get('href')
        if link:
            updated_community_link = f'https://scholarspace.manoa.hawaii.edu{link}?cmscm.page=1&cmscm.rpp=100'
            print(f"Found community link: {updated_community_link}")
            response = requests.get(updated_community_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            ng_star_elements = soup.find_all(class_='lead')
            subcommunity_links = [elem for elem in ng_star_elements if 'href' in str(elem)]
            for subcommunity in subcommunity_links:
                title = subcommunity.get_text(strip=True)
                folder = sanitize_folder_name(title.replace(" ", "_").replace("/", "_"))
                create_folder(folder)
                os.chdir(folder)
                # Extract the href attribute if available
                link = subcommunity.get('href')
                if link:
                    updated_subcommunity_link = f'https://scholarspace.manoa.hawaii.edu{link}?cmcl.page=1&cmcl.rpp=100' 
                    print(f"Found subcommunity link: {updated_subcommunity_link}")
                    response = requests.get(updated_subcommunity_link)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    ng_star_elements = soup.find_all(class_='lead')
                    subsubcommunity_links = [elem for elem in ng_star_elements if 'href' in str(elem)]
                    for subsubcommunity in subsubcommunity_links:
                        # Extract the href attribute if available
                        title = subsubcommunity.get_text(strip=True)
                        folder = sanitize_folder_name(title.replace(" ", "_").replace("/", "_"))
                        create_folder(folder)
                        os.chdir(folder)
                        link = subsubcommunity.get('href')                 
                        link = link[13:]
                        if link:
                            updated_subsubcommunity_link = f'https://scholarspace.manoa.hawaii.edu/browse/dateissued?scope={link}&bbm.rpp=100'
                            print(f"Found subsubcommunity link: {updated_subsubcommunity_link}")
                            response = requests.get(updated_subsubcommunity_link)
                            soup = BeautifulSoup(response.content, 'html.parser')
                            ng_star_elements = soup.find_all(class_='item-list-title')
                            paper_links = [elem for elem in ng_star_elements if 'href' in str(elem)]
                            for paper in paper_links:
                                title = paper.get_text(strip=True)
                                paper_name = sanitize_folder_name(title.replace(" ", "_").replace("/", "_")) + '.pdf'
                                if os.path.isfile(paper_name):
                                    print("File already exists!")
                                    continue
                                link = paper.get('href') 
                                if link:
                                    updated_paper_link = f'https://scholarspace.manoa.hawaii.edu{link}'
                                    print(f"Found paper link: {updated_paper_link}")
                                    response = requests.get(updated_paper_link)
                                    soup = BeautifulSoup(response.content, 'html.parser')
                                    pdf_tags = soup.find_all('a', class_='dont-break-out')
                                    print(pdf_tags)
                                    pdf_link = pdf_tags[0]['href'] if pdf_tags else None
                                    pdf_link = pdf_link[:-9]
                                    updated_download_link = f'https://scholarspace.manoa.hawaii.edu/server/api/core{pdf_link}/content'
                                    print(updated_download_link)
                                    pdf_response = requests.get(updated_download_link)
                                    if pdf_response.status_code == 200:
                                        with open(paper_name, 'wb') as f:
                                            f.write(pdf_response.content)
                            os.chdir('..')
                    os.chdir('..') 
            os.chdir('..') 
    os.chdir('..')
else:
    print(f"Failed to access the base URL: {base_url}")