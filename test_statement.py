import json
import pytest
from statement import statement


# Arrange
@pytest.fixture
def invoice():
	with open("invoices.json", 'r') as f:
		invoices = json.load(f)
	return invoices[0]

@pytest.fixture
def plays():
	with open("plays.json", 'r') as f:
		return json.load(f)

def test_statement(invoice, plays):
	assert statement(invoice, plays) == "Statement for BigCo\n"\
	" Hamlet: $650.00 (55 seats)\n"\
	" As You Like It: $580.00 (35 seats)\n"\
	" Othello: $500.00 (40 seats)\n"\
	"Amount owed is $1730.00\n"\
	"You earned 47 credits\n"
