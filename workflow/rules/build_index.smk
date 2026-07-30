rule combine_sequences:
    input:
        sequences=config["sequences"],
    output:
        fasta=f"{config['index_name']}.combined.fasta",
    log:
        "logs/combine_sequences/combine_sequences.log",
    benchmark:
        "benchmarks/combine_sequences/combine_sequences.txt"
    conda:
        "../envs/bowtie2.yaml"
    script:
        "../scripts/combine_sequences.py"


rule bowtie2_build:
    input:
        fasta=rules.combine_sequences.output.fasta,
    output:
        multiext(
            config["index_name"],
            ".1.bt2",
            ".2.bt2",
            ".3.bt2",
            ".4.bt2",
            ".rev.1.bt2",
            ".rev.2.bt2",
        ),
    params:
        index_name=lambda w, output: output[0][: -len(".1.bt2")],
    log:
        "logs/bowtie2_build/bowtie2_build.log",
    benchmark:
        "benchmarks/bowtie2_build/bowtie2_build.txt"
    conda:
        "../envs/bowtie2.yaml"
    threads: 4
    shell:
        "bowtie2-build --threads {threads} {input.fasta} {params.index_name} &> {log}"
