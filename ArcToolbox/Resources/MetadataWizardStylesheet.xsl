<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <!-- An xsl template for displaying metadata in ArcInfo8 with the
     traditional FGDC look and feel created by mp
	
     Revision History:   Created 6/7/99 avienneau
                       Modified 8/29/02 dave rugg - XSL 1.0 update
                       Modified 8/15/03 dave rugg - NBII elements
                       Modified 3/2/05 dave rugg - deal with some Unicode display issues
                       Modified 11/19/2008 Colin Talbert - added in template 'prewrap' to preserve whitespace in text fields
                       Modified 11/19/2008 Colin Talbert - added in template 'write_date' to format date fields in a mm/dd/yyyy format
-->
  <xsl:template match="/">
    <html>
      <body>
        <a name="Top" />
        <h1>
          <xsl:value-of select="metadata/idinfo/citation/citeinfo/title" />
        </h1>
        <h2>Metadata:</h2>
        <ul>
          <xsl:for-each select="metadata/idinfo">
            <li>
              <a href="#Identification Information">Identification Information</a>
            </li>
          </xsl:for-each>
          <xsl:for-each select="metadata/dataqual">
            <li>
              <a href="#Data Quality Information">Data Quality Information</a>
            </li>
          </xsl:for-each>
          <xsl:for-each select="metadata/spdoinfo">
            <li>
              <a href="#Spatial Data Organization Information">Spatial Data Organization Information</a>
            </li>
          </xsl:for-each>
          <xsl:for-each select="metadata/spref">
            <li>
              <a href="#Spatial Reference Information">Spatial Reference Information</a>
            </li>
          </xsl:for-each>
          <xsl:for-each select="metadata/eainfo">
            <li>
              <a href="#Entity and Attribute Information">Entity and Attribute Information</a>
            </li>
          </xsl:for-each>
          <xsl:variable name="numdist">
            <xsl:number value="count(metadata/distinfo)" />
          </xsl:variable>
          <xsl:for-each select="metadata/distinfo">
            <xsl:choose>
              <xsl:when test="$numdist = 0"></xsl:when>
              <xsl:when test="$numdist = 1">
                <li>
                  <a href="#{generate-id(.)}">
                  Distribution Information
               </a>
                </li>
              </xsl:when>
              <xsl:otherwise>
                <xsl:choose>
                  <xsl:when test="position() = 1">
                    <li>Distribution Information</li>
                    <li style="margin-left:0.3in">
                      <a href="#{generate-id(.)}">
                  Distributor <xsl:number value="position()" /></a>
                    </li>
                  </xsl:when>
                  <xsl:otherwise>
                    <li style="margin-left:0.3in">
                      <a href="#{generate-id(.)}">
                  Distributor <xsl:number value="position()" /></a>
                    </li>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:for-each>
          <xsl:for-each select="metadata/metainfo">
            <li>
              <a href="#Metadata Reference Information">Metadata Reference Information</a>
            </li>
          </xsl:for-each>
        </ul>
        <xsl:apply-templates select="metadata/idinfo" />
        <xsl:apply-templates select="metadata/dataqual" />
        <xsl:apply-templates select="metadata/spdoinfo" />
        <xsl:apply-templates select="metadata/spref" />
        <xsl:apply-templates select="metadata/eainfo" />
        <xsl:apply-templates select="metadata/distinfo" />
        <xsl:apply-templates select="metadata/metainfo" />
      </body>
    </html>
  </xsl:template>
  <!-- Identification -->
  <xsl:template match="idinfo">
    <a name="Identification Information">
      <hr></hr>
    </a>
    <dl>
      <dt>
        <h3>Identification Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="citation">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Citation:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="citeinfo" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="descript">
            <xsl:apply-templates select="citeinfo" />
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Description:   </font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="abstract">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Abstract:   </font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:choose>
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <dl>
                          <xsl:call-template name="prewrap">
                            <xsl:with-param name="text" select="." />
                          </xsl:call-template>
                        </dl>
                      </xsl:otherwise>
                    </xsl:choose>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="purpose">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Purpose:   </font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:choose>
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <dl>
                          <xsl:call-template name="prewrap">
                            <xsl:with-param name="text" select="." />
                          </xsl:call-template>
                        </dl>
                      </xsl:otherwise>
                    </xsl:choose>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="supplinf">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Supplemental Information:   </font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:choose xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <dl>
                          <xsl:call-template name="prewrap">
                            <xsl:with-param name="text" select="." />
                          </xsl:call-template>
                        </dl>
                      </xsl:otherwise>
                    </xsl:choose>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="timeperd">
            <dt>
              <b>
                <b>
                  <i>
                    <font color="#488AC7">Time Period of Content:   </font>
                  </i>
                </b>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="timeinfo" />
                <xsl:for-each select="current">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Currentness Reference:   </font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:choose>
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:value-of select="." />
                      </xsl:otherwise>
                    </xsl:choose>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="status">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Status:   </font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="progress">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Progress:   </font>
                      </i>
                    </b>
                    <xsl:choose>
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <dl>
                          <xsl:call-template name="prewrap">
                            <xsl:with-param name="text" select="." />
                          </xsl:call-template>
                        </dl>
                      </xsl:otherwise>
                    </xsl:choose>
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="update">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Maintenance and Update Frequency:   </font>
                      </i>
                    </b>
                    <xsl:choose>
                      <xsl:when test="@missing">
                        <font color="red">Required element.</font>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:value-of select="." />
                      </xsl:otherwise>
                    </xsl:choose>
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="spdom">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Spatial Domain:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Description of Geographic Extent:   </font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <xsl:value-of select="descgeog" />
                </dd>
                <xsl:for-each select="bounding">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Bounding Coordinates:   </font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">West Bounding Coordinate:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="westbc" />
                      </dt>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">East Bounding Coordinate:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="eastbc" />
                      </dt>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">North Bounding Coordinate:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="northbc" />
                      </dt>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">South Bounding Coordinate:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="southbc" />
                      </dt>
                      <xsl:for-each select="boundalt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Bounding Altitudes:</font>
                            </i>
                          </b>
                        </dt>
                        <dl>
                          <dt>
                            <b>
                              <i>
                                <font color="#488AC7">Altitude Minimum:   </font>
                              </i>
                            </b>
                            <xsl:value-of select="altmin" />
                          </dt>
                          <dt>
                            <b>
                              <i>
                                <font color="#488AC7">Altitude Maximum:   </font>
                              </i>
                            </b>
                            <xsl:value-of select="altmax" />
                          </dt>
                          <dt>
                            <b>
                              <i>
                                <font color="#488AC7">Altitude Distance Units:   </font>
                              </i>
                            </b>
                            <xsl:value-of select="altunits" />
                          </dt>
                        </dl>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="dsgpoly">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Data Set G-Polygon:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="dsgpolyo">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Data Set G-Polygon Outer G-Ring:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:apply-templates select="grngpoin" />
                            <xsl:apply-templates select="gring" />
                          </dl>
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="dsgpolyx">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Data Set G-Polygon Exclusion G-Ring:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:apply-templates select="grngpoin" />
                            <xsl:apply-templates select="gring" />
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="keywords">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Keywords:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="theme">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Theme:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="themekt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Theme Keyword Thesaurus:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="themekey">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Theme Keyword:   </font>
                            </i>
                          </b>
                          <xsl:choose>
                            <xsl:when test="@missing">
                              <font color="red">Required element.</font>
                            </xsl:when>
                            <xsl:otherwise>
                              <xsl:value-of select="." />
                            </xsl:otherwise>
                          </xsl:choose>
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="place">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Place:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="placekt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Place Keyword Thesaurus:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="placekey">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Place Keyword:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="stratum">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Stratum:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="stratkt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Stratum Keyword Thesaurus:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="stratkey">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Stratum Keyword:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="temporal">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Temporal:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="tempkt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Temporal Keyword Thesaurus:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="tempkey">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Temporal Keyword:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="taxonomy">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Taxonomy:</font>
                </i>
              </b>
            </dt>
            <dl>
              <xsl:for-each select="keywtax">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Keywords/Taxon:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Taxonomic Keyword Thesaurus:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="taxonkt" />
                  </dd>
                  <xsl:for-each select="taxonkey">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Taxonomic Keywords:   </font>
                        </i>
                      </b>
                      <xsl:value-of select="." />
                    </dt>
                  </xsl:for-each>
                </dl>
              </xsl:for-each>
              <xsl:for-each select="taxonsys">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Taxonomic System:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <xsl:for-each select="classsys">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Classification System/Authority:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <xsl:for-each select="classcit">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Classification System Citation:</font>
                            </i>
                          </b>
                        </dt>
                        <dl>
                          <xsl:apply-templates select="citeinfo" />
                        </dl>
                      </xsl:for-each>
                      <xsl:for-each select="classmod">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Classification System Modifications:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </xsl:for-each>
                  <xsl:for-each select="idref">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Identification Reference:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <xsl:apply-templates select="citeinfo" />
                    </dl>
                  </xsl:for-each>
                  <xsl:for-each select="ider">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Identifer:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <xsl:apply-templates select="cntinfo" />
                    </dl>
                  </xsl:for-each>
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Taxonomic Procedures:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="taxonpro" />
                  </dd>
                  <xsl:for-each select="taxoncom">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Taxonomic Completeness:</font>
                        </i>
                      </b>
                    </dt>
                    <dd>
                      <xsl:value-of select="." />
                    </dd>
                  </xsl:for-each>
                  <xsl:for-each select="vouchers">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Vouchers:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Specimen:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="specimen" />
                      </dt>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Repository:</font>
                          </i>
                        </b>
                      </dt>
                      <xsl:for-each select="reposit">
                        <dl>
                          <xsl:apply-templates select="cntinfo" />
                        </dl>
                      </xsl:for-each>
                    </dl>
                  </xsl:for-each>
                </dl>
              </xsl:for-each>
              <xsl:for-each select="taxongen">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">General Taxonomic Coverage:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <xsl:value-of select="." />
                </dd>
              </xsl:for-each>
              <xsl:apply-templates select="taxoncl" />
            </dl>
          </xsl:for-each>
          <xsl:for-each select="accconst">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Access Constraints:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="useconst">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Use Constraints:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="ptcontac">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Point of Contact:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="cntinfo" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="browse">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Browse Graphic:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="browsen">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Browse Graphic File Name:   </font>
                      </i>
                    </b>
                    <a TARGET="viewer">
                      <xsl:attribute name="href">
                        <xsl:value-of select="." />
                      </xsl:attribute>
                      <xsl:value-of select="." />
                    </a>
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="browsed">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Browse Graphic File Description:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="." />
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="browset">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Browse Graphic File Type:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="datacred">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Data Set Credit:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="secinfo">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Security Information:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="secsys">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Security Classification System:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="secclass">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Security Classification:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="sechandl">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Security Handling Description:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="native">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Native Data Set Environment:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:call-template name="prewrap">
                  <xsl:with-param name="text" select="." />
                </xsl:call-template>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="crossref">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Cross Reference:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="citeinfo" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="tool">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Analytical Tool:</font>
                </i>
              </b>
            </dt>
            <dl>
              <dt>
                <b>
                  <i>
                    <font color="#488AC7">Analytical Tool Description:</font>
                  </i>
                </b>
              </dt>
              <dd>
                <dl>
                  <xsl:call-template name="prewrap">
                    <xsl:with-param name="text" select="tooldesc" />
                  </xsl:call-template>
                </dl>
              </dd>
              <xsl:for-each select="toolacc">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Tool Access Information:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <xsl:for-each select="onlink">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Online Linkage:   </font>
                        </i>
                      </b>
                      <a>
                        <xsl:attribute name="href">
                          <xsl:value-of select="." />
                        </xsl:attribute>
                        <xsl:value-of select="." />
                      </a>
                    </dt>
                  </xsl:for-each>
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Tool Access Instructions:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="toolinst" />
                  </dd>
                  <xsl:for-each select="toolcomp">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Tool Computer and Operating System:</font>
                        </i>
                      </b>
                    </dt>
                    <dd>
                      <xsl:value-of select="." />
                    </dd>
                  </xsl:for-each>
                </dl>
              </xsl:for-each>
              <xsl:for-each select="toolcont">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Tool Contact:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <xsl:apply-templates select="cntinfo" />
                </dl>
              </xsl:for-each>
              <xsl:for-each select="toolcite">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Tool Citation:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <xsl:apply-templates select="citeinfo" />
                </dl>
              </xsl:for-each>
            </dl>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="r">Back to Top</a>
  </xsl:template>
  <!-- Data Quality -->
  <xsl:template match="dataqual">
    <a name="Data Quality Information">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Data Quality Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="attracc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Attribute Accuracy:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="attraccr">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Attribute Accuracy Report:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:call-template name="prewrap">
                        <xsl:with-param name="text" select="." />
                      </xsl:call-template>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="qattracc">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Quantitative Attribute Accuracy Assessment:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="attraccv">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Attribute Accuracy Value:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="attracce">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Attribute Accuracy Explanation:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:call-template name="prewrap">
                              <xsl:with-param name="text" select="." />
                            </xsl:call-template>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="logic">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Logical Consistency Report:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:call-template name="prewrap">
                  <xsl:with-param name="text" select="." />
                </xsl:call-template>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="complete">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Completeness Report:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="posacc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Positional Accuracy:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="horizpa">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Horizontal Positional Accuracy:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="horizpar">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Horizontal Positional Accuracy Report:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="qhorizpa">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Quantitative Horizontal Positional Accuracy Assessment:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="horizpav">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Horizontal Positional Accuracy Value:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="horizpae">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Horizontal Positional Accuracy Explanation:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="vertacc">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Vertical Positional Accuracy:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="vertaccr">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Vertical Positional Accuracy Report:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="qvertpa">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Quantitative Vertical Positional Accuracy Assessment:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="vertaccv">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Vertical Positional Accuracy Value:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="vertacce">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Vertical Positional Accuracy Explanation:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="lineage">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Lineage:</font>
                </i>
              </b>
            </dt>
            <dl>
              <xsl:for-each select="method">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Methodology:</font>
                    </i>
                  </b>
                </dt>
                <dl>
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Methodology Type:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="methtype" />
                  </dt>
                  <xsl:for-each select="methodid">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Methodolgy Identifier:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Methodolgy Keyword Thesaurus:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="methkt" />
                      </dd>
                      <xsl:for-each select="methkey">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Methodology Keyword:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </xsl:for-each>
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Methodology Description:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:call-template name="prewrap">
                        <xsl:with-param name="text" select="methdesc" />
                      </xsl:call-template>
                    </dl>
                  </dd>
                  <xsl:for-each select="methcite">
                    <dt>
                      <b>
                        <i>
                          <font color="#488AC7">Methodology Citation:</font>
                        </i>
                      </b>
                    </dt>
                    <dl>
                      <xsl:apply-templates select="citeinfo" />
                    </dl>
                  </xsl:for-each>
                </dl>
              </xsl:for-each>
              <xsl:for-each select="srcinfo">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Source Information:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:for-each select="srccite">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Citation:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <dl>
                          <xsl:apply-templates select="citeinfo" />
                        </dl>
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="srcscale">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Scale Denominator:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="typesrc">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Type of Source Media:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="srctime">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Time Period of Content:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <dl>
                          <xsl:apply-templates select="timeinfo" />
                          <xsl:for-each select="srccurr">
                            <dt>
                              <b>
                                <i>
                                  <font color="#488AC7">Source Currentness Reference:</font>
                                </i>
                              </b>
                            </dt>
                            <dd>
                              <xsl:value-of select="." />
                            </dd>
                          </xsl:for-each>
                        </dl>
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="srccitea">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Citation Abbreviation:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="srccontr">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Contribution:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                  </dl>
                </dd>
              </xsl:for-each>
              <xsl:for-each select="procstep">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Process Step:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:for-each select="procdesc">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Process Description:</font>
                          </i>
                        </b>
                      </dt>
                      <dl>
                        <xsl:call-template name="prewrap">
                          <xsl:with-param name="text" select="." />
                        </xsl:call-template>
                      </dl>
                    </xsl:for-each>
                    <xsl:for-each select="srcused">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Used Citation Abbreviation:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="procdate">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Process Date:   </font>
                          </i>
                        </b>
                        <xsl:call-template name="write_date">
                          <xsl:with-param name="vtext" select="." />
                        </xsl:call-template>
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="proctime">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Process Time:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="srcprod">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Source Produced Citation Abbreviation:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="proccont">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Process Contact:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <dl>
                          <xsl:apply-templates select="cntinfo" />
                        </dl>
                      </dd>
                    </xsl:for-each>
                  </dl>
                </dd>
              </xsl:for-each>
            </dl>
          </xsl:for-each>
          <xsl:for-each select="cloud">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Cloud Cover:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Spatial Data Organization -->
  <xsl:template match="spdoinfo">
    <a name="Spatial Data Organization Information">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Spatial Data Organization Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="indspref">
            <dt>
              <h3>Indirect Spatial Reference Method:</h3>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="direct">
            <dt>
              <h3>Direct Spatial Reference Method:   </h3>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="ptvctinf">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Point and Vector Object Information:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="sdtsterm">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">SDTS Terms Description:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="sdtstype">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">SDTS Point and Vector Object Type:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="ptvctcnt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Point and Vector Object Count:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="vpfterm">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">VPF Terms Description:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="vpflevel">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">VPF Topology Level:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="vpfinfo">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">VPF Point and Vector Object Information:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="vpftype">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">VPF Point and Vector Object Type:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="ptvctcnt">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Point and Vector Object Count:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="rastinfo">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Raster Object Information:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="rasttype">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Raster Object Type:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="rowcount">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Row Count:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="colcount">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Column Count:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="vrtcount">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Vertical Count:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Spatial Reference -->
  <xsl:template match="spref">
    <a name="Spatial Reference Information">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Spatial Reference Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="horizsys">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Horizontal Coordinate System Definition:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="geograph">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Geographic:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="latres">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Latitude Resolution:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="longres">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Longitude Resolution:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="geogunit">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Geographic Coordinate Units:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="planar">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Planar:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="mapproj">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Map Projection:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="mapprojn">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Map Projection Name:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="albers">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Albers Conical Equal Area:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="azimequi">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Azimuthal Equidistant:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="equicon">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Equidistant Conic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="equirect">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Equirectangular:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="gvnsp">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">General Vertical Near-sided Perspective:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="gnomonic">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Gnomonic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="lamberta">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Lambert Azimuthal Equal Area:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="lambertc">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Lambert Conformal Conic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="mercator">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Mercator:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="modsak">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Modified Stereographic for Alaska:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:apply-templates select="feast" />
                                  <xsl:apply-templates select="fnorth" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="miller">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Miller Cylindrical:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="obqmerc">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Oblique Mercator:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="orthogr">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Orthographic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="polarst">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Polar Stereographic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="polycon">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Polyconic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="robinson">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Robinson:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:apply-templates select="longpc" />
                                  <xsl:apply-templates select="feast" />
                                  <xsl:apply-templates select="fnorth" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="sinusoid">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Sinusoidal:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="spaceobq">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Space Oblique Mercator (Landsat):</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:apply-templates select="landsat" />
                                  <xsl:apply-templates select="pathnum" />
                                  <xsl:apply-templates select="feast" />
                                  <xsl:apply-templates select="fnorth" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="stereo">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Stereographic:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="transmer">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Transverse Mercator:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="vdgrin">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">van der Grinten:</font>
                                  </i>
                                </b>
                              </dt>
                              <xsl:apply-templates select="." />
                            </xsl:for-each>
                            <xsl:for-each select="otherprj">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Other Projection's Definition:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="gridsys">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Grid Coordinate System:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="gridsysn">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Grid Coordinate System Name:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="utm">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Universal Transverse Mercator:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="utmzone">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">UTM Zone Number:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="transmer">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Transverse Mercator:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="transmer" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="ups">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Universal Polar Stereographic:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="upszone">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">UPS Zone Identifier:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="polarst">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Polar Stereographic:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="polarst" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="spcs">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">State Plane Coordinate System:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="spcszone">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">SPCS Zone Identifier:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="lambertc">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Lambert Conformal Conic:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="lambertc" />
                                  <xsl:for-each select="transmer">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Transverse Mercator:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="transmer" />
                                  <xsl:for-each select="obqmerc">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Oblique Mercator:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="obqmerc" />
                                  <xsl:for-each select="polycon">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Polyconic:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="polycon" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="arcsys">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">ARC Coordinate System:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="arczone">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">ARC System Zone Identifier:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="equirect">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Equirectangular:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="equirect" />
                                  <xsl:for-each select="azimequi">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Azimuthal Equidistant:</font>
                                        </i>
                                      </b>
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:apply-templates select="azimequi" />
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="othergrd">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Other Grid System's Definition:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="localp">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Local Planar:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="localpd">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Local Planar Description:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="localpgi">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Local Planar Georeference Information:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="planci">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Planar Coordinate Information:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="plance">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Planar Coordinate Encoding Method:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="coordrep">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Coordinate Representation:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="absres">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Abscissa Resolution:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="ordres">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Ordinate Resolution:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="distbrep">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Distance and Bearing Representation:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="distres">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Distance Resolution:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="bearres">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Bearing Resolution:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="bearunit">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Bearing Units:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="bearrefd">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Bearing Reference Direction:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="bearrefm">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Bearing Reference Meridian:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="plandu">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Planar Distance Units:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="local">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Local:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="localdes">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Local Description:</font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="localgeo">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Local Georeference Information:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="geodetic">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Geodetic Model:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="horizdn">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Horizontal Datum Name:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="ellips">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Ellipsoid Name:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="semiaxis">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Semi-major Axis:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="denflat">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Denominator of Flattening Ratio:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="vertdef">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Vertical Coordinate System Definition:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="altsys">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Altitude System Definition:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="altdatum">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Altitude Datum Name:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="altres">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Altitude Resolution:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="altunits">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Altitude Distance Units:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="altenc">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Altitude Encoding Method:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="depthsys">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Depth System Definition:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="depthdn">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Depth Datum Name:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="depthres">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Depth Resolution:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="depthdu">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Depth Distance Units:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="depthem">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Depth Encoding Method:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Entity and Attribute -->
  <xsl:template match="eainfo">
    <a name="Entity and Attribute Information">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Entity and Attribute Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="detailed">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Detailed Description:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="enttyp">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Entity Type:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="enttypl">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Entity Type Label:   </font>
                            </i>
                          </b>
                          <xsl:value-of select="." />
                        </dt>
                      </xsl:for-each>
                      <xsl:for-each select="enttypd">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Entity Type Definition:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="enttypds">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Entity Type Definition Source:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <xsl:value-of select="." />
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:apply-templates select="attr" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="overview">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Overview Description:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="eaover">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Entity and Attribute Overview:</font>
                      </i>
                    </b>
                  </dt>
                  <dl>
                    <xsl:call-template name="prewrap" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                      <xsl:with-param name="text" select="." />
                    </xsl:call-template>
                  </dl>
                </xsl:for-each>
                <xsl:for-each select="eadetcit">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Entity and Attribute Detail Citation:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="." />
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Distribution -->
  <xsl:template match="distinfo">
    <a name="{generate-id(.)}">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Distribution Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="distrib">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Distributor:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="cntinfo" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="resdesc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Resource Description:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="distliab">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Distribution Liability:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="stdorder">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Standard Order Process:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="nondig">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Non-digital Form:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="." />
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="digform">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Digital Form:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <dl>
                      <xsl:for-each select="digtinfo">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Digital Transfer Information:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="formname">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Format Name:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="formvern">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Format Version Number:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="formverd">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Format Version Date:   </font>
                                  </i>
                                </b>
                                <xsl:call-template name="write_date">
                                  <xsl:with-param name="vtext" select="." />
                                </xsl:call-template>
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="formspec">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Format Specification:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="asciistr">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">ASCII File Structure:</font>
                                  </i>
                                </b>
                              </dt>
                              <dl>
                                <xsl:for-each select="recdel">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Record Delimiter:   </font>
                                      </i>
                                    </b>
                                    <xsl:value-of select="." />
                                  </dt>
                                </xsl:for-each>
                                <xsl:for-each select="numheadl">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Number Header Lines:   </font>
                                      </i>
                                    </b>
                                    <xsl:value-of select="." />
                                  </dt>
                                </xsl:for-each>
                                <xsl:for-each select="deschead">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Description of Header Content:</font>
                                      </i>
                                    </b>
                                  </dt>
                                  <dd>
                                    <xsl:value-of select="." />
                                  </dd>
                                </xsl:for-each>
                                <xsl:for-each select="orienta">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Orientation:   </font>
                                      </i>
                                    </b>
                                    <xsl:value-of select="." />
                                  </dt>
                                </xsl:for-each>
                                <xsl:for-each select="casesens">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Case Sensitive:   </font>
                                      </i>
                                    </b>
                                    <xsl:value-of select="." />
                                  </dt>
                                </xsl:for-each>
                                <xsl:for-each select="authent">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Authentication:   </font>
                                      </i>
                                    </b>
                                  </dt>
                                  <dd>
                                    <xsl:value-of select="." />
                                  </dd>
                                </xsl:for-each>
                                <xsl:for-each select="quotech">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Quote character:   </font>
                                      </i>
                                    </b>
                                    <xsl:value-of select="." />
                                  </dt>
                                </xsl:for-each>
                                <xsl:for-each select="datafiel">
                                  <dt>
                                    <b>
                                      <i>
                                        <font color="#488AC7">Data Field:</font>
                                      </i>
                                    </b>
                                  </dt>
                                  <dl>
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Data Field Name:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="dfieldnm" />
                                    </dt>
                                    <xsl:for-each select="missingv">
                                      <dt>
                                        <b>
                                          <i>
                                            <font color="#488AC7">Missing Value Code:   </font>
                                          </i>
                                        </b>
                                        <xsl:value-of select="." />
                                      </dt>
                                    </xsl:for-each>
                                    <xsl:for-each select="dfwidthd">
                                      <dt>
                                        <b>
                                          <i>
                                            <font color="#488AC7">Data Field Width Delimiter:   </font>
                                          </i>
                                        </b>
                                        <xsl:value-of select="." />
                                      </dt>
                                    </xsl:for-each>
                                    <xsl:for-each select="dfwidth">
                                      <dt>
                                        <b>
                                          <i>
                                            <font color="#488AC7">Data Field Width:   </font>
                                          </i>
                                        </b>
                                        <xsl:value-of select="." />
                                      </dt>
                                    </xsl:for-each>
                                  </dl>
                                </xsl:for-each>
                              </dl>
                            </xsl:for-each>
                            <xsl:for-each select="formcont">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Format Information Content:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <xsl:value-of select="." />
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="filedec">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">File Decompression Technique:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                            <xsl:for-each select="transize">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Transfer Size:   </font>
                                  </i>
                                </b>
                                <xsl:value-of select="." />
                              </dt>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                      <xsl:for-each select="digtopt">
                        <dt>
                          <b>
                            <i>
                              <font color="#488AC7">Digital Transfer Option:</font>
                            </i>
                          </b>
                        </dt>
                        <dd>
                          <dl>
                            <xsl:for-each select="onlinopt">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Online Option:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="computer">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Computer Contact Information:</font>
                                        </i>
                                      </b>
                                    </dt>
                                    <dd>
                                      <dl>
                                        <xsl:for-each select="networka">
                                          <dt>
                                            <b>
                                              <i>
                                                <font color="#488AC7">Network Address:</font>
                                              </i>
                                            </b>
                                          </dt>
                                          <dd>
                                            <dl>
                                              <xsl:for-each select="networkr">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Network Resource Name:</font>
                                                    </i>
                                                  </b>
                                                  <a TARGET="viewer">
                                                    <xsl:attribute name="href">
                                                      <xsl:value-of select="." />
                                                    </xsl:attribute>
                                                    <xsl:value-of select="." />
                                                  </a>
                                                </dt>
                                              </xsl:for-each>
                                            </dl>
                                          </dd>
                                        </xsl:for-each>
                                        <xsl:for-each select="dialinst">
                                          <dt>
                                            <b>
                                              <i>
                                                <font color="#488AC7">Dialup Instructions:</font>
                                              </i>
                                            </b>
                                          </dt>
                                          <dd>
                                            <dl>
                                              <xsl:for-each select="lowbps">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Lowest BPS:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="highbps">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Highest BPS:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="numdata">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Number DataBits:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="numstop">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Number StopBits:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="parity">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Parity:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="compress">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Compression Support:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="dialtel">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Dialup Telephone:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                              <xsl:for-each select="dialfile">
                                                <dt>
                                                  <b>
                                                    <i>
                                                      <font color="#488AC7">Dialup File Name:   </font>
                                                    </i>
                                                  </b>
                                                  <xsl:value-of select="." />
                                                </dt>
                                              </xsl:for-each>
                                            </dl>
                                          </dd>
                                        </xsl:for-each>
                                      </dl>
                                    </dd>
                                  </xsl:for-each>
                                  <xsl:for-each select="accinstr">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Access Instructions:</font>
                                        </i>
                                      </b>
                                    </dt>
                                    <dd>
                                      <xsl:value-of select="." />
                                    </dd>
                                  </xsl:for-each>
                                  <xsl:for-each select="oncomp">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Online Computer and Operating System:</font>
                                        </i>
                                      </b>
                                    </dt>
                                    <dd>
                                      <xsl:value-of select="." />
                                    </dd>
                                  </xsl:for-each>
                                </dl>
                              </dd>
                            </xsl:for-each>
                            <xsl:for-each select="offoptn">
                              <dt>
                                <b>
                                  <i>
                                    <font color="#488AC7">Offline Option:</font>
                                  </i>
                                </b>
                              </dt>
                              <dd>
                                <dl>
                                  <xsl:for-each select="offmedia">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Offline Media:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="reccap">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Recording Capacity:</font>
                                        </i>
                                      </b>
                                    </dt>
                                    <dd>
                                      <dl>
                                        <xsl:for-each select="recden">
                                          <dt>
                                            <b>
                                              <i>
                                                <font color="#488AC7">Recording Density:   </font>
                                              </i>
                                            </b>
                                            <xsl:value-of select="." />
                                          </dt>
                                        </xsl:for-each>
                                        <xsl:for-each select="recdenu">
                                          <dt>
                                            <b>
                                              <i>
                                                <font color="#488AC7">Recording Density Units:   </font>
                                              </i>
                                            </b>
                                            <xsl:value-of select="." />
                                          </dt>
                                        </xsl:for-each>
                                      </dl>
                                    </dd>
                                  </xsl:for-each>
                                  <xsl:for-each select="recfmt">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Recording Format:   </font>
                                        </i>
                                      </b>
                                      <xsl:value-of select="." />
                                    </dt>
                                  </xsl:for-each>
                                  <xsl:for-each select="compat">
                                    <dt>
                                      <b>
                                        <i>
                                          <font color="#488AC7">Compatibility Information:</font>
                                        </i>
                                      </b>
                                    </dt>
                                    <dd>
                                      <xsl:value-of select="." />
                                    </dd>
                                  </xsl:for-each>
                                </dl>
                              </dd>
                            </xsl:for-each>
                          </dl>
                        </dd>
                      </xsl:for-each>
                    </dl>
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="fees">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Fees:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="ordering">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Ordering Instructions:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="." />
                  </dd>
                </xsl:for-each>
                <xsl:for-each select="turnarnd">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Turnaround:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="custom">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Custom Order Process:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="techpreq">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Technical Prerequisites:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="availabl">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Available Time Period:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="timeinfo" />
              </dl>
            </dd>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Metadata -->
  <xsl:template match="metainfo">
    <a name="Metadata Reference Information">
      <hr />
    </a>
    <dl>
      <dt>
        <h3>Metadata Reference Information:</h3>
      </dt>
      <dd>
        <dl>
          <xsl:for-each select="metd">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Date:   </font>
                </i>
              </b>
              <xsl:call-template name="write_date">
                <xsl:with-param name="vtext" select="." />
              </xsl:call-template>
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metrd">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Review Date:   </font>
                </i>
              </b>
              <xsl:call-template name="write_date">
                <xsl:with-param name="vtext" select="." />
              </xsl:call-template>
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metfrd">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Future Review Date:   </font>
                </i>
              </b>
              <xsl:call-template name="write_date">
                <xsl:with-param name="vtext" select="." />
              </xsl:call-template>
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Contact:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:apply-templates select="cntinfo" />
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="metstdn">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Standard Name:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metstdv">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Standard Version:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="mettc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Time Convention:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metac">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Access Constraints:   </font>
                </i>
              </b>
              <xsl:value-of select="." />
            </dt>
          </xsl:for-each>
          <xsl:for-each select="metuc">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Use Constraints:</font>
                </i>
              </b>
            </dt>
            <dd>
              <xsl:value-of select="." />
            </dd>
          </xsl:for-each>
          <xsl:for-each select="metsi">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Security Information:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="metscs">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Metadata Security Classification System:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="metsc">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Metadata Security Classification:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="metshd">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Metadata Security Handling Description:</font>
                      </i>
                    </b>
                  </dt>
                  <dd>
                    <xsl:value-of select="." />
                  </dd>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
          <xsl:for-each select="metextns">
            <dt>
              <b>
                <i>
                  <font color="#488AC7">Metadata Extensions:</font>
                </i>
              </b>
            </dt>
            <dd>
              <dl>
                <xsl:for-each select="onlink">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Online Linkage:</font>
                      </i>
                    </b>
                    <a TARGET="viewer">
                      <xsl:attribute name="href">
                        <xsl:value-of select="." />
                      </xsl:attribute>
                      <xsl:value-of select="." />
                    </a>
                  </dt>
                </xsl:for-each>
                <xsl:for-each select="metprof">
                  <dt>
                    <b>
                      <i>
                        <font color="#488AC7">Profile Name:   </font>
                      </i>
                    </b>
                    <xsl:value-of select="." />
                  </dt>
                </xsl:for-each>
              </dl>
            </dd>
          </xsl:for-each>
        </dl>
      </dd>
    </dl>
    <a href="#Top">Back to Top</a>
  </xsl:template>
  <!-- Citation -->
  <xsl:template match="citeinfo">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Citation Information:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="origin">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Originator:   </font>
              </i>
            </b>
            <xsl:choose>
              <xsl:when test="@missing">
                <font color="red">Required element.</font>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="." />
              </xsl:otherwise>
            </xsl:choose>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="pubdate">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Publication Date:   </font>
              </i>
            </b>
            <xsl:choose>
              <xsl:when test="@missing">
                <font color="red">Required element.</font>
              </xsl:when>
              <xsl:otherwise>
                <xsl:call-template name="write_date">
                  <xsl:with-param name="vtext" select="." />
                </xsl:call-template>
              </xsl:otherwise>
            </xsl:choose>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="pubtime">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Publication Time:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="title">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Title:   </font>
              </i>
            </b>
          </dt>
          <xsl:choose>
            <xsl:when test="@missing">
              <font color="red">Required element.</font>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="." />
            </xsl:otherwise>
          </xsl:choose>
        </xsl:for-each>
        <xsl:for-each select="edition">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Edition:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="geoform">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Geospatial Data Presentation Form:   </font>
              </i>
            </b>
            <xsl:choose>
              <xsl:when test="@missing">
                <font color="red">Required element.</font>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="." />
              </xsl:otherwise>
            </xsl:choose>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="serinfo">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Series Information:   </font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="sername">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Series Name:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
              <xsl:for-each select="issue">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Issue Identification:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="pubinfo">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Publication Information:   </font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="pubplace">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Publication Place:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
              <xsl:for-each select="publish">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Publisher:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="othercit">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Other Citation Details:   </font>
              </i>
            </b>
          </dt>
          <dd>
            <xsl:value-of select="." />
          </dd>
        </xsl:for-each>
        <xsl:for-each select="onlink">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Online Linkage:   </font>
              </i>
            </b>
            <a>
              <xsl:attribute name="href">
                <xsl:value-of select="." />
              </xsl:attribute>
              <xsl:value-of select="." />
            </a>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="lworkcit">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Larger Work Citation:   </font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:apply-templates select="citeinfo" />
            </dl>
          </dd>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <!-- Contact -->
  <xsl:template match="cntinfo">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Contact Information:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="cntperp">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Person Primary:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="cntper">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Contact Person:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="cntorg">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Contact Organization:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="cntorgp">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Organization Primary:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="cntorg">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Contact Organization:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="cntper">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Contact Person:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="cntpos">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Position:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="cntaddr">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Address:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="addrtype">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Address Type:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="address">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Address:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
              <xsl:for-each select="city">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">City:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="state">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">State or Province:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="postal">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Postal Code:   </font>
                    </i>
                  </b>
                  <xsl:choose>
                    <xsl:when test="@missing">
                      <font color="red">Required element.</font>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:value-of select="." />
                    </xsl:otherwise>
                  </xsl:choose>
                </dt>
              </xsl:for-each>
              <xsl:for-each select="country">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Country:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="cntvoice">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Voice Telephone:   </font>
              </i>
            </b>
            <xsl:choose>
              <xsl:when test="@missing">
                <font color="red">Required element.</font>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="." />
              </xsl:otherwise>
            </xsl:choose>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="cnttdd">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact TDD/TTY Telephone:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="cntfax">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Facsimile Telephone:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="cntemail">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Electronic Mail Address:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="hours">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Hours of Service:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="cntinst">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Contact Instructions:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <!-- Time Period Info -->
  <xsl:template match="timeinfo">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Time Period Information:</font>
        </i>
      </b>
      <xsl:choose>
        <xsl:when test="@missing">
          <font color="red"> Required element.</font>
        </xsl:when>
      </xsl:choose>
    </dt>
    <dd>
      <dl>
        <xsl:apply-templates select="sngdate" />
        <xsl:apply-templates select="mdattim" />
        <xsl:apply-templates select="rngdates" />
      </dl>
    </dd>
  </xsl:template>
  <!-- Single Date/Time -->
  <xsl:template match="sngdate">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Single Date/Time:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="caldate">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Calendar Date:   </font>
              </i>
            </b>
            <xsl:call-template name="write_date">
              <xsl:with-param name="vtext" select="." />
            </xsl:call-template>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="time">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Time of Day:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:apply-templates select="geolage" />
      </dl>
    </dd>
  </xsl:template>
  <!-- Multiple Date/Time -->
  <xsl:template match="mdattim">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Multiple Dates/Times:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:apply-templates select="sngdate" />
      </dl>
    </dd>
  </xsl:template>
  <!-- Range of Dates/Times -->
  <xsl:template match="rngdates">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Range of Dates/Times:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="begdate">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Beginning Date:   </font>
              </i>
            </b>
            <xsl:call-template name="write_date">
              <xsl:with-param name="vtext" select="." />
            </xsl:call-template>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="begtime">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Beginning Time:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="enddate">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Ending Date:   </font>
              </i>
            </b>
            <xsl:call-template name="write_date">
              <xsl:with-param name="vtext" select="." />
            </xsl:call-template>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="endtime">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Ending Time:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="beggeol">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Beginning Geologic Age:   </font>
              </i>
            </b>
          </dt>
          <dl>
            <xsl:apply-templates select="geolage" />
          </dl>
        </xsl:for-each>
        <xsl:for-each select="endgeol">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Ending Geologic Age:   </font>
              </i>
            </b>
          </dt>
          <dl>
            <xsl:apply-templates select="geolage" />
          </dl>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <!-- Geologic Age, NBII extension -->
  <xsl:template match="geolage">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Geologic Age:</font>
        </i>
      </b>
    </dt>
    <xsl:for-each select="geolscal">
      <dt>
        <b>
          <i>
            <font color="#488AC7">Geologic Time Scale:   </font>
          </i>
        </b>
        <xsl:value-of select="." />
      </dt>
    </xsl:for-each>
    <xsl:for-each select="geolest">
      <dt>
        <b>
          <i>
            <font color="#488AC7">Geologic Age Estimate:   </font>
          </i>
        </b>
        <xsl:value-of select="." />
      </dt>
    </xsl:for-each>
    <xsl:for-each select="geolun">
      <dt>
        <b>
          <i>
            <font color="#488AC7">Geologic Age Uncertainty:   </font>
          </i>
        </b>
        <dd>
          <xsl:value-of select="." />
        </dd>
      </dt>
    </xsl:for-each>
    <xsl:for-each select="geolexpl">
      <dt>
        <b>
          <i>
            <font color="#488AC7">Geologic Age Explanation:   </font>
          </i>
        </b>
        <dd>
          <xsl:value-of select="." />
        </dd>
      </dt>
    </xsl:for-each>
    <xsl:apply-templates select="geolcit" />
  </xsl:template>
  <xsl:template match="geolcit">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Geologic Citation:   </font>
        </i>
      </b>
    </dt>
    <dl>
      <xsl:apply-templates select="citeinfo" />
    </dl>
  </xsl:template>
  <!-- Taxonomic Classification -->
  <xsl:template match="taxoncl">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Taxonomic Classification:</font>
        </i>
      </b>
    </dt>
    <dl>
      <dt>
        <b>
          <i>
            <font color="#488AC7">Taxon Rank Name:   </font>
          </i>
        </b>
        <xsl:value-of select="taxonrn" />
      </dt>
      <dt>
        <b>
          <i>
            <font color="#488AC7">Taxon Rank Value:   </font>
          </i>
        </b>
        <xsl:value-of select="taxonrv" />
      </dt>
      <xsl:for-each select="common">
        <dt>
          <b>
            <i>
              <font color="#488AC7">Applicable Common Name:   </font>
            </i>
          </b>
          <xsl:value-of select="." />
        </dt>
      </xsl:for-each>
      <xsl:apply-templates select="taxoncl" />
    </dl>
  </xsl:template>
  <!-- G-Ring -->
  <xsl:template match="grngpoin">
    <dt>
      <b>
        <i>
          <font color="#488AC7">G-Ring Point:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="gringlat">
          <dt>
            <b>
              <i>
                <font color="#488AC7">G-Ring Latitude:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="gringlon">
          <dt>
            <b>
              <i>
                <font color="#488AC7">G-Ring Longitude:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="gring">
    <dt>
      <b>
        <i>
          <font color="#488AC7">G-Ring:</font>
        </i>
      </b>
    </dt>
    <dd>
      <xsl:value-of select="." />
    </dd>
  </xsl:template>
  <!-- Map Projections -->
  <xsl:template match="albers | equicon | lambertc">
    <dd>
      <dl>
        <xsl:apply-templates select="stdparll" />
        <xsl:apply-templates select="longcm" />
        <xsl:apply-templates select="latprjo" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="gnomonic | lamberta | orthogr | stereo | gvnsp">
    <dd>
      <dl>
        <xsl:for-each select="../gvnsp">
          <xsl:apply-templates select="heightpt" />
        </xsl:for-each>
        <xsl:apply-templates select="longpc" />
        <xsl:apply-templates select="latprjc" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="miller | sinusoid | vdgrin | equirect | mercator">
    <dd>
      <dl>
        <xsl:for-each select="../equirect">
          <xsl:apply-templates select="stdparll" />
        </xsl:for-each>
        <xsl:for-each select="../mercator">
          <xsl:apply-templates select="stdparll" />
          <xsl:apply-templates select="sfequat" />
        </xsl:for-each>
        <xsl:apply-templates select="longcm" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <!--
<xsl:template match="azimequi | polycon | transmer">
  <dd>
  <dl>
    <xsl:for-each select="../transmer">
      <xsl:apply-templates select="sfctrmer"/>
    </xsl:for-each>
    <xsl:apply-templates select="longcm"/>
    <xsl:apply-templates select="latprjo"/>
    <xsl:apply-templates select="feast"/>
    <xsl:apply-templates select="fnorth"/>
  </dl>
  </dd>
</xsl:template>
-->
  <xsl:template match="azimequi | polycon">
    <dd>
      <dl>
        <xsl:apply-templates select="longcm" />
        <xsl:apply-templates select="latprjo" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="transmer">
    <dd>
      <dl>
        <xsl:apply-templates select="sfctrmer" />
        <xsl:apply-templates select="longcm" />
        <xsl:apply-templates select="latprjo" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="polarst">
    <dd>
      <dl>
        <xsl:apply-templates select="svlong" />
        <xsl:apply-templates select="stdparll" />
        <xsl:apply-templates select="sfprjorg" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="obqmerc">
    <dd>
      <dl>
        <xsl:apply-templates select="sfctrlin" />
        <xsl:apply-templates select="obqlazim" />
        <xsl:apply-templates select="obqlpt" />
        <xsl:apply-templates select="latprjo" />
        <xsl:apply-templates select="feast" />
        <xsl:apply-templates select="fnorth" />
      </dl>
    </dd>
  </xsl:template>
  <!-- Map Projection Parameters -->
  <xsl:template match="stdparll">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Standard Parallel:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="longcm">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Longitude of Central Meridian:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="latprjo">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Latitude of Projection Origin:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="feast">
    <dt>
      <b>
        <i>
          <font color="#488AC7">False Easting:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="fnorth">
    <dt>
      <b>
        <i>
          <font color="#488AC7">False Northing:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="sfequat">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Scale Factor at Equator:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="heightpt">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Height of Perspective Point Above Surface:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="longpc">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Longitude of Projection Center:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="latprjc">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Latitude of Projection Center:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="sfctrlin">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Scale Factor at Center Line:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="obqlazim">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Oblique Line Azimuth:   </font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="azimangl">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Azimuthal Angle:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="azimptl">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Azimuthal Measure Point Longitude:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="obqlpt">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Oblique Line Point:   </font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <dt>
          <b>
            <i>
              <font color="#488AC7">Oblique Line Latitude:   </font>
            </i>
          </b>
          <xsl:value-of select="obqllat[1]" />
        </dt>
        <dt>
          <b>
            <i>
              <font color="#488AC7">Oblique Line Longitude:   </font>
            </i>
          </b>
          <xsl:value-of select="obqllong[1]" />
        </dt>
        <dt>
          <b>
            <i>
              <font color="#488AC7">Oblique Line Latitude:   </font>
            </i>
          </b>
          <xsl:value-of select="obqllat[2]" />
        </dt>
        <dt>
          <b>
            <i>
              <font color="#488AC7">Oblique Line Longitude:   </font>
            </i>
          </b>
          <xsl:value-of select="obqllong[2]" />
        </dt>
      </dl>
    </dd>
  </xsl:template>
  <xsl:template match="svlong">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Straight Vertical Longitude from Pole:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="sfprjorg">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Scale Factor at Projection Origin:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="landsat">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Landsat Number:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="pathnum">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Path Number:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="sfctrmer">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Scale Factor at Central Meridian:   </font>
        </i>
      </b>
      <xsl:value-of select="." />
    </dt>
  </xsl:template>
  <xsl:template match="attr">
    <dt>
      <b>
        <i>
          <font color="#488AC7">Attribute:</font>
        </i>
      </b>
    </dt>
    <dd>
      <dl>
        <xsl:for-each select="attrlabl">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Label:   </font>
              </i>
            </b>
            <xsl:value-of select="." />
          </dt>
        </xsl:for-each>
        <xsl:for-each select="attrdef">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Definition:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:call-template name="prewrap">
                <xsl:with-param name="text" select="." />
              </xsl:call-template>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="attrdefs">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Definition Source:</font>
              </i>
            </b>
          </dt>
          <dd>
            <xsl:value-of select="." />
          </dd>
        </xsl:for-each>
        <xsl:for-each select="attrdomv">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Domain Values:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="edom">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Enumerated Domain:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:for-each select="edomv">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Enumerated Domain Value:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="edomvd">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Enumerated Domain Value Definition:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                    <xsl:for-each select="edomvds">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Enumerated Domain Value Definition Source:</font>
                          </i>
                        </b>
                      </dt>
                      <dd>
                        <xsl:value-of select="." />
                      </dd>
                    </xsl:for-each>
                    <xsl:apply-templates select="attr" />
                  </dl>
                </dd>
              </xsl:for-each>
              <xsl:for-each select="rdom">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Range Domain:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:for-each select="rdommin">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Range Domain Minimum:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="rdommax">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Range Domain Maximum:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="attrunit">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Attribute Units of Measure:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="attrmres">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Attribute Measurement Resolution:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:apply-templates select="attr" />
                  </dl>
                </dd>
              </xsl:for-each>
              <xsl:for-each select="codesetd">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Codeset Domain:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:for-each select="codesetn">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Codeset Name:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                    <xsl:for-each select="codesets">
                      <dt>
                        <b>
                          <i>
                            <font color="#488AC7">Codeset Source:   </font>
                          </i>
                        </b>
                        <xsl:value-of select="." />
                      </dt>
                    </xsl:for-each>
                  </dl>
                </dd>
              </xsl:for-each>
              <xsl:for-each select="udom">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Unrepresentable Domain:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <dl>
                    <xsl:call-template name="prewrap">
                      <xsl:with-param name="text" select="." />
                    </xsl:call-template>
                  </dl>
                </dd>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="begdatea">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Beginning Date of Attribute Values:   </font>
              </i>
            </b>
            <xsl:call-template name="write_date">
              <xsl:with-param name="vtext" select="." />
            </xsl:call-template>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="enddatea">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Ending Date of Attribute Values:   </font>
              </i>
            </b>
            <xsl:call-template name="write_date">
              <xsl:with-param name="vtext" select="." />
            </xsl:call-template>
          </dt>
        </xsl:for-each>
        <xsl:for-each select="attrvai">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Value Accuracy Information:</font>
              </i>
            </b>
          </dt>
          <dd>
            <dl>
              <xsl:for-each select="attrva">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Attribute Value Accuracy:   </font>
                    </i>
                  </b>
                  <xsl:value-of select="." />
                </dt>
              </xsl:for-each>
              <xsl:for-each select="attrvae">
                <dt>
                  <b>
                    <i>
                      <font color="#488AC7">Attribute Value Accuracy Explanation:</font>
                    </i>
                  </b>
                </dt>
                <dd>
                  <xsl:value-of select="." />
                </dd>
              </xsl:for-each>
            </dl>
          </dd>
        </xsl:for-each>
        <xsl:for-each select="attrmfrq">
          <dt>
            <b>
              <i>
                <font color="#488AC7">Attribute Measurement Frequency:</font>
              </i>
            </b>
          </dt>
          <dd>
            <xsl:value-of select="." />
          </dd>
        </xsl:for-each>
      </dl>
    </dd>
  </xsl:template>
  <xsl:template name="prewrap">
    <xsl:param name="text" select="." />
    <xsl:variable name="spaceIndex" select="string-length(substring-after($text, '  '))" />
    <xsl:variable name="tabIndex" select="string-length(substring-after($text, '&#x9;'))" />
    <xsl:variable name="lineFeedIndex" select="string-length(substring-after($text, '&#xA;'))" />
    <xsl:choose>
      <xsl:when test="$spaceIndex = 0 and $tabIndex = 0 and $lineFeedIndex = 0">
        <!-- no special characters left -->
        <xsl:value-of select="$text" />
      </xsl:when>
      <xsl:when test="$spaceIndex &lt; $tabIndex and $lineFeedIndex &lt; $tabIndex">
        <!-- tab -->
        <xsl:value-of select="substring-before($text, '&#x9;')" />
        <xsl:text disable-output-escaping="yes">        </xsl:text>
        <xsl:call-template name="prewrap">
          <xsl:with-param name="text" select="substring-after($text,'&#x9;')" />
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="$spaceIndex &lt; $lineFeedIndex and $tabIndex &lt; $lineFeedIndex">
        <!-- line feed -->
        <xsl:value-of select="substring-before($text, '&#xA;')" />
        <br />
        <xsl:call-template name="prewrap">
          <xsl:with-param name="text" select="substring-after($text,'&#xA;')" />
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="$lineFeedIndex &lt; $spaceIndex and $tabIndex &lt; $spaceIndex">
        <!-- two spaces -->
        <xsl:value-of select="substring-before($text, '  ')" />
        <xsl:text disable-output-escaping="yes"> </xsl:text>
        <xsl:text disable-output-escaping="yes"> </xsl:text>
        <xsl:call-template name="prewrap">
          <xsl:with-param name="text" select="substring-after($text, '  ')" />
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <!-- should never happen -->
        <xsl:value-of select="$text" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  <xsl:template name="write_date">
    <xsl:param name="vtext" />
    <xsl:choose>
      <xsl:when test="string-length($vtext) = 8">
        <xsl:value-of select="concat(substring($vtext,5,2),'/',substring($vtext,7,2),'/',substring($vtext,1,4))" />
      </xsl:when>
      <xsl:when test="string-length($vtext) = 6">
        <xsl:value-of select="concat(substring($vtext,5,2),'/',substring($vtext,1,4))" />
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$vtext" />
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>