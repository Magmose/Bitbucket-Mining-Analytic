import requests
import json

# Define variables for workspace, repo_slug, and access_token
workspace = "YOUR_WORKSPACE"
repo_slug = "YOUR_REPO_SLUG"
access_token = "YOUR_ACCESS_TOKEN"

url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests"

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {access_token}"
}

response = requests.request(
   "GET",
   url,
   headers=headers
)

# Load the JSON data from the response
data = json.loads(response.text)

# Extract the "href" values from the "commits" keys in the "values" array, filtering out empty or null values, and store them in a list
commit_links = [value['links']['commits']['href'] for value in data['values'] if value['links']['commits']['href']]

responses = []

# Fetch responses for each href
for link in commit_links:
    resp = requests.request(
        "GET",
        link,
        headers=headers
        )   
    responses.append(resp.json())

# Save the responses array to a file named "pullrequest_comments.json"
with open('pullrequest_comments.json', 'w') as f:
    json.dump(responses, f, indent=4, separators=(",", ": "))

print("Saved responses to pullrequest_comments.json")
