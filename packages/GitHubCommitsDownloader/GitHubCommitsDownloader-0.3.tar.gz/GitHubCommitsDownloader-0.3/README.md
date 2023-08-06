# GitHubCommitsDownloader
----------

If you want explore any package's development tree you can use this package.

## Installation

```PIP
pip install GHCD
```

or

```PIP
pip install GitHubCommitsDownloader
```

## Usage

```Python
# How To Use Programatically
import GitHubCommitsDownloader as GHCD

"""
	input: {
		user: required: User's Github Name
		repo: required: User's GitHub Reposetory
		branch: not required: default: all, input: comma-separated branches list
		root: not required: default current directory
	}
"""
GHCD({
	user: "MDReal32",
	repo: "GitHubCommitsDownloader"
}).parse()
```

```Bash
# CLI Usage Guide
# input {
# 	-u/--user: required: User's Github Name
# 	-r/--repo: required: User's GitHub Reposetory
# 	-b/--branch: not required: default: all, input: comma-separated branches list
# 	-w/--workingdir: not required: default current directory
# }
GitHubCommitsDownloader -u MDReal32 -r GitHubCommitsDownloader
```