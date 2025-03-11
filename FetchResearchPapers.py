import requests
import csv
import re
from typing import List, Dict, Optional

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Fetch research papers from PubMed based on a given query.
    :param query: PubMed search query.
    :param max_results: Maximum number of results to fetch.
    :return: List of dictionaries containing paper metadata.
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    
    return fetch_paper_details(paper_ids)

def fetch_paper_details(paper_ids: List[str]) -> List[Dict[str, str]]:
    """
    Fetch detailed metadata for given PubMed paper IDs.
    :param paper_ids: List of PubMed IDs.
    :return: List of dictionaries with paper details.
    """
    if not paper_ids:
        return []
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    papers = []
    for paper_id in paper_ids:
        paper_data = data.get("result", {}).get(paper_id, {})
        papers.append({
            "PubmedID": paper_id,
            "Title": paper_data.get("title", "N/A"),
            "Publication Date": paper_data.get("pubdate", "N/A"),
            "Authors": paper_data.get("authors", [])
        })
    
    return papers

def identify_non_academic_authors(authors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Identify non-academic authors by filtering out universities and research institutions.
    :param authors: List of authors with their affiliations.
    :return: Filtered list of non-academic authors with company affiliations.
    """
    non_academic_authors = []
    academic_keywords = ["university", "college", "institute", "hospital", "school", "lab", "research"]
    
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if affiliation and not any(keyword in affiliation for keyword in academic_keywords):
            non_academic_authors.append({
                "Name": author.get("name", "Unknown"),
                "Company": affiliation
            })
    
    return non_academic_authors

def save_to_csv(papers: List[Dict[str, str]], filename: str) -> None:
    """
    Save paper details to a CSV file.
    :param papers: List of dictionaries with paper details.
    :param filename: CSV filename.
    """
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for paper in papers:
            writer.writerow({
                "PubmedID": paper["PubmedID"],
                "Title": paper["Title"],
                "Publication Date": paper["Publication Date"],
                "Non-academic Author(s)": ", ".join(a["Name"] for a in paper.get("NonAcademicAuthors", [])),
                "Company Affiliation(s)": ", ".join(a["Company"] for a in paper.get("NonAcademicAuthors", []))
            })
