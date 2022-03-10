from math import floor


def statement(invoice, plays):

	def enrichPerformance(aPerformance):
		result = aPerformance.copy()
		result['play'] = playFor(result)
		return result
	
	def playFor(aPerformance):
		return plays[aPerformance['playID']]
	
	statementData = {}
	statementData['customer'] = invoice['customer']
	statementData['performances'] = list(map(enrichPerformance ,invoice['performances']))
	return renderPlainText(statementData, plays)

def renderPlainText(data, plays):
	def usd(aNumber):
		return f'${aNumber/100:.2f}'

	def amountFor(aPerformance):
		result = 0
		if aPerformance['play']['type'] == 'tragedy':
			result = 40000
			if aPerformance['audience'] > 30:
				result += 1000 * (aPerformance['audience'] - 30)
		elif aPerformance['play']['type'] == 'comedy':
			result = 30000
			if aPerformance['audience'] > 20:
				result += 10000 + 500 * (aPerformance['audience'] - 20)
			result += 300 * aPerformance['audience']
		else:
			raise Exception(f"unknown type: {aPerformance['play']['type']}")
		return result

	def volumeCreditsFor(aPerformance):
		result = 0
		result += max(aPerformance['audience'] - 30, 0)
		if aPerformance['play']['type'] == "comedy":
			result += floor(aPerformance['audience'] / 5)
		return result
	
	def totalVolumeCredits():
		result = 0
		for perf in data['performances']:
			result += volumeCreditsFor(perf)
		return result
	
	def totalAmount():
		result = 0
		for perf in data['performances']:
			result += amountFor(perf)
		return result

	result = f"Statement for {data['customer']}\n"
	for perf in data['performances']:
		result += f" {perf['play']['name']}: {usd(amountFor(perf))} ({perf['audience']} seats)\n"
	result += f'Amount owed is {usd(totalAmount())}\n'
	result += f'You earned {totalVolumeCredits()} credits\n'
	return result
