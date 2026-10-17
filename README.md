About
=====

A quick and relatively dirty script to upload your payslips to FranceTravail.
Their list is unsorted, changes every time you open it and the upload process takes several clicks. This script cares a lot less about that than I do.

WARNING
=======

This script worked for me. It may not work for you. For all I know, it may go on a rampage and end all of humanity if you try to run it. As soon as you use it, that becomes a _you_ problem. I offer no warranty of any kind.

The only thing I guarantee is that it is 100% human-written.

How to use it
=============

0. In your FranceTravail account, upload any documents that are not payslips. This script is not equipped to encounter any other documents and will probably show some unexpected behaviour if it does. This is your one and only warning.

1. Create a virtual env and install requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Make sure you have all of your payslips in a folder with the following structure:
   - `%Y`
     - `%m.%Y.pdf`

3. Call the script:
```bash
python3 ./upload.py --user "username" --password "password" --docs-path "/path/to/your/payslips"
```

Yes, you'll enter your login data in plaintext. This is a quick and dirty script, not a full-fledged application.

4. When it gets to two-factor auth, the script will stop and let you take care of that: select your preferred method of receiving the code, enter it, click "Poursuivre" and either option (trust the browser or not, it doesn't matter, the browser used by the script will reset itself). Then go back to the script and press Enter.

5. It will start clicking through the list of documents and uploading them one at a time. Every time, it will ask you to confirm that the document selected is the correct one; verify in the browser, go to the script and press Enter to confirm. If it's wrong, there's probably an issue with your document names. If you trust it and don't want to verify every time (I've heard better ideas, but it's your life, live it your way!), remove the `input` at line 120.

6. Once done, it will end abruptly and close the browser window it was using.

