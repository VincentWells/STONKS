# import from DataGather?
years = range(2009, 2020)

quarters = ["q1", "q2", "q3", "q4"]

# Might be simpler to build SQL database and run query
all_data = []
tag_list = ["Revenues", "Assets", "AssetsCurrent", "AssestsNoncurrent", "Liabilities", "LiabilitiesCurrent", "LiabilitiesNoncurrent", "LongTermDebtCurrent"]

for year in years:
    for quarter in quarters:
        dir_addr = '../data/' + str(year) + quarter
        company_to_adsh = {}
        with open(dir_addr + '/sub.tsv', 'r', encoding='utf-8') as f:
            next(f)
            for _, line in enumerate(f):
                line_list = line.split('\t')
                # adsh column
                adsh = line_list[0]
                # name column
                name = line_list[2]
                company_to_adsh[adsh] = name
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

# write data to a single .csv file for easier use in TensorFlow & memoization
out_addr = "../data/output.csv"
with open (out_addr, 'w') as o:
    for i in range(0, len(years) * len(quarters)):
        for company in all_data[i]:
            line = [years[i // 4], quarters[i % 4], company.replace(',', ''), *all_data[i][company]]
            o.write(",".join(str(v) for v in line) + '\n')

