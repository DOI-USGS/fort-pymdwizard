<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="/">
    <html>
      <body>
        <h2 ALIGN="Center">MP Metadata Validation Report</h2>
        <h4 ALIGN="Center">
          <xsl:value-of select="concat('File: ', report/info/@input_file)" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" />
        </h4>
        <h5 ALIGN="Center">
          <xsl:value-of select="concat('Run at: ', report/info/@process_date, &quot; ,  &quot;, report/info/@process_time)" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"></xsl:value-of>
        </h5>
        <hr />
        <h3>Errors:</h3>
          <xsl:for-each select="report/error">
            <ul></ul>
            <li>
            <xsl:value-of select="." />
              <b>
                  <font color="#F70D1A">
                      <li />
                      <xsl:value-of select="concat(' xpath: ', @xpath)" />
                  </font>
              </b>
            </li>
          </xsl:for-each>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>