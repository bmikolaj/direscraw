#/bin/bash
#Comparing the current version of a file to all previous commits
for line in $(git log --pretty=%h); do
git diff $line --exit-code $1 > /dev/null
if [ $? == 0 ]; then
git log --stat --pretty=oneline -n 1 --abbrev-commit $line
fi
done
