INSTALL_DIR:=${HOME}/.local/bin

install:
	sed '1i#!/usr/bin/env python3' jisho.py > ${INSTALL_DIR}/jisho
	chmod +x ${INSTALL_DIR}/jisho
