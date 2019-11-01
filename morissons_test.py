#!/usr/bin/env python
import pandas as pd
import numpy as np 
import math
import argparse
import os
from decimal import Decimal
from datetime import datetime

#checks the the 7 digit number and transforms it into GTIN-8 code
def check_digit(input_mf):
	GTIN = str(input_mf)
	P1=int(GTIN[0])
	P2=int(GTIN[1])
	P3=int(GTIN[2])
	P4=int(GTIN[3])
	P5=int(GTIN[4])
	P6=int(GTIN[5])
	P7=int(GTIN[6])
	#calculates the last digit
	GTINT=int(P1*3+P2+P3*3+P4+P5*3+P6+P7*3)
	roundup=round(GTINT, -1)
	GTIN8=int(roundup-GTINT) % 10
	#turns the seven digit code into an 8 digit code by adding the earlier calculated number at the back
	modified_mf_element = str(GTIN)+str(GTIN8)
	return modified_mf_element

def format_report(filename, output_dir):

	#reads the file specified in argument filename
	original_morrisons_dataframe = pd.read_csv(filename)
	#sorts the data by MF_CODE
	sorted_morrisons_dataframe = original_morrisons_dataframe.sort_values(by=["MF_CODE"], axis = 0, ascending = True, na_position ="last")
	#filters out all the rows that don't have MF_CODE
	filtered_df = sorted_morrisons_dataframe[sorted_morrisons_dataframe['MF_CODE'].notnull()]
	#swaps the columns around in the filtered out data
	renamed_df = filtered_df.rename(columns ={"MF_CODE" : "MIN", "MIN" : "MF_CODE"})
	#reindexes the two earlier changed columns 
	cols = list(renamed_df.columns)
	a, b = cols.index('MF_CODE'), cols.index('MIN')
	#swaps the columns around 
	cols[b], cols[a] = cols[a], cols[b]
	renamed_df = renamed_df[cols]
	#gets rid of .0 at the end of all the MIN values
	renamed_df["MIN"] = renamed_df["MIN"].apply(lambda x: int(Decimal(x).normalize()))
	#pads out to seven digits with zeros
	renamed_df["MIN"] = renamed_df["MIN"].apply(lambda x: '{0:0>7}'.format(x))
	#adds the GTIN digit at the end of data
	renamed_df["MIN"] = renamed_df['MIN'].map(lambda mf_element: check_digit(mf_element))
	#merges the filtered out and edited data with the original data
	merged_df =sorted_morrisons_dataframe.append(renamed_df, sort = False)
	#checks todays date and then adds it to the title of the newely created report
	datestring = datetime.strftime(datetime.now(), '%Y-%m-%d')
	full_output_path = os.path.join(output_dir,'Bot_Report_' + datestring + ".csv")
	#creates new csv file
	merged_df.to_csv(full_output_path)

def main():
	
	parser = argparse.ArgumentParser(description="Morrisons report formating script")
	parser.add_argument("-f", "--filename", required=True, help="Path to file to be formated")
	parser.add_argument("-o", "--output_dir", required=True, help="Path to where the file will be saved")
	args = parser.parse_args()
	format_report(args.filename, args.output_dir)


if __name__ == '__main__': 
    main()
