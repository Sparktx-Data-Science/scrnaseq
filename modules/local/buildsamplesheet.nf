process BuildSampleSheet {

    input:
    path(fastqs)

    output:
    path("*.csv")

    script:
    """
    make_samplesheet.py --strandedness $params.strandedness --fastqs ${fastqs.join(" ")} --output samplesheet.csv
    """
}
