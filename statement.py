from math import floor


def statement(invoice, plays):

	def usd(aNumber):
		return f'${aNumber/100:.2f}'

	def playFor(aPerformance):
		return plays[aPerformance['playID']]

	def amountFor(aPerformance):
		result = 0
		if playFor(aPerformance)['type'] == 'tragedy':
			result = 40000
			if aPerformance['audience'] > 30:
				result += 1000 * (aPerformance['audience'] - 30)
		elif playFor(aPerformance)['type'] == 'comedy':
			result = 30000
			if aPerformance['audience'] > 20:
				result += 10000 + 500 * (aPerformance['audience'] - 20)
			result += 300 * aPerformance['audience']
		else:
			raise Exception(f"unknown type: {playFor(aPerformance)['type']}")
		return result

	def volumeCreditsFor(aPerformance):
		result = 0
		result += max(aPerformance['audience'] - 30, 0)
		if playFor(aPerformance)['type'] == "comedy":
			result += floor(aPerformance['audience'] / 5)
		return result
	
	def totalVolumeCredits():
		volumeCredits = 0
		for perf in invoice['performances']:
			volumeCredits += volumeCreditsFor(perf)
		return volumeCredits

	totalAmount = 0
	result = f"Statement for {invoice['customer']}\n"
	for perf in invoice['performances']:
		result += f" {playFor(perf)['name']}: {usd(amountFor(perf))} ({perf['audience']} seats)\n"
		totalAmount += amountFor(perf)

	volumeCredits = totalVolumeCredits()
	result += f'Amount owed is {usd(totalAmount)}\n'
	result += f'You earned {volumeCredits} credits\n'
	return result
