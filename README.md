# phoronix trace

Tool to track what packages affect a pts benchmark

python dep_analyzer.py

The test suites that you want to run shoudl be a file in /var/lib/phoronix-test-suite/test-suites/local

The system will run a benchmark as :

phoronix-test-suite batch-benchmark local/<bench>

results/ will have the index.html and json files as well as logs
