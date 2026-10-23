#!/usr/bin/env bash
# After the English build (_config.en.yml, into <site>/en), drop its copy of the
# images and IIIF files and point its pages at the Japanese build's, so that
# every image, manifest and collection keeps one URL (/lda/files/..., /lda/iiif/...).
# Usage: bash src/scripts/share_ja_assets.sh <site dir, e.g. _site>
set -euo pipefail
site=${1:?site dir}
en=$site/en
if [[ ! -d $en/files || ! -d $site/files ]]; then echo "no $en/files or $site/files" >&2; exit 1; fi
rm -rf "$en/files" "$en/iiif"
pattern=(-e '/lda/en/files/' -e '/lda/en/iiif/')
grep -rl --null --include='*.html' --include='*.json' --include='*.js' --include='*.xml' --include='*.csv' "${pattern[@]}" "$en" | while IFS= read -r -d '' f; do
  sed -i.bak -e 's#/lda/en/files/#/lda/files/#g' -e 's#/lda/en/iiif/#/lda/iiif/#g' "$f"
done || true
find "$en" -name '*.bak' -delete
left=$( (grep -rl "${pattern[@]}" "$en" || true) | wc -l | tr -d ' ')
echo "en: images and IIIF shared with the Japanese build ($left files still pointing at en)"
