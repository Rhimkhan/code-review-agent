#!/bin/bash
set -e
USERNAME="Rhimkhan"
REPOS=("object-detection-api" "Titanic-prediction" "ACC45DAYSOFCODE-2024" "house-price-predictor")

for REPO in "${REPOS[@]}"; do
  echo "--- Processing $REPO ---"
  WORKDIR=$(mktemp -d)
  gh repo clone "$USERNAME/$REPO" "$WORKDIR" -- -q

  if [ -f "$WORKDIR/README.md" ]; then
    echo "README.md already exists in $REPO, skipping."
  else
    cat > "$WORKDIR/README.md" << EOF
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
\`\`\`

## 📊 Results / Demo
[Add screenshot, output sample, or accuracy metrics here]
EOF
    cd "$WORKDIR"
    git add README.md
    git commit -q -m "Add project README"
    git push -q
    echo "✅ README.md added to $REPO"
    cd - > /dev/null
  fi
  rm -rf "$WORKDIR"
done

echo ""
echo "=== All done! ==="
