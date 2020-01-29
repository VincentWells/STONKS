# import from DataGather?
years = range(2009, 2019)
quarters = ["q1", "q2", "q3", "q4"]
company_to_adsh = {}

# theory: don't need to read all sub.tsv files, just the last one, as long as no company has gone out of business
with open('../data/2019q3/sub.tsv', 'r') as f:
    for line in enumerate(f):
        line_list = line.split('\t')
        # adsh column
        adsh = line_list[0]
        # name column
        name = line_list[2]
        company_to_adsh[adsh] = name

# Might be simpler to build SQL database and run query
adsh_to_tab_value = {}
for year in years:
    for quarter in quarters:
        dir_addr = '../data/' + str(year) + quarter

        with open(dir_addr + '/num.tsv', 'wb') as f:
            for line in enumerate(f):
                line_list = line.split('\t')
                # adsh column
                adsh = line_list[0]
                # name column
                name = line_list[2]
                company_to_adsh[adsh] = name

