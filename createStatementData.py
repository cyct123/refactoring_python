from functools import reduce
from math import floor


class PerformanceCalculator:

	def __init__(self, aPerformance, aPlay) -> None:
		self.performance = aPerformance
		self.play = aPlay

	@property
	def amount(self):
		result = 0
		if self.play['type'] == 'tragedy':
			result = 40000
			if self.performance['audience'] > 30:
				result += 1000 * (self.performance['audience'] - 30)
		elif self.play['type'] == 'comedy':
			result = 30000
			if self.performance['audience'] > 20:
				result += 10000 + 500 * (self.performance['audience'] - 20)
			result += 300 * self.performance['audience']
		else:
			raise Exception(f"unknown type: {self.play['type']}")
		return result


def createStatementData(invoice, plays):

	def enrichPerformance(aPerformance):
		calculator = PerformanceCalculator(aPerformance, playFor(aPerformance))
		result = aPerformance.copy()
		result['play'] = calculator.play
		result['amount'] = calculator.amount
		result['volumeCredits'] = volumeCreditsFor(result)
		return result
	
	def playFor(aPerformance):
		return plays[aPerformance['playID']]
	
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
	return statementData
