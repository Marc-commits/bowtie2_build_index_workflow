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
    log:
        "logs/bowtie2_build/bowtie2_build.log",
    # No benchmark: directive here on purpose. Snakemake refuses to mark a
    # rule with a benchmark as cache-eligible (snakemake/snakemake#2238), and
    # consumers enable between-workflow caching on this rule via
    # `use rule bowtie2_build from ... with: cache: True`.
    conda:
        "../envs/bowtie2.yaml"
    threads: 4
    params:
        index_name=lambda w, output: output[0][: -len(".1.bt2")],
    shell:
        "bowtie2-build --threads {threads} {input.fasta} {params.index_name} &> {log}"
