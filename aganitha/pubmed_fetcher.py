import requests
import csv
import re
from typing import List, Dict, Optional

# Define types for clarity
Paper = Dict[str, Optional[str]]

class PubMedFetcher:
    """Class to fetch and process PubMed research papers."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def fetch_paper_ids(self, query: str) -> List[str]:
        """Fetches PubMed IDs for a given query."""
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'api_key': self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('esearchresult', {}).get('idlist', [])

    def fetch_paper_details(self, paper_ids: List[str]) -> List[Paper]:
        """Fetches details for the given PubMed IDs."""
        if not paper_ids:
            return []

        params = {
            'db': 'pubmed',
            'id': ','.join(paper_ids),
            'retmode': 'json',
            'api_key': self.api_key
        }
        response = requests.get(self.SUMMARY_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return self._process_paper_data(data)

    def _process_paper_data(self, data: dict) -> List[Paper]:
        """Processes raw data into the required format."""
        papers = []
        for pmid, details in data.get('result', {}).items():
            if pmid == 'uids':
                continue
            title = details.get('title', 'Unknown Title')
            pub_date = details.get('pubdate', 'Unknown Date')
            authors = details.get('authors', [])
            corresponding_author_email = self.extract_corresponding_author_email(details)

     
            non_academic_authors = [author['name'] for author in authors if 'company' in author.get('affiliation', '').lower()]
            company_affiliations = list({author.get('affiliation', '') for author in authors if 'company' in author.get('affiliation', '').lower()})

            papers.append({
                'PubmedID': pmid,
                'Title': title,
                'Publication Date': pub_date,
                'Non-academic Author(s)': ", ".join(non_academic_authors),
                'Company Affiliation(s)': ", ".join(company_affiliations),
                'Corresponding Author Email': corresponding_author_email
            })
        return papers

    def extract_corresponding_author_email(self, details: dict) -> Optional[str]:
        """Extracts the email of the corresponding author if available."""
        authors = details.get('authors', [])
        for author in authors:
            # Assuming the email might be in the author’s affiliation or name field
            if 'email' in author:
                return author['email']
            # If not explicitly in the author's data, we can check affiliations
            affiliation = author.get('affiliation', '')
            email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', affiliation)
            if email_match:
                return email_match.group(0)
        return None
    




    def save_to_csv(self, papers: List[Paper], filename: str) -> None:
        """Saves the processed papers to a CSV file."""
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'PubmedID', 'Title', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
            ])
            writer.writeheader()
            writer.writerows(papers)
# import requests
# import csv
# import re
# from typing import List, Dict, Optional

# # Define types for clarity
# Paper = Dict[str, Optional[str]]


# class PubMedFetcher:
#     """
#     Class to fetch and process PubMed research papers.
#     """

#     BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

#     def __init__(self, api_key: Optional[str] = None):
#         self.api_key = api_key

#     def fetch_paper_ids(self, query: str) -> List[str]:
#         """
#         Fetches PubMed IDs for a given query.
#         """
#         params = {
#             'db': 'pubmed',
#             'term': query,
#             'retmode': 'json',
#             'api_key': self.api_key
#         }
#         response = requests.get(self.BASE_URL, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return data.get('esearchresult', {}).get('idlist', [])

#     def fetch_paper_details(self, paper_ids: List[str]) -> List[Paper]:
#         """
#         Fetches details for the given PubMed IDs
#         .
#         """
#         if not paper_ids:
#             return []

#         params = {
#             'db': 'pubmed',
#             'id': ','.join(paper_ids),
#             'retmode': 'json',
#             'api_key': self.api_key
#         }
#         response = requests.get(self.SUMMARY_URL, params=params)
#         response.raise_for_status()
#         data = response.json()
#         return self.process_paper_data(data)

#     def process_paper_data(self, data: dict) -> List[Paper]:
#         """
#         Processes raw data into the required format.
#         """
#         papers = []
#         for pmid, details in data.get('result', {}).items():
#             if pmid == 'uids':
#                 continue
#             title = details.get('title', 'Unknown Title')
#             pub_date = details.get('pubdate', 'Unknown Date')
#             authors = details.get('authors', [])

#             # Example heuristic: Check for company affiliations in authors
#             non_academic_authors = [
#                 author['name'] for author in authors
#                 if author.get('affiliation') and 'company' in author.get('affiliation', '').lower()
#             ]
#             company_affiliations = list({
#                 author.get('affiliation', '') for author in authors
#                 if author.get('affiliation') and 'company' in author.get('affiliation', '').lower()
#             })

#             papers.append({
#                 'PubmedID': pmid,
#                 'Title': title,
#                 'Publication Date': pub_date,
#                 'Non-academic Author(s)': ", ".join(non_academic_authors),
#                 'Company Affiliation(s)': ", ".join(company_affiliations),
#                 'Corresponding Author Email': None  # Placeholder for email extraction
#             })
#         return papers

#     def save_to_csv(self, papers: List[Paper], filename: str) -> None:
#         """
#         Saves the processed papers to a CSV file.
#         """
#         with open(filename, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=[
#                 'PubmedID', 'Title', 'Publication Date', 'Non-academic Author(s)', 'Company Affiliation(s)', 'Corresponding Author Email'
#             ])
#             writer.writeheader()
#             writer.writerows(papers)
