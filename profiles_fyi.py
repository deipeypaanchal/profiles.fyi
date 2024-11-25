import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("leetcode_finder.log"),
        logging.StreamHandler()
    ]
)

def get_linkedin_username(linkedin_url):
    # Extract username from LinkedIn URL
    linkedin_username = linkedin_url.rstrip('/').split('/')[-1]
    logging.info(f"Extracted LinkedIn username: {linkedin_username}")
    return linkedin_username

def check_leetcode_profile_api(username):
    url = 'https://leetcode.com/graphql'
    headers = {
        'Content-Type': 'application/json',
        'Referer': f'https://leetcode.com/{username}/',
        'User-Agent': 'Mozilla/5.0'
    }
    payload = {
        "operationName": "getUserProfile",
        "variables": {
            "username": username
        },
        "query": """
        query getUserProfile($username: String!) {
          matchedUser(username: $username) {
            username
          }
        }
        """
    }
    try:
        logging.info(f"Checking LeetCode profile for username: {username}")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('data', {}).get('matchedUser'):
            leetcode_profile_url = f'https://leetcode.com/{username}/'
            logging.info(f"LeetCode profile found: {leetcode_profile_url}")
            return leetcode_profile_url
        else:
            logging.info("LeetCode profile not found via API.")
            return None
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while checking LeetCode profile: {http_err}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while checking LeetCode profile: {e}")
        return None

def main():
    linkedin_url = input("Enter LinkedIn Profile URL: ").strip()
    if not linkedin_url:
        logging.error("No LinkedIn URL provided.")
        print("No LinkedIn URL provided.")
        return

    linkedin_username = get_linkedin_username(linkedin_url)
    logging.info(f"LinkedIn Username: {linkedin_username}")

    # First attempt with LinkedIn username
    leetcode_profile = check_leetcode_profile_api(linkedin_username)
    if leetcode_profile:
        print(f"LeetCode profile found: {leetcode_profile}")
        return

    # Optionally ask for GitHub username
    use_github = input("LeetCode profile not found using LinkedIn username. Do you want to provide a GitHub username to check? (yes/no): ").strip().lower()
    if use_github == 'yes':
        github_username = input("Enter GitHub Username: ").strip()
        if github_username:
            logging.info(f"GitHub Username provided: {github_username}")
            leetcode_profile = check_leetcode_profile_api(github_username)
            if leetcode_profile:
                print(f"LeetCode profile found using GitHub username: {leetcode_profile}")
                return
            else:
                logging.info("LeetCode profile not found using GitHub username.")
        else:
            logging.error("No GitHub username provided.")
            print("No GitHub username provided.")

    print("LeetCode profile not found.")
    logging.info("LeetCode profile not found after all attempts.")

if __name__ == "__main__":
    main()