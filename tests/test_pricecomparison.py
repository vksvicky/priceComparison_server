"""Tests for `pricecomparison` package."""

import pytest
import os


#  Test if file exists
def test_fileExists():
    fileName = "./tests/pricewatch.xls"
    fileExists = os.path.realpath(fileName)
    assert fileExists
