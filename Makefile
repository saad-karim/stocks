unit-tests:
	pytest --rootdir /Users/SaadK/Development/saad-karim/stocks -s --cache-clear .

test-coverage:
	pytest --cov=. --rootdir /Users/SaadK/Development/saad-karim/stocks --cov-report xml:cov.xml