def pytest_configure(config):
    config.addinivalue_line("markers", "integration: starts local servers and a headless browser")
