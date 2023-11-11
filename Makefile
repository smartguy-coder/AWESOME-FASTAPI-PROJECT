# poetry https://habr.com/ru/articles/593529/
#        https://python-poetry.org/docs/basic-usage/

.PHONY: build-win
build-win:
	python.exe -m pip install --upgrade pip
	pip install poetry
	poetry config --local virtualenvs.in-project true
	touch README.md
	poetry init -n
	poetry install


.PHONY: build-unix
build-unix:
	python3 -m pip install --upgrade pip
	pip3 install poetry
	poetry config --local virtualenvs.in-project true
	touch README.md
	poetry init -n
	poetry install


.PHONY: install
install:
	# make install package='fastapi[all]'
	poetry add ${package}
	poetry install


.PHONY: install-dev
install-dev:
	# make install-dev package='pytest'
	poetry add ${package} --dev
	poetry install
# cat requirements.txt | xargs poetry add
