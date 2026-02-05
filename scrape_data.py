import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_page(id_):
    """Scrape a single details page and return the data."""
    url = f"https://anitsayac.com/details.aspx?id={id_}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {
            'id': id_,
            'ad_soyad': '',
            'il_ilce': '',
            'tarih': '',
            'neden_olduruldu': '',
            'kim_tarafindan': '',
            'korunma_talebi': '',
            'oldurulme_sekli': '',
            'failin_durumu': '',
            'kaynak': ''
        }
        
        # Field mapping: label text (normalized) -> data key
        field_map = {
            'Ad Soyad:': 'ad_soyad',
            'İl/ilçe:': 'il_ilce',
            'Tarih:': 'tarih',
            'Neden öldürüldü:': 'neden_olduruldu',
            'Kim tarafından öldürüldü:': 'kim_tarafindan',
            'Korunma talebi:': 'korunma_talebi',
            'Öldürülme şekli:': 'oldurulme_sekli',
            'Failin durumu:': 'failin_durumu',
            'Kaynak:': 'kaynak'
        }
        
        # Find all <b> tags which contain the labels
        for b_tag in soup.find_all('b'):
            # Normalize label by stripping whitespace
            label = b_tag.get_text().strip()
            
            for field_label, field_key in field_map.items():
                if label == field_label:
                    # Get the text after this <b> tag until the next <br> or tag
                    next_sibling = b_tag.next_sibling
                    if next_sibling:
                        if field_key == 'kaynak':
                            # For kaynak, get the href from the <a> tag
                            a_tag = b_tag.find_next('a')
                            if a_tag and a_tag.get('href'):
                                data[field_key] = a_tag.get('href')
                        else:
                            # Get text content
                            value = str(next_sibling).strip()
                            data[field_key] = value
                    break
        
        return data
    
    except Exception as e:
        print(f"Error scraping ID {id_}: {e}")
        return None

def main():
    # Load IDs from extracted_ids.txt
    with open('extracted_ids.txt', 'r') as f:
        ids = [int(line.strip()) for line in f if line.strip()]
    
    # Limit to first 10 IDs for testing
    ids = ids[5000:]
    
    print(f"Scraping {len(ids)} pages...")
    
    # Track failed IDs
    failed_ids = []
    
    # Open CSV for writing
    with open('scraped_data_after_5000.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'ad_soyad', 'il_ilce', 'tarih', 'neden_olduruldu', 
                      'kim_tarafindan', 'korunma_talebi', 'oldurulme_sekli', 
                      'failin_durumu', 'kaynak']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, id_ in enumerate(ids, start=1):
            print(f"({i}/{len(ids)}) Extracting ID: {id_}")
            data = scrape_page(id_)
            if data:
                writer.writerow(data)
                print(f"  -> Successfully extracted ID: {id_}")
            else:
                failed_ids.append(id_)
                print(f"  -> Failed to extract ID: {id_}")
            
            # Be respectful - add delay between requests
            time.sleep(0.5)
    
    # Save failed IDs to file
    if failed_ids:
        with open('failed_ids.txt', 'w') as f:
            for id_ in failed_ids:
                f.write(f"{id_}\n")
        print(f"\n{len(failed_ids)} failed IDs saved to failed_ids.txt")
    
    print(f"Done! Data saved to scraped_data_after_5000.csv ({len(ids) - len(failed_ids)} successful, {len(failed_ids)} failed)")

if __name__ == "__main__":
    main()
