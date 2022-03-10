import json
import pytest
from statement import statement, htmlStatement


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

def test_plain_statement(invoice, plays):
	assert statement(invoice, plays) == "Statement for BigCo\n"\
	" Hamlet: $650.00 (55 seats)\n"\
	" As You Like It: $580.00 (35 seats)\n"\
	" Othello: $500.00 (40 seats)\n"\
	"Amount owed is $1730.00\n"\
	"You earned 47 credits\n"

def test_html_statement(invoice, plays):
	assert htmlStatement(invoice, plays) == "<h1>Statement for BigCo</h1>\n"\
	"<table>\n"\
	"<tr><th>play</th><th>seats</th><th>cost</th></tr>"\
	"  <tr><td>Hamlet</td><td>55</td>"\
	"<td>$650.00</td></tr>\n"\
	"  <tr><td>As You Like It</td><td>35</td>"\
	"<td>$580.00</td></tr>\n"\
	"  <tr><td>Othello</td><td>40</td>"\
	"<td>$500.00</td></tr>\n"\
	"</table>\n"\
	"<p>Amount owed is <em>$1730.00</em></p>\n"\
	"<p>You earned <em>47</em> credits</p>\n"
