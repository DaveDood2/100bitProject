Hello! This is the public version of the 100bit project I made for a data mining class in the University of Tennessee. Feel free to use the graphs generated from my code for whatever.

Note: If you don't feel like installing jupyter-notebook/conda, you can still view this project in the files, "100 Bit Crawler.ipynb" and "100 Bit Project.ipynb". The only problem is that you will not be able to re-run the code. Also note that if you are viewing the .ipynb files on a web browser, you MAY need to refresh a few times before it will properly load.

Install conda from here: https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html

Install jupyter-notebook from here: https://jupyter.org/install

Then, from the github repository, run:
<code>conda env create -f environment.yml</code>

This should create a new conda environment called "100bitenv" that you can then activate with:
<code>conda activate 100bitenv</code>

If it worked, you should see (100bitenv) appear above each command you type. Finally, run the command:
<code>jupyter-notebook</code>

Jupyter-notebook should then open up the repository in your default browser, at which point you can find and open "100 Bit Crawler.ipynb" and "100 Bit Project.ipynb".

Tested with Python 3.8.8 on Windows 10. Unfortunately, I do not think the code will run well on non-windows systems, as the package webdriver-manager seems to be specific to Windows.
