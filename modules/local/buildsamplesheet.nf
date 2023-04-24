process BuildSampleSheet {

    input:
    path(fastqs)
    val(bucket)

    output:
    path("*.csv")

    script:
    """
    make_samplesheet.py --bucket $bucket --strandedness $params.strandedness --fastqs ${fastqs.join(" ")} --output samplesheet.csv
    """
}
