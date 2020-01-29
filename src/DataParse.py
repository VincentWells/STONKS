# import from DataGather?
years = range(2009, 2019)
quarters = ["q1", "q2", "q3", "q4"]

# Might be simpler to build SQL database and run query
all_data = []
tag_list = []
for year in years:
    for quarter in quarters:
        dir_addr = '../data/' + str(year) + quarter
        company_to_adsh = {}
        with open(dir_addr + '/sub.tsv', 'r') as f:
            next(f)
            for line in enumerate(f):
                line_list = line.split('\t')
                # adsh column
                adsh = line_list[0]
                # name column
                name = line_list[2]
                company_to_adsh[adsh] = name
        with open(dir_addr + '/num.tsv', 'r') as f:
            next(f)
            quarter_data = {}
            for line in enumerate(f):
                line_list = line.split('\t')

                # tag column
                tag = line_list[1]
                # value column
                # TODO: remove decimal points and whatnot from this value
                val = line_list[8]

                name = company_to_adsh[line_list[0]]
                if tag in tag_list:
                    if name in quarter_data:
                        quarter_data[name] = [0] * len(tag_list)
                    quarter_data[name][tag_list.index(tag)] = val
            all_data.append(quarter_data)




