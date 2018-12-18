# Dep-Analizer

Tool to track what packages affect a phoronix test suite benchmark


### Prerequisites

    * Python 3
    * Phoronix test suite
    * strace

### How to use it

python dep_analyzer.py

The test suites that you want to run shoudl be a file in:

    /var/lib/phoronix-test-suite/test-suites/local

The system will run a benchmark as :

phoronix-test-suite batch-benchmark local/<bench>

The directory results/ will have the index.html and json files as well as log
directory with the results of strace


## Contributing

Please read
[CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for
details on our code of conduct, and the process for submitting pull requests to
us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Victor Rodriguez** - *Initial work* -
  [Victor Rodriguez](https://github.com/VictorRodriguez)

* **Abraham Duenas** - *Initial work* -
  [Abraham Duenas](https://github.com/aduenasd)

  ## License

  This project is licensed under the MIT License - see the
  [LICENSE.md](LICENSE.md) file for details

  ## Acknowledgments

  * Hat tip to anyone whose code was used
  * Inspiration
  * etc


