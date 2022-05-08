from xml.sax.saxutils import escape
import pandas as pd
import requests

csv_filename = 'vouchers.csv'
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
					<ID>Vouchers</ID>
				</HEADER>
				<BODY>
					<DESC>
						<STATICVARIABLES>
							<IMPORTDUPS>@@DUPIGNORE</IMPORTDUPS>
						</STATICVARIABLES>
					</DESC>
				<DATA>\n"""

def convert_row(row):
	if row.voucher_type == 'Receipt' or row.voucher_type == 'Purchase' or row.voucher_type == 'Contra' or row.voucher_type == 'Credit Note': return (f"""<TALLYMESSAGE><VOUCHER VCHTYPE='{escape(row.voucher_type)}' ACTION='Create'><VOUCHERTYPENAME>{escape(row.voucher_type)}</VOUCHERTYPENAME><DATE>{row.entry_date}</DATE><REFERENCEDATE>{row.invoice_date}</REFERENCEDATE><PARTYLEDGERNAME>{escape(row.dr_ledger)}</PARTYLEDGERNAME><NARRATION>{escape(row.naration)}</NARRATION><REFERENCE>{escape(row.supplier_invoice_no)}</REFERENCE><VOUCHERNUMBER></VOUCHERNUMBER><ALLLEDGERENTRIES.LIST><REMOVEZEROENTRIES>No</REMOVEZEROENTRIES><LEDGERFROMITEM>No</LEDGERFROMITEM><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE><LEDGERNAME>{escape(row.dr_ledger)}</LEDGERNAME><AMOUNT>{row.amount}</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST><REMOVEZEROENTRIES>No</REMOVEZEROENTRIES><LEDGERFROMITEM>No</LEDGERFROMITEM><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><LEDGERNAME>{escape(row.cr_ledger)}</LEDGERNAME><AMOUNT>-{row.amount}</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER></TALLYMESSAGE>""")
	elif row.voucher_type == 'Sales' or row.voucher_type == 'Payment' or row.voucher_type == 'Journal' or row.voucher_type == 'Debit Note': return (f"""<TALLYMESSAGE><VOUCHER VCHTYPE='{escape(row.voucher_type)}' ACTION='Create'><VOUCHERTYPENAME>{escape(row.voucher_type)}</VOUCHERTYPENAME><DATE>{row.entry_date}</DATE><REFERENCEDATE>{row.invoice_date}</REFERENCEDATE><PARTYLEDGERNAME>{escape(row.dr_ledger)}</PARTYLEDGERNAME><NARRATION>{escape(row.naration)}</NARRATION><REFERENCE>{escape(row.supplier_invoice_no)}</REFERENCE><VOUCHERNUMBER></VOUCHERNUMBER><ALLLEDGERENTRIES.LIST><REMOVEZEROENTRIES>No</REMOVEZEROENTRIES><LEDGERFROMITEM>No</LEDGERFROMITEM><ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE><LEDGERNAME>{escape(row.dr_ledger)}</LEDGERNAME><AMOUNT>-{row.amount}</AMOUNT></ALLLEDGERENTRIES.LIST><ALLLEDGERENTRIES.LIST><REMOVEZEROENTRIES>No</REMOVEZEROENTRIES><LEDGERFROMITEM>No</LEDGERFROMITEM><ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE><LEDGERNAME>{escape(row.cr_ledger)}</LEDGERNAME><AMOUNT>{row.amount}</AMOUNT></ALLLEDGERENTRIES.LIST></VOUCHER></TALLYMESSAGE>""")

xml_op += '\n'.join(df.apply(convert_row, axis=1))

xml_op += """</DATA>
			</BODY>
		</ENVELOPE>\n"""

print(xml_op)

print('======')

response = requests.post(url,data=xml_op, headers=headers)

print(response.text)
