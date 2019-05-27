from tavern.core import run

success = run("test_server2.tavern.yaml")

if not success:
    print("Error running tests")