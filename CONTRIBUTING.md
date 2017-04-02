Contributing
============

Contributions are welcome, please take a look at the [issues list](https://github.com/nicoulaj/rainbow/issues).

This project uses a standard layout. Here are some example steps to setup
your development environment using [pew](https://github.com/berdario/pew):

1. Checkout project sources:

        git clone https://github.com/nicoulaj/rainbow.git
        cd rainbow

2. Create a virtual environment for rainbow:

        pew new rainbow

3. Install rainbow build dependencies:

        pip install -r requirements-build.txt -r requirements-test.txt

4. To run tests, rainbow uses [tox](https://tox.readthedocs.io):

        tox

   This will run all the tests, for all python versions. To run tests for
   one specific version:

        tox -e py27

   After you run tests, results (test, coverage and benchmark HTML reports) will be available in the `build/tests` directory.
