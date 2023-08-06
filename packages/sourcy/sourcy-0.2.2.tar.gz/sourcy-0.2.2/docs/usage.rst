=====
Usage
=====

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

