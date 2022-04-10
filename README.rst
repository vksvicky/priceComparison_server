===============
priceComparison
===============

.. image:: https://img.shields.io/badge/License-GPL3.0-yellow.svg?style=plastic
        :target: https://www.gnu.org/licenses
        :alt: License

.. image:: https://img.shields.io/travis/vksvicky/pricecomparison.svg?style=plastic
        :target: https://app.travis-ci.com/github/vksvicky/priceComparison
        :alt: CI Build

.. image:: https://readthedocs.org/projects/pricecomparison/badge/?style=plastic&version=latest
        :target: https://pricecomparison.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/github/issues/vksvicky/priceComparison?style=plastic
        :target: https://github.com/vksvicky/priceComparison/issues
        :alt: GitHub issues


Description
-----------

Compare high-street stores product price


Features
--------

* Basic feature to make sure screen scraping is working too retrieve product cost



TODO
====

[X] Update folder structure

[ ] TDD approach to the solution

[ ] Moduler solution

[ ] Update the Excel sheet(s) with required items

[X] Build CI pipeline - Travis

[X] Added Codacy Security Scan, CodeQL & Checkmarx CxFlow

[ ] Possibly deploy to Docker?

[ ] Get prices for each store working
        [X] Sainsburys
        [X] Tesco
        [ ] Co-op
        [ ] Ocado
        [ ] Morissons
        [ ] Lidl
        [ ] Asda
        [ ] M&S
        [ ] Aldi

[ ] Parallel process to retrieve product prices from each provider

[ ] Create a sheet in Excel to find the cheapest store for the listed products

[ ] Add quantity column for products

[ ] Add a column to state availability

[ ] Identify if the product is in stock and update excel cost accordingly

[ ] Identify offers if available and add relevant items update cost accordingly

[ ] Create a shopping list sheet and identify the cost

[ ] For the created shopping cart compare across the listed providers and find the cheapest and show the store name

[ ] Create a master sheet of stores for selection and a master sheet for products

[ ] Ability to create a shopping cart (in the format) + select a store

[ ] Ability to create a shopping cart (in the format) + select a stores + best price across selected stores

[ ] Add Petrol & Diesel prices for comparison for available Supermarkets
 
Phase 2
=======

[ ] Move excel data to a DB

[ ] Update code to update and read from DB

[ ] Create a ReactJS/NextJS/Flutter Web App, where a user would be able to select their product of choice and we should the cost across stores

[ ] Deploy app to a web-portal

[ ] Customer have their own profiles on the portal

[ ] Customer can create their own shopping list

[ ] Add Electric charger prices, source of prices?


Phase 3
=======

[ ] Customer can send their shopping list to their favourite TODO mobile app?

[ ] Ability for customer to get notification when product price goes up / down

[ ] Ability for customer to get notification of each week with the best priced store?

[ ] Ability for customer to add a favourite list to their profile

[ ] Customer upload bill to the system; OCR Scan the bill and suggest if there could have been a discount

[ ] Find coupons from Quidco

[ ] Find coupons from TopCashBack

[ ] If customer has coupons from Store, can we use it online?

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
