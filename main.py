name: Update Clone Count Badge

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run clone count script
        run: |
          curl -O https://raw.githubusercontent.com/MShawon/github-clone-count-badge/master/main.py
          python main.py
        env:
          GITHUB_TOKEN: ${{ secrets.SECRET_TOKEN }}

      - name: Commit and push changes
        run: |
          git config --global user.name "GitHub Action"
          git config --global user.email "action@github.com"
          git add clone.json
          git commit -m "Update clone count"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.SECRET_TOKEN }}
