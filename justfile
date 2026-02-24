MANAGE := "python manage.py "

default:
	@just -l

setup:
	python3.12 -m venv .venv
	python -m pip install --upgrade pip
	pip install uv

install-requirements:
	uv pip install -r requirements.txt

install-pyproject:
	uv pip install -r pyproject.toml

serve:
	{{MANAGE}} runserver

migrate:
	{{MANAGE}} migrate


pre-commit:
	pre-commit run -a

run: serve
