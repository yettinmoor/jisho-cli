install:
	cp jint.py /usr/local/bin/jint
	cp jisho.py /usr/local/bin/
	echo 'python /usr/local/bin/jisho.py "$$@"' > /usr/local/bin/jisho
	chmod 755 /usr/local/bin/jisho
	chmod 755 /usr/local/bin/jint

uninstall:
	rm /usr/local/bin/{jint,jisho*}
