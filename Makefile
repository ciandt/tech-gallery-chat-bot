#!/usr/bin/make -f
# -*- makefile -*-

deps:
	@pip install --no-cache -q -r requirements-dev.txt

clean:
	@echo "Cleaning..."
	@find . -name '*.py[cod]' -delete
	@find . -name '*.so' -delete
	@find . -name '.coverage' -delete
	@find . -name __pycache__ -delete
	@rm -rf *.egg-info *.log build dist MANIFEST
	@rm -rf htmlcov
	@coverage erase

tests:
	@python -m pytest tests

coverage:
	@python -m pytest --cov=tech_gallery_bot --cov-report=term --cov-report=html tests

format:
	@python -m black --target-version=py37 *.py tech_gallery_bot tests

run:
	@python main.py

.PHONY:	deps clean tests coverage format run
