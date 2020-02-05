# import from DataGather?
import datetime
years = range(2009, 2018)
quarter_names = ["q1", "q2", "q3", "q4"]


# Might be simpler to build SQL database and run queries
all_data = []
tag_list = ["Revenues", "Assets", "AssetsCurrent", "AssestsNoncurrent", "Liabilities", "LiabilitiesCurrent", "LiabilitiesNoncurrent", "LongTermDebtCurrent", "MarketCapitalization"]

print("* Parsing SEC database files")
for year in years:
    for quarter in quarter_names:
        dir_addr = '../data/' + str(year) + quarter
        company_to_adsh = {}
        with open(dir_addr + '/sub.tsv', 'r', encoding='utf-8') as f:
            next(f)
            for _, line in enumerate(f):
                line_list = line.split('\t')
                # adsh column
                adsh = line_list[0]
                # name column
                cik = line_list[1]
                company_to_adsh[adsh] = cik
        with open(dir_addr + '/num.tsv', 'r', encoding='utf-8', errors='ignore') as f:
            next(f)
            quarter_data = {}
            for _, line in enumerate(f):
                line_list = line.strip().split('\t')

                # tag column
                tag = line_list[1]
                # value column
                # TODO: remove decimal points and whatnot from this value
                val = line_list[8]

                name = company_to_adsh[line_list[0]]
                if tag in tag_list:
                    if name not in quarter_data:
                        quarter_data[name] = [0] * len(tag_list)
                    quarter_data[name][tag_list.index(tag)] = val
            all_data.append(quarter_data)

print("* Parsing cik to ticker file")
# Map CIK to ticker values from csv
cik_to_tickers = {}
with open("../data/cik_ticker.csv", 'r', encoding='utf-8') as c:
    next(c)
    for _, line in enumerate(c):
        line_list = line.split('|')
        # adsh column
        cik = line_list[0]
        # name column
        ticker = line_list[1]
        cik_to_tickers[cik] = ticker

# Read market cap data from alternate datasets


def get_qtr_avgs(company_name):
    # Q1 2009 is empty
    avg_list = [0]
    cutoff = datetime.date(2009, 7, 1)
    start = datetime.date(2009, 4, 1)
    file_name = "../kaggle_dataset/price-volume-data-for-all-us-stocks-etfs/Stocks/" + company_name + ".us.txt"
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            next(f)
            qtr_highs = []
            for _, line in enumerate(f):
                line_list = line.strip().split(',')
                date_fields = [int(x) for x in line_list[0].split('-')]
                date = datetime.date(*date_fields)
                close = float(line_list[4])

                if date > cutoff:
                    if len(qtr_highs) == 0:
                        avg_list.append(0)
                    else:
                        avg_list.append(sum(qtr_highs) / len(qtr_highs))
                    qtr_highs = [close]
                    start = cutoff
                    if cutoff.month == 10:
                        cutoff = cutoff.replace(month=1, year=cutoff.year + 1)
                    else:
                        cutoff = cutoff.replace(month=cutoff.month + 3)
                elif date > start:
                    qtr_highs.append(close)
        return avg_list
    except (FileNotFoundError, StopIteration):
        return [0]*40


print("* Parsing Kaggle stock price data")
company_qtr_price_dict = {}
# TODO: remove calls to companies not in Kaggle dataset
for cik in cik_to_tickers:
    company_qtr_price_dict[cik_to_tickers[cik]] = get_qtr_avgs(cik_to_tickers[cik])

# write data to a single .csv file for easier use in TensorFlow & memoization
print("* Writing to output.csv")
out_addr = "../data/output.csv"
with open (out_addr, 'w') as o:
    for i in range(0, (len(years) - 1)* len(quarter_names)):
        for cik in all_data[i]:
            try:
                ticker = cik_to_tickers[cik]
                tag_results = all_data[i][cik]
                company_qtr_price = company_qtr_price_dict[ticker][i]
                future_qtr_price = company_qtr_price_dict[ticker][i + 4]
                company_qtr_price = 0
                line = [years[i // 4], quarter_names[i % 4], ticker, *tag_results, company_qtr_price, future_qtr_price]
                o.write(",".join(str(v) for v in line) + '\n')
            except (KeyError, TypeError, IndexError):
                continue
