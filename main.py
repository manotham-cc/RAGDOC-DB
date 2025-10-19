from ragsql.summary import get_summary
def main():

	# Allow question via env, arg, or interactive input
	question =  None
	if not question:
		try:
			# interactive
			question = input("Enter your natural-language question: ")
		except EOFError:
			print("No question provided. Exiting.")
			return

	response, sql = get_summary(question)
	print("\n--- USER-FACING SUMMARY ---\n")
	print(response)
	print("\n--- GENERATED SQL ---\n")
	print(sql)


if __name__ == "__main__":
	main()

