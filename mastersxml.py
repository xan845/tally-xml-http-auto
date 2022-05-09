from escapexml import escape
import pandas as pd

def convert_masters_row(row):
	return (f"""
                <LEDGER NAME='{escape(row.ledger_name)}' ACTION='Create'>
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
                </LEDGER>
""")

def mastersxml(filename):
    xml_op = """
<ENVELOPE>
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
            <TALLYMESSAGE>
"""
    df = pd.read_csv(str(filename))
    df.columns = [c.lower().replace(' ', '_').replace('/','_') for c in df.columns]
    print(df.shape)
    print(df.columns)
    xml_op += '\n'.join(df.apply(convert_masters_row, axis=1))
    xml_op += """
            </TALLYMESSAGE>
        </DATA>
    </BODY>
</ENVELOPE>
"""
    return xml_op
