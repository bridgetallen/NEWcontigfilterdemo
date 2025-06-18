/*
A KBase module: bridgetallencontigfilterappdemo
*/

module bridgetallencontigfilterappdemo {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_bridgetallencontigfilterappdemo(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

    /*
        A variation of the contig filter that filters by both minimum and maximum contig length.
    */
    funcdef run_bridgetallencontigfilterappdemo_max(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;
};

