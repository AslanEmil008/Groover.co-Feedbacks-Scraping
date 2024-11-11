import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file
csv_file_path = 'influencer_profiles_Before.csv'  # Update with your CSV file path
df = pd.read_csv(csv_file_path)

# Initialize the results list
results = []

# Iterate through each URL in the 'link' column
for url in df['link']:
    # Check if the URL is empty
    if pd.isna(url) or url.strip() == "":
        # If URL is empty, print and continue
        results.append({'url': "Empty URL", 'name': "Empty link column", 'genres': "Empty link column"})
        print("Empty link column")  # Print a message when link is empty
        continue  # Skip to the next iteration

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the influencer name
        name_div = soup.find('h1', class_='influencerName ellipsis')
        if name_div:
            name = name_div.text.strip()
        else:
            name = "Name not found"
        
        # Find the section that contains the phrase "They want to receive..."
        phrase_div = soup.find(string="They want to receive...")

        if phrase_div:
            # Navigate up to the parent div of the phrase
            parent_div = phrase_div.find_parent('div')

            # Find the <li> tag for "Genres" (which should be right after the phrase div)
            genres_li = parent_div.find_next('li', class_='tw-grid-column')

            # Check if the genres <li> is found
            if genres_li:
                # Look for the tags within the 'tagGridTemplateWrapper' div
                genres_div = genres_li.find('div', class_='tagGridTemplateWrapper')
                
                if genres_div:
                    # Find all genre items within the div
                    genre_items = genres_div.find_all('div', class_='tagElementWrapper')
                    
                    # Extract the text of each genre and store it in a list
                    genres_list = [item.find('div', class_='name ellipsis').text.strip() for item in genre_items]
                    
                    # Print the genres to the console
                    if genres_list:
                        print(f"Genres for {url} ({name}): {', '.join(genres_list)}")
                    else:
                        print(f"Genres for {url} ({name}): No genres found")
                    
                    # Store genres in results
                    results.append({'url': url, 'name': name, 'genres': ', '.join(genres_list) if genres_list else "No genres found"})
                else:
                    results.append({'url': url, 'name': name, 'genres': "Genres section not found"})
                    print(f"Genres for {url} ({name}): Genres section not found")
            else:
                results.append({'url': url, 'name': name, 'genres': "Genres list not found"})
                print(f"Genres for {url} ({name}): Genres list not found")
        else:
            results.append({'url': url, 'name': name, 'genres': "Phrase not found"})
            print(f"Genres for {url} ({name}): Phrase not found")
    else:
        results.append({'url': url, 'name': name, 'genres': f"Failed to retrieve page, status code: {response.status_code}"})
        print(f"Genres for {url} ({name}): Failed to retrieve page, status code: {response.status_code}")

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a new CSV file
results_df.to_csv('Genres_Before.csv', index=False)

# print("Processing complete. Results saved to 'resulttsInfinite.csv'.")

