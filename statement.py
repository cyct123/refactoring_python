from createStatementData import createStatementData


def statement(invoice, plays):
	return renderPlainText(createStatementData(invoice, plays))

def renderPlainText(data):
	def usd(aNumber):
		return f'${aNumber/100:.2f}'

	result = f"Statement for {data['customer']}\n"
	for perf in data['performances']:
		result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
	result += f"Amount owed is {usd(data['totalAmount'])}\n"
	result += f"You earned {data['totalVolumeCredits']} credits\n"
	return result
