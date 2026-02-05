import re

def extract_ids(file_path):
    """Extract unique IDs from anitsayac.com details URLs."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern matches: details.aspx?id= followed by 1-5 digits
    pattern = r'details\.aspx\?id=(\d{1,5})'
    
    # Find all matches and convert to set for unique values
    ids = set(re.findall(pattern, content))
    
    # Convert to sorted list of integers
    unique_ids = sorted([int(id_) for id_ in ids])
    
    return unique_ids

if __name__ == "__main__":
    file_path = "/Users/ataberk/Downloads/view-source_https___anitsayac.com__year=2010.html"
    
    ids = extract_ids(file_path)
    
    print(f"Total unique IDs found: {len(ids)}")
    print(f"ID range: {min(ids)} - {max(ids)}")
    print(f"\nFirst 10 IDs: {ids[:10]}")
    print(f"Last 10 IDs: {ids[-10:]}")
    
    # Save to file
    with open("extracted_ids.txt", "w") as f:
        for id_ in ids:
            f.write(f"{id_}\n")
    
    print(f"\nAll IDs saved to extracted_ids.txt")
