# Project_Butler

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