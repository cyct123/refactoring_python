from functools import reduce
from math import floor


def statement(invoice, plays):

	def enrichPerformance(aPerformance):
		result = aPerformance.copy()
		result['play'] = playFor(result)
		result['amount'] = amountFor(result)
		result['volumeCredits'] = volumeCreditsFor(result)
		return result
	
	def playFor(aPerformance):
		return plays[aPerformance['playID']]
	
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
	
	def totalVolumeCredits(data):
		return reduce(lambda total, p: total + p['volumeCredits'], data['performances'], 0)
	
	def totalAmount(data):
		return reduce(lambda total, p: total + p['amount'], data['performances'], 0)

	statementData = {}
	statementData['customer'] = invoice['customer']
	statementData['performances'] = list(map(enrichPerformance ,invoice['performances']))
	statementData['totalAmount'] = totalAmount(statementData)
	statementData['totalVolumeCredits'] = totalVolumeCredits(statementData)
	return renderPlainText(statementData)

def renderPlainText(data):
	def usd(aNumber):
		return f'${aNumber/100:.2f}'

	result = f"Statement for {data['customer']}\n"
	for perf in data['performances']:
		result += f" {perf['play']['name']}: {usd(perf['amount'])} ({perf['audience']} seats)\n"
	result += f"Amount owed is {usd(data['totalAmount'])}\n"
	result += f"You earned {data['totalVolumeCredits']} credits\n"
	return result
