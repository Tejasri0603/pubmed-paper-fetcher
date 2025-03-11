# pubmed-paper-fetcher
## Overview
This project is a command-line tool that fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and exports the results as a CSV file.

## Code Organization
- **`pubmed_fetcher.py`**: Contains functions to fetch and process research papers from PubMed.
- **`main.py`**: Implements the command-line interface for user interaction.
- **`pyproject.toml`**: Defines project dependencies and settings for Poetry.
- **`README.md`**: Documentation about the project, installation, and usage.

## Installation
### **Prerequisites**
Ensure you have the following installed:
- **Python 3.8+**
- **Poetry** (for dependency management)

### **Steps to Install**
1. Clone the repository:
   git clone https://github.com/your-username/pubmed-paper-fetcher.git
   cd pubmed-paper-fetcher

2. Install dependencies using Poetry:
   poetry install

3. Activate the virtual environment:
   poetry shell

## Usage
Run the command-line tool using:
poetry run get-papers-list "your query here" -f output.csv

### **Command-line Options**
| Option                   | Description |
|--------                  |-------------|
| `-h, --help`             | Show help message |
| `-d, --debug`            | Enable debugging mode |
| `-f, --file <filename>`  | Save results to a CSV file |

Example:
poetry run get-papers-list "cancer treatment biotech" -f papers.csv


## Tools & Libraries Used
- **PubMed API**: [NCBI Entrez API](https://www.ncbi.nlm.nih.gov/home/develop/api/)
- **Requests**: For making HTTP requests ([Docs](https://docs.python-requests.org/en/latest/))
- **Poetry**: Dependency management ([Poetry](https://python-poetry.org/))

## License
This project is licensed under the MIT License.
