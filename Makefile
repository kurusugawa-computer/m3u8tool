.PHONY: docs lint test format test publish_test publish

publish_test:
	rm -fr build/ dist/ m3u8tool.egg-info
	pipenv run python setup.py check --strict
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --repository-url https://test.pypi.org/legacy/ --verbose

publish:
	rm -fr build/ dist/ m3u8tool.egg-info
	pipenv run python setup.py check --strict
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --repository-url https://upload.pypi.org/legacy/ --verbose

