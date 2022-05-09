#!/usr/bin/python3
"""
	Script used to generate Markdown documenation for JSON files.
"""
import sys
sys.path.append('../doc_mark_json')
import argparse
from doc_mark_json import DocMarkJson
from git_wiki import GitWiki

# Lets setup the argument parser
parser = argparse.ArgumentParser(description ='Document generation tool to create '
	+ 'Markdown documents from JSON.')

# Add Arguments
parser.add_argument('input', metavar='Input', help ='File or directory to process')
parser.add_argument('out', metavar='OutputDir', action='store', help='Directory for output')
parser.add_argument('owner', metavar='Owner', action='store', help='Directory for output')
parser.add_argument('repo', metavar='Repo', action='store', help='Directory for output')

# Parse the arguments
args = parser.parse_args()

print(args.owner)

# Let's initiate Doctor Mark JSON and Git Wiki
doc_mj = DocMarkJson()
wiki = GitWiki(args.owner, args.repo, args.out)
args.out = args.out + f"/{args.repo}.wiki"
print(args.out)
# Clone the wiki
wiki.clone()

# Process
doc_mj.discover(vars(args))

# Lets check for errors
errors = doc_mj.lint()
if errors:
	for error in errors:
		print(error)
	quit()

# Build the markdown files
doc_mj.build()

# commit wiki
wiki.commit('First wiki push test')

# push wiki
wiki.push()

# Clean the local files
wiki.remove()
