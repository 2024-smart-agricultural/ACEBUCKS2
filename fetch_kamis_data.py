name: Fetch KAMIS API Data

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  fetch-kamis-data:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Fetch KAMIS Data
        env:
          KAMIS_KEY: ${{ secrets.KAMIS_KEY }}
          P_CERT_ID: ${{ secrets.P_CERT_ID }}
        run: |
          python fetch_kamis_data.py

      - name: Commit and push XML files
        run: |
          git config --global user.email "heejun1481@jbnu.ac.kr"
          git config --global user.name "aceyang00"
          git add kamis_data_*.xml
          git commit -m "Add fetched KAMIS data in XML format"
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
