.PHONY: build check serve import-medium publish

PYTHON ?= python3
MESSAGE ?= Update journal

build:
	$(PYTHON) build.py

check:
	$(PYTHON) -m py_compile build.py import_medium.py
	$(PYTHON) build.py
	git diff --check

serve: build
	$(PYTHON) -m http.server 4173

import-medium:
	@test -f /tmp/arshad-medium.xml || (echo "Missing /tmp/arshad-medium.xml"; exit 1)
	$(PYTHON) import_medium.py
	$(PYTHON) build.py

publish: check
	git add .
	git commit -m "$(MESSAGE)"
	git push origin main