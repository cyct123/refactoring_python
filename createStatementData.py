from functools import reduce
from math import floor


class PerformanceCalculator:

	def __init__(self, aPerformance, aPlay) -> None:
		self.performance = aPerformance
		self.play = aPlay

	@property
	def amount(self):
		raise NotImplementedError("subclass responsibility")

	@property
	def volumeCredits(self):
		return max(self.performance['audience'] - 30, 0)

class TragedyCalculator(PerformanceCalculator):

	@property
	def amount(self):
		result = 40000
		if self.performance['audience'] > 30:
			result += 1000 * (self.performance['audience'] - 30)
		return result

class ComedyCalculator(PerformanceCalculator):

	@property
	def amount(self):
		result = 30000
		if self.performance['audience'] > 20:
			result += 10000 + 500 * (self.performance['audience'] - 20)
		result += 300 * self.performance['audience']
		return result

	@property
	def volumeCredits(self):
		return super().volumeCredits + floor(self.performance['audience'] / 5)

def createPerformancCalculator(aPerformance, aPlay):
	if aPlay['type'] == 'tragedy':
		return TragedyCalculator(aPerformance, aPlay)
	elif aPlay['type'] == 'comedy':
		return ComedyCalculator(aPerformance, aPlay)
	else:
		raise Exception(f"unknown type: {aPlay['type']}")

def createStatementData(invoice, plays):

	def enrichPerformance(aPerformance):
		calculator = createPerformancCalculator(aPerformance, playFor(aPerformance))
		result = aPerformance.copy()
		result['play'] = calculator.play
		result['amount'] = calculator.amount
		result['volumeCredits'] = calculator.volumeCredits
		return result
	
	def playFor(aPerformance):
		return plays[aPerformance['playID']]
	
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
