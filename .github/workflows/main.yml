name: Update JWT Tokens

on:
  schedule:
    - cron: '0 */7 * * *'     # প্রতি ৭ ঘণ্টা পরপর
  workflow_dispatch:          # ম্যানুয়ালি রান করতে পারবে

jobs:
  update-tokens:
    runs-on: ubuntu-latest
    permissions:
      contents: write        # ফাইল আপডেট ও পুশ করার অনুমতি

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run Token Update Script
        run: python update_tokens.py

      - name: Commit and Push Changes
        run: |
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          
          if git diff --quiet tokens.json; then
            echo "✅ No changes in tokens.json"
          else
            git add tokens.json
            git commit -m "Update tokens [Automated] - $(date '+%Y-%m-%d %H:%M:%S')"
            git push
            echo "✅ Tokens updated and pushed successfully!"
          fi
