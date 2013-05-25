**Here is new, more powerful plugin for lint your Python files: [github.com/dreadatour/Flake8Lint](https://github.com/dreadatour/Flake8Lint)**

**Flake8Lint includes pep8 lind and pyflakes lint - please, use it.**

Pep8Lint
=========

Pep8Lint is a Sublime Text 2 plugin for check Python files against some of the style conventions in **[PEP8](http://www.python.org/dev/peps/pep-0008/)**.

Based on **[github.com/jcrocholl/pep8](https://github.com/jcrocholl/pep8)**.

Install
-------

Download the latest source from [GitHub](https://github.com/dreadatour/Pep8Lint/zipball/master) and copy *Pep8Lint* folder to your ST2 "Packages" directory.

Or clone the repository to your ST2 "Packages" directory:

    git clone git://github.com/dreadatour/Pep8Lint.git


The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/

Config
------

Default Pep8Lint config: "Preferences" -> "Package Settings" -> "Pep8Lint" -> "Settings - Default"

	{
		// run pep8 lint on file saving
		"lint_on_save": true,
		// set maximum line length
		"max-line-length": 79,
		// select errors and warnings (e.g. ["E", "W6"])
		"select": [],
		//skip errors and warnings (e.g. ["E303", E4", "W"])
		"ignore": [],

		// Visual settings

		// display popup with errors
		"popup": true,
		// highlight errors
		"highlight": false
	}


To change default settings, go to "Preferences" -> "Package Settings" -> "Pep8Lint" -> "Settings - User" and paste default config to opened file.

Features / Usage
----------------

Automatically check Python files with pep8 lint tool and show window with error list:

[![Error list](http://habrastorage.org/storage2/5ac/5f2/ded/5ac5f2ded857d962d1ca78da087a65f7.png)](http://habrastorage.org/storage2/5ac/5f2/ded/5ac5f2ded857d962d1ca78da087a65f7.png)

And move to error line/char on select.
