from math import floor
import locale


def statement(invoice, plays):
	totalAmount = 0
	volumeCredits = 0
	result = f"Statement for {invoice['customer']}\n"
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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

	for perf in invoice['performances']:
		
		volumeCredits += max(perf['audience'] - 30, 0)
		if playFor(perf)['type'] == "comedy":
			volumeCredits += floor(perf['audience'] / 5)

		result += f" {playFor(perf)['name']}: {locale.currency(amountFor(perf) / 100)} ({perf['audience']} seats)\n"
		totalAmount += amountFor(perf)
	result += f'Amount owed is {locale.currency(totalAmount / 100)}\n'
	result += f'You earned {volumeCredits} credits\n'
	return result
