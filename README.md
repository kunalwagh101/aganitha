1. **Clone the repository**:
   ```bash
   git clone git@github.com:kunalwagh101/aganitha.git
   cd aganitha

2. **create virtual venv**:
   ```bash
   python -m venv venv
   venv/scripts/activate --- windows

   source venv/bin/activate --- Mac


3. **Run the requirements file**:
   ```bash
   pip install -r requirements.txt


3. **Run the program**:
   ```bash
  poetry install
  poetry run get-papers-list "cancer AND therapy" -f output.csv