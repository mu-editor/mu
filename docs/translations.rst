Internationalisation of Mu
==========================

Create a New Translation
------------------------

If you want to translate mu to your language, you should goto:;

   mou/locale/es/LC_MESSAGES 

You will find mu.po file, and the text mu used are stored in this file in plain text. 
You need to deal with this file if you want to translate mu to you native language.

The po file is convenient for human to read but mu can't, you need covert .po file 
to binary .mo file, so you nedd to download poeditor to edit the .po file, it's really
a good tools. https://poedit.net/

Step 1:
Create a folder under ```locale```, then create a sub-folder named ```LC_MESSAGES``` 
under the folder you created.For ex, i create zh_CN folder under locale.

Step 2:
Copy mu.po file under the default es/LC_MESSAGES folder to ```YOU_LANGUAGE/LC_MESSAGES``` 
you created.

Step 3:
Open the mo file under ```OU_LANGUAGE/LC_MESSAGES/mu.mo``` use poeditor,translate 
Englist text to your language.

Step 4:
Afer translation, slect poeditor File|complie to mo|, and save the .mo file to the same 
dir of .po file.

Step 5:
	current_locale, encoding = locale.getdefaultlocale()
	language_code = current_locale[:2] # if not work change this line
	gettext.translation('mu', localedir=localedir,
						languages=[language_code], fallback=True).install()

Step 6:
Restart Mu, and Mu editor is in your native language now.






