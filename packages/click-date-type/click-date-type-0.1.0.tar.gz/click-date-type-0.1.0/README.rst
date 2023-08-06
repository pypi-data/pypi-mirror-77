click-date-type
===============

Date type parameter for click

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install click-date-type

Usage
-----

.. code-block:: python

    from click_date_type import Date

    @click.command()
    @click.option("--start_date", type=Date())
    def cli(start_date):
        click.echo(start_date.strftime("%Y-%m-%d"))
