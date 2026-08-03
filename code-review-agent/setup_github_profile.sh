#!/bin/bash
set -e
USERNAME="Rhimkhan"

echo "=== Step 1: Creating profile README repo (Rhimkhan/Rhimkhan) ==="
mkdir -p /tmp/profile-readme && cd /tmp/profile-readme
git init -q

cat > README.md << 'EOF'
<h1 align="center">Hi 👋, I'm Rhimkhan</h1>
<h3 align="center">A passionate developer building cool things</h3>

- 🔭 I'm currently working on **[Project name here]**
- 🌱 I'm currently learning **[Skill/Tech name here]**
- 👯 I'm looking to collaborate on **[Type of project]**
- 💬 Ask me about **[Topics]**
- 📫 How to reach me: **[email or LinkedIn link]**

### 🛠️ Languages and Tools

<p align="left">
  <img src="https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/-Git-F05032?style=flat&logo=git&logoColor=white" />
</p>

### 📊 GitHub Stats

<p align="left">
  <img src="https://github-readme-stats.vercel.app/api?username=Rhimkhan&show_icons=true&theme=radical" alt="Rhimkhan's GitHub stats" />
</p>
EOF

git add README.md
git commit -q -m "Add profile README"
git branch -M main

gh repo create "$USERNAME/$USERNAME" --public --source=. --remote=origin --push
echo "✅ Profile README repo created and pushed."
echo ""

echo "=== Step 2: Adding missing descriptions to existing repos ==="
gh repo edit "$USERNAME/Titanic-prediction" \
  --description "ML model predicting Titanic passenger survival using classification algorithms"

gh repo edit "$USERNAME/ACC45DAYSOFCODE-2024" \
  --description "45 Days of Code challenge — daily coding practice and problem solving (2024)"

gh repo edit "$USERNAME/house-price-predictor" \
  --description "Regression model predicting house prices based on property features"

echo "✅ Descriptions added."
echo ""

echo "=== Step 3: Adding README templates to project repos ==="
REPOS=("sentiment-analysis-project" "object-detection-api" "Titanic-prediction" "ACC45DAYSOFCODE-2024" "house-price-predictor")

for REPO in "${REPOS[@]}"; do
  echo "--- Processing $REPO ---"
  TMPDIR=$(mktemp -d)
  gh repo clone "$USERNAME/$REPO" "$TMPDIR" -- -q

  if [ -f "$TMPDIR/README.md" ]; then
    echo "README.md already exists in $REPO, skipping (edit manually if needed)."
  else
    cat > "$TMPDIR/README.md" << EOF
# $REPO

## 📌 Overview
[One paragraph: what problem does this project solve?]

## 🛠️ Tech Stack
- Language:
- Libraries/Frameworks:
- Tools:

## 🚀 How to Run
\`\`\`bash
git clone https://github.com/$USERNAME/$REPO.git
cd $REPO
# install dependencies
# run command
\`\`\`

## 📊 Results / Demo
[Add screenshot, output sample, or accuracy metrics here]
EOF
    cd "$TMPDIR"
    git add README.md
    git commit -q -m "Add project README"
    git push -q
    echo "✅ README.md added to $REPO"
    cd - > /dev/null
  fi
  rm -rf "$TMPDIR"
done

echo ""
echo "=== All done! ==="
echo "Next manual step: Go to your GitHub profile > click 'Customize your pins' > pin your best 4-5 repos."