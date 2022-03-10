from createStatementData import createStatementData


def usd(aNumber):
	return f'${aNumber/100:.2f}'

def statement(invoice, plays):
	return renderPlainText(createStatementData(invoice, plays))

def renderPlainText(data):

	result = f"Statement for {data['customer']}\n"
	for perf in data['performances']:
		result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
	result += f"Amount owed is {usd(data['totalAmount'])}\n"
	result += f"You earned {data['totalVolumeCredits']} credits\n"
	return result

def htmlStatement(invoice, plays):
	return renderHtml(createStatementData(invoice, plays))

def renderHtml(data):
	result = f"<h1>Statement for {data['customer']}</h1>\n"
	result += "<table>\n"
	result += "<tr><th>play</th><th>seats</th><th>cost</th></tr>"
	for perf in data['performances']:
		result += f"  <tr><td>{perf['play']['name']}</td><td>{perf['audience']}</td>"
		result += f"<td>{usd(perf['amount'])}</td></tr>\n"
	result += "</table>\n"
	result += f"<p>Amount owed is <em>{usd(data['totalAmount'])}</em></p>\n"
	result += f"<p>You earned <em>{data['totalVolumeCredits']}</em> credits</p>\n"
	return result
