#!/usr/bin/env zsh
# Make files/small/<issue>/<name>.jpg, 800px wide, from files/original (used as
# image_small / image_thumb). files/medium (200px) is kept so old links still work.
# Needs vips (brew install vips). Usage: zsh src/scripts/make_small.zsh
set -euo pipefail
cd "${0:A:h}/../.."
for f in files/original/*/*.jpg; do
  o=files/small/${f#files/original/}
  mkdir -p ${o:h}
  [[ -e $o ]] || vips thumbnail $f "$o[Q=82,strip,optimize_coding]" 800
done
echo "$(ls files/small/*/*.jpg | wc -l | tr -d ' ') images in files/small"
