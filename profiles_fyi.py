import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed output
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename="leetcode_finder.log",
    filemode='a'
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
    st.title("LeetCode Profile Finder")
    st.write("Enter a LinkedIn Profile URL to find the corresponding LeetCode profile.")

    linkedin_url = st.text_input("LinkedIn Profile URL")

    if st.button("Find LeetCode Profile"):
        if not linkedin_url:
            logging.error("No LinkedIn URL provided.")
            st.error("Please provide a LinkedIn URL.")
            return

        linkedin_username = get_linkedin_username(linkedin_url)
        logging.info(f"LinkedIn Username: {linkedin_username}")

        # First attempt with LinkedIn username
        leetcode_profile = check_leetcode_profile_api(linkedin_username)
        if leetcode_profile:
            st.success(f"LeetCode profile found: {leetcode_profile}")
            st.markdown(f"[View LeetCode Profile]({leetcode_profile})")
            return
        else:
            logging.info("LeetCode profile not found using LinkedIn username.")
            st.warning("LeetCode profile not found using LinkedIn username.")

            # Optionally ask for GitHub username
            use_github = st.radio(
                "LeetCode profile not found. Do you want to provide a GitHub username to check?",
                ('Yes', 'No')
            )
            if use_github == 'Yes':
                github_username = st.text_input("GitHub Username")
                if st.button("Check GitHub Username"):
                    if github_username:
                        logging.info(f"GitHub Username provided: {github_username}")
                        leetcode_profile = check_leetcode_profile_api(github_username)
                        if leetcode_profile:
                            st.success(f"LeetCode profile found using GitHub username: {leetcode_profile}")
                            st.markdown(f"[View LeetCode Profile]({leetcode_profile})")
                            return
                        else:
                            logging.info("LeetCode profile not found using GitHub username.")
                            st.error("LeetCode profile not found using GitHub username.")
                    else:
                        logging.error("No GitHub username provided.")
                        st.error("Please provide a GitHub username.")
            else:
                st.info("LeetCode profile not found after all attempts.")
                logging.info("LeetCode profile not found after all attempts.")

if __name__ == "__main__":
    main()