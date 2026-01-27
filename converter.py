import re
import json
import requests

def convert_md_to_json(source_url, output_file):
    print(f"Fetching markdown from: {source_url}")
    
    try:
        response = requests.get(source_url)
        response.raise_for_status()
        md_text = response.text
    except Exception as e:
        print(f"Error fetching file: {e}")
        return

    # This regex looks for lines starting with #, ##, or ###
    # It uses a lookahead to split the string without losing the headers
    sections = re.split(r'\n(?=#+\s)', md_text)
    
    json_data = []
    
    for index, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
            
        # Extract the title from the first line of the section
        title_match = re.match(r'^#+\s+(.*)', section)
        title = title_match.group(1).strip() if title_match else f"Section {index + 1}"
        
        # Create a dictionary for the case
        case_entry = {
            "id": f"case-{index}",
            "title": title,
            "content": section,
            "char_count": len(section)
        }
        
        json_data.append(case_entry)

    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully converted {len(json_data)} cases to {output_file}")

if __name__ == "__main__":
    GITHUB_URL = "https://raw.githubusercontent.com/citecase/archives/main/2026.md"
    OUTPUT_NAME = "2026.json"
    
    convert_md_to_json(GITHUB_URL, OUTPUT_NAME)
