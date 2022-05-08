from xml.sax.saxutils import escape
import pandas as pd
import requests

csv_filename = 'masters.csv'
url = 'http://10.251.74.65:9000'
headers = {"Content-type": "text/xml;charset=UTF-8", "Accept": "text/xml"}


with open(csv_filename, 'r') as f:
    df = pd.read_csv(f, header=0, index_col=False)
    print(df)

# add helper method for converting column names to lower case and replacing spaces with underscores
df.columns = [c.lower().replace(' ', '_').replace('/','_') for c in df.columns]
print(df.columns)

xml_op = """<ENVELOPE>
				<HEADER>
					<VERSION>1</VERSION>
					<TALLYREQUEST>Import</TALLYREQUEST>
					<TYPE>Data</TYPE>
					<ID>All Masters</ID>
				</HEADER>
				<BODY>
					<DESC>
						<STATICVARIABLES>
							<IMPORTDUPS>@@DUPIGNORE</IMPORTDUPS>
						</STATICVARIABLES>
					</DESC>
				<DATA>
				<TALLYMESSAGE>\n"""

def convert_row(row):
	return (f"""<LEDGER NAME='{escape(row.ledger_name)}' ACTION='Create'>
         <ADDRESS.LIST TYPE="String">
					<ADDRESS>{escape(row.address_a)}</ADDRESS>
					<ADDRESS>{escape(row.address_b)}</ADDRESS>
					<ADDRESS>{escape(row.address_c)}</ADDRESS>
					<ADDRESS>{escape(row.address_d)}</ADDRESS>
				</ADDRESS.LIST>
				<NAME>{escape(row.ledger_name)}</NAME>
				<PARENT>{escape(row.group)}</PARENT>
				<OPENINGBALANCE>{row.opening_balance}</OPENINGBALANCE>
				<LEDSTATENAME>{escape(row.state)}</LEDSTATENAME>
      	<ISBILLWISEON>{escape(row.maintain_bill_by_bill)}</ISBILLWISEON>
				<GSTREGISTRATIONTYPE>{escape(row.gst_registration_type)}</GSTREGISTRATIONTYPE>
				<ISGSTAPPLICABLE>{escape(row.is_gst_applicable)}</ISGSTAPPLICABLE>
				<PARTYGSTIN>{escape(row.party_gstin)}</PARTYGSTIN>
				<COUNTRYNAME>{escape(row.country)}</COUNTRYNAME>
				<COUNTRYOFRESIDENCE>{escape(row.country)}</COUNTRYOFRESIDENCE>
				</LEDGER>""")


xml_op += '\n'.join(df.apply(convert_row, axis=1))

xml_op += """</TALLYMESSAGE>
				</DATA>
			</BODY>
		</ENVELOPE>\n"""

print(xml_op)

print('======')

response = requests.post(url,data=xml_op, headers=headers)

print(response.text)

