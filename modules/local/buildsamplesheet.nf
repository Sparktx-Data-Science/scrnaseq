process BuildSampleSheet {
    container "125195589298.dkr.ecr.us-east-2.amazonaws.com/cbml-pandas:v1"

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
