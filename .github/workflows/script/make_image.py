from github import *
import requests
import os
import os.path
from collections import Counter
import matplotlib.pyplot as plt

# GitHub API token and repository information
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
OWNER = 'Vita3K'
REPO = 'compatibility'

# List of labels to count
TARGET_LABELS = ['Nothing', 'Bootable', 'Intro', 'Menu', 'Ingame -', 'Ingame +', 'Playable']

# Add token to headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}'
}

# Function to get all issues using pagination
def get_all_issues(owner, repo, headers):
    issues = []
    page = 1
    per_page = 100  # Maximum per_page value
    while True:
        issues_url = f'https://api.github.com/repos/{owner}/{repo}/issues?page={page}&per_page={per_page}'
        response = requests.get(issues_url, headers=headers)
        page_issues = response.json()
        if not page_issues:  # If the page is empty, break the loop
            break
        issues.extend(page_issues)
        page += 1
    return issues

# Retrieve all issues
issues = get_all_issues(OWNER, REPO, headers)

# Count specific labels
labels = []
for issue in issues:
    for label in issue['labels']:
        if label['name'] in TARGET_LABELS:
            labels.append(label['name'])

label_counts = Counter(labels)

# sort inverse
sorted_label_counts = dict(sorted(label_counts.items(), key=lambda item: item[1]))

print(sorted_label_counts)

# Define colors for the labels
colors = ['#ff0000','#621fa5','#c71585','#1d76db','#e08a1e','#fbca04','#0e8a16']

# Sort the counts according to TARGET_LABELS order
labels = TARGET_LABELS
sizes = [label_counts[label] for label in labels]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
ax1.axis('equal')  # Draw the pie chart as a circle

# Save the image
plt.savefig('labels_pie_chart.svg')
