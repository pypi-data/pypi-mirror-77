======
sourCy
======


.. image:: https://img.shields.io/pypi/v/sourcy.svg
        :target: https://pypi.python.org/pypi/sourcy

.. image:: https://img.shields.io/travis/SasCezar/sourcy.svg
        :target: https://travis-ci.com/SasCezar/sourcy

.. image:: https://readthedocs.org/projects/sourcy/badge/?version=latest
        :target: https://sourcy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


A library for NLP like preprocessing for source code in different programming languages.
The architecture follows the one of `spaCy`_.


* Free software: GNU General Public License v3
* Documentation: https://sourcy.readthedocs.io.

Features
--------

* **Grammar based parsing**
* **Multilanguage Support**

Usage
--------


To use sourCy in a project:

.. code-block:: python

    import sourcy

    code = """
            # This function computes the factor of the argument passed
            def print_factors(x):
                print("The factors of",x,"are:")

                for i in range(1, x + 1):
                    if x % i == 0:
                    print(i)

            num = 320

            print_factors(num)
            """

    # Creates a pipeline to process source code
    scp = sourcy.load("python")

    # Process the code and create a document with the tokens and the annotation
    doc = scp(code)

    for token in doc:
        print(token.token, token.annotation, token.block)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`spaCy`: https://github.com/explosion/spaCy