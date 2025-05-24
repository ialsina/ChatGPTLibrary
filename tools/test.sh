# Run all tests with coverage
pytest ..

# Run only unit tests
pytest -m unit ..

# Run tests without slow tests
pytest -m "not slow" ..

# Generate HTML coverage report
pytest --cov-report=html ..