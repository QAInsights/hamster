#! /bin/sh

# shellcheck disable=SC2006
#for num in `gh release list 2>/dev/null | awk '{print $1}'`; do
#  gh release delete "$num" -y >/dev/null
#done

for num in `gh api repos/:owner/:repo/tags | jq -r '.[].name'`; do
  gh api repos/:owner/:repo/git/refs/tags/"${num}" -X DELETE >/dev/null
  echo '✓ Deleted tag' "$num"
done
