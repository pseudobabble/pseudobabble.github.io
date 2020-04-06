title: First Post - Getting Set Up with Pelican
date: 2020-04-06
author: me

# Getting started with Python and Pelican for Github Pages

I've used the excellent guide to getting started on Github Pages using python and Pelican found here: [Github Pages with python and Pelican](https://opensource.com/article/19/5/run-your-blog-github-pages-python).

I've used python3 here.

The synopsis is as follows:

1. Create a virtual environment
   - `virtualenv -p python3 your-venv-name`
2. Activate the virtualenv
   - `source your-venv-name/bin/activate`
3. Install the required packages
   - `pip install pelican ghp-import Markdown`
4. Create the repo which will be used for your site
   - Assuming you already have a Github account, create a new repository named `your-username.github.io`. This is where the files associated with your site will be stored.
5. Clone your repo and move into it
   - `git clone your-repo-url && cd your-username.github.io`
6. Separate your sites metadata
   - Erik (the author of the guide I followed) has a useful technique to separate your sites metadata (config files, etc) from the content. You commit the metadata to a separate branch (which I've named `dev`), and use `ghp-import` to commit the content to `master`.
   - `git checkout -b dev`
7. Configure your site with Pelican
   - `pelican-quickstart`

   - You should see the following output, line by line:

```
Welcome to pelican-quickstart v3.7.1.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.

> Where do you want to create your new web site? [.]  
> What will be the title of this web site? Super blog
> Who will be the author of this web site? username
> What will be the default language of this web site? [en]
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n)
> How many articles per page do you want? [10]
> What is your time zone? [Europe/Paris] US/Central
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done. Your new project is available at /Users/username/blog
```

8. Commit your `dev` metadata, but first, remember to create a `.gitignore' file to avoid commiting the whole `venv` folder:
```
touch .gitignore && echo "venv" >> .gitignore
git add .
git commit -m "your-commit-message"
git push origin	dev
```

9. Create some content for your site
```
cd content
mkdir pages images
cp ~/Pictures/my-test-image.png images
touch 01-My-First-Post.md
touch pages/My-About-Page.md
```

Open up the `01-My-First-Post.md` file and enter the following:
```
title: My First Post
date: <today's date>
author: your-name

# My First Post

Some content blah blah blah
```

The first three lines (beginning `title: `) are part of Pelican's metadata. There are more available, check the docs.

Now open the `pages/My-About-Page.md` file and enter the following:
```
title: About
date: <today's date>

![A Picture][my_picture]

Something about yourself here


[my_picture]: {static}/images/my-test-image.png
```

10. Publish

    - Have Pelican generate the content:
`pelican content -o output -s publishconf.py`

    - Use ghp-import to commit it to master
`ghp-import -m "your-commit-message" --no-jekyll -b master output`

    - Push master
`git push origin master`

    - Commit and push the new content to `dev`
```
git add content
git commit -m 'your-commit-message'
git push origin dev
```

11. Now go check your-github-username.github.io to see what your site looks like.

#### Bonus!

I decided to create a script to handle all those publishing commands:

`touch publish.sh && chmod +x publish.sh`

```
#!/bin/bash

# activate venv - from your project root dir
source venv/bin/activate

# generate html
pelican content -o output -s publishconf.py;

# github pages commit output dir to master
ghp-import -m "Publishing on ${TODAY}" --no-jekyll -b master output

# push master
git push origin master

# commit and push dev
git add content
git commit -m "changes to dev on ${TODAY}"
git push origin dev

# deactivate venv
deactivate
```

I some shell variables to take care of automatically putting data into the commit messages. You may need to enter passwords during script execution, depending on if you use HTTPS or SSH. 