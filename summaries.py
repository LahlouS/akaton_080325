import numpy as np
import pandas as pd

# Lets sum-up our continuous variables
def continuous_variable_summary(df, col_name):
	mean = []
	var = []
	std = []
	min_vals = []
	max_vals = []
	med = []

	for col in col_name:
		mean.append(df[col].mean())
		var.append(df[col].var())
		std.append(df[col].std())
		min_vals.append(df[col].min())
		max_vals.append(df[col].max())
		med.append(df[col].median())

	summary = pd.DataFrame({
		"mean": mean,
		"median": med,
		"variance": var,
		"std_dev": std,
		"min": min_vals,
		"max": max_vals
	}, index=col_name)

	return summary

def check_null_ish_values(df):
	null_counts = df.isnull().sum()  # NaN or None values
	empty_string_counts = (df == "").sum()  # Empty strings
	custom_nulls = ["unknown", "N/A", "na"]  # Add your specific "null-ish" values here
	custom_counts = {val: (df == val).sum() for val in custom_nulls}

	# Combine results into a DataFrame
	summary = pd.DataFrame({
		"Nulls": null_counts,
		"Empty Strings": empty_string_counts,
		**{f"Custom ({val})": count for val, count in custom_counts.items()}
	})
	
	return summary